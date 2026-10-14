"""Previsão latente condicionada a ações e MPC local em um mundo linear sintético.

Experimento inspirado em predição joint-embedding. Não é uma implementação de
I-JEPA/V-JEPA2, não usa LLaMA, não constitui integração oficial com Meta AI.
Sem rede, credenciais, aquisição de recursos ou autorreplicação de processos.
"""
from dataclasses import dataclass,field
from pathlib import Path
import argparse
import asyncio
import hashlib
import json
import math
import os
import tempfile
import threading

import numpy as np

A=np.array([[1.,.15],[0.,.9]])
B=np.array([[0.],[.15]])


def transicao(estado,acao):
    x=np.asarray(estado,dtype=float);u=np.asarray(acao,dtype=float).reshape(-1,1)
    if x.ndim==1:x=x.reshape(1,2)
    if x.shape!=(len(u),2) or not np.isfinite(x).all() or not np.isfinite(u).all():
        raise ValueError('Estados e ações devem ser finitos e compatíveis.')
    if np.max(np.abs(u))>1+1e-12:raise ValueError('Ação excede o intervalo [-1,1].')
    return x@A.T+u@B.T


def gerar_transicoes(semente,n):
    rng=np.random.default_rng(semente)
    x=rng.uniform(-2,2,(n,2));u=rng.uniform(-1,1,(n,1))
    return x,u,transicao(x,u)


def regularizacao(h,gamma=.35):
    """Penalidades variance/covariance e gradiente, sem tratar colapso como impossível."""
    n,d=h.shape
    if n<2:raise ValueError('Regularização exige pelo menos duas observações.')
    c=h-h.mean(axis=0);cov=c.T@c/(n-1)
    std=np.sqrt(np.diag(cov)+1e-4)
    variancia=float(np.mean(np.maximum(0,gamma-std)))
    dv=-c*((std<gamma)/std)[None,:]/(d*(n-1))
    off=cov-np.diag(np.diag(cov))
    covariancia=float(np.sum(off*off)/d)
    dc=4*c@off/(d*(n-1))
    return variancia,covariancia,dv,dc


class ModeloLatente:
    def __init__(self,semente=0):
        rng=np.random.default_rng(semente)
        self.encoder=rng.normal(0,.5,(2,3));self.alvo=self.encoder.copy()
        self.preditor=np.vstack((np.eye(3),np.zeros((1,3))))
        self.bias=np.zeros((1,3));self.alinhado=False

    def validar(self):
        for nome,shape in dict(encoder=(2,3),alvo=(2,3),preditor=(4,3),bias=(1,3)).items():
            a=getattr(self,nome)
            if not isinstance(a,np.ndarray) or a.shape!=shape or not np.isfinite(a).all():
                raise ValueError('Parâmetro inválido: '+nome)

    def codificar(self,x):return np.asarray(x)@self.encoder

    def prever(self,z,u):
        return np.concatenate((z,np.asarray(u).reshape(-1,1)),axis=1)@self.preditor+self.bias

    def perda_gradientes(self,x,u,y,peso_variancia=.2,peso_covariancia=.02):
        hx=x@self.encoder;hy=y@self.encoder
        target=y@self.alvo  # stop-gradient: alvo permanece constante nesta derivada.
        features=np.concatenate((hx,u),axis=1)
        pred=features@self.preditor+self.bias;delta=pred-target
        dp=2*delta/delta.size
        dencoder=x.T@(dp@self.preditor[:3].T)
        inv=float(np.mean(delta*delta));var=0.;cov=0.
        for entrada,h in ((x,hx),(y,hy)):
            v,c,dv,dc=regularizacao(h);var+=v;cov+=c
            dencoder+=entrada.T@(peso_variancia*dv+peso_covariancia*dc)
        loss=inv+peso_variancia*var+peso_covariancia*cov
        return loss,(dencoder,features.T@dp,np.sum(dp,axis=0,keepdims=True)),dict(invariancia=inv,variancia=var,covariancia=cov)

    def treinar(self,x,u,y,epocas=150,taxa=.03):
        self.validar()
        x,u,y=(np.asarray(a,dtype=float) for a in (x,u,y))
        if x.ndim!=2 or len(x)<2 or x.shape[1]!=2 or y.shape!=x.shape or u.shape!=(len(x),1):
            raise ValueError('Treino exige Nx2,Nx1,Nx2 e n>=2.')
        if not all(np.isfinite(a).all() for a in (x,u,y)):raise ValueError('Dados não finitos.')
        if type(epocas) is not int or not 1<=epocas<=500 or not math.isfinite(taxa) or not 0<taxa<=.1:
            raise ValueError('Orçamento/taxa inválidos.')
        historia=[]
        for i in range(epocas):
            loss,(de,dp,db),componentes=self.perda_gradientes(x,u,y)
            self.encoder-=taxa*de;self.preditor-=taxa*dp;self.bias-=taxa*db
            self.alvo=.99*self.alvo+.01*self.encoder
            if i in (0,epocas-1):historia.append(dict(epoca=i,perda=loss,**componentes))
        # Congelar o encoder e reconciliar bases antes do rollout multietapa.
        # Isso é uma calibração linear declarada, não um detalhe oculto da JEPA.
        self.alvo=self.encoder.copy()
        f=np.concatenate((x@self.encoder,u,np.ones((len(x),1))),axis=1)
        solu=np.linalg.lstsq(f,y@self.encoder,rcond=None)[0]
        self.preditor=solu[:4];self.bias=solu[4:5];self.alinhado=True
        return historia

    def copia(self,congelar=False):
        m=object.__new__(type(self));m.alinhado=self.alinhado
        for nome in ('encoder','alvo','preditor','bias'):
            v=getattr(self,nome).copy()
            if congelar:v.setflags(write=False)
            setattr(m,nome,v)
        return m

    def diagnostico(self,x,u,y):
        z=x@self.encoder;target=y@self.encoder;pred=self.prever(z,u)
        singular=np.linalg.svd(self.encoder,compute_uv=False)
        std=z.std(axis=0,ddof=1)
        denom=float(np.mean(target*target))
        mse=float(np.mean((pred-target)**2))
        return dict(mse_latente=mse,mse_relativo=mse/max(denom,1e-12),
            desvio_latente=std.tolist(),posto_encoder=int(np.sum(singular>1e-8)),
            colapso_detectado=bool(np.mean(std)<.1 or np.sum(singular>1e-8)<2),
            base_alinhada=self.alinhado)


def planejar(modelo,estado,objetivo,horizonte=8,candidatos=128,semente=0):
    modelo.validar()
    if not modelo.alinhado:raise ValueError('Bases devem ser alinhadas antes de compor previsões.')
    if not 1<=horizonte<=12 or not 2<=candidatos<=512:raise ValueError('Orçamento de planejamento excedido.')
    if np.linalg.matrix_rank(modelo.encoder)<2:raise ValueError('Representação sem informação suficiente.')
    estado=np.asarray(estado,dtype=float).reshape(1,2)
    objetivo=np.asarray(objetivo,dtype=float).reshape(1,2)
    if not np.isfinite(estado).all() or not np.isfinite(objetivo).all():raise ValueError('Estado/objetivo não finito.')
    rng=np.random.default_rng(semente);seq=rng.uniform(-1,1,(candidatos,horizonte))
    seq[0]=0.;seq[1]=-1 if estado[0,0]>objetivo[0,0] else 1
    z=np.repeat(modelo.codificar(estado),candidatos,axis=0)
    zg=modelo.codificar(objetivo);custos=np.zeros(candidatos)
    for t in range(horizonte):
        u=seq[:,t:t+1];z=modelo.prever(z,u)
        custos+=np.sum((z-zg)**2,axis=1)+.02*u[:,0]**2
    if not np.isfinite(custos).all():raise ValueError('Custos previstos não finitos.')
    i=int(np.argmin(custos))
    return dict(acao=float(seq[i,0]),custo_previsto=float(custos[i]),
        custo_sequencia_nula=float(custos[0]),horizonte=horizonte,candidatos=candidatos)


@dataclass
class ControleExecucao:
    autorizado: bool=True
    encerrado: bool=False
    _lock: object=field(default_factory=threading.RLock,repr=False,compare=False)

    def parar(self):
        with self._lock:self.encerrado=True

    def ativo(self):
        with self._lock:return self.autorizado and not self.encerrado

    def efetivar(self,operacao):
        with self._lock:
            if not self.autorizado or self.encerrado:return None
            return operacao()

    def snapshot(self):
        with self._lock:return dict(autorizado=self.autorizado,encerrado=self.encerrado)


def controlar(modelo,inicial,objetivo,controle,passos=20,semente=0):
    if not 0<=passos<=100:raise ValueError('Orçamento de ações inválido.')
    state=np.asarray(inicial,dtype=float).reshape(1,2).copy()
    objetivo=np.asarray(objetivo,dtype=float).reshape(1,2)
    custo=0.;trace=[]
    if not np.isfinite(state).all() or not np.isfinite(objetivo).all():raise ValueError('Estado/objetivo não finito.')
    def parado():return dict(status='encerrado',estado=state[0].tolist(),acoes=len(trace),custo=custo,traco=trace)
    if not controle.ativo():return parado()
    for t in range(passos):
        if not controle.ativo():return parado()
        p=planejar(modelo,state[0],objetivo[0],semente=semente+t)
        novo=controle.efetivar(lambda:transicao(state,[[p['acao']]]))
        if novo is None:return parado()
        state=novo
        custo+=float(np.sum((state-np.asarray(objetivo))**2)+.02*p['acao']**2)
        trace.append(dict(passo=t,estado=state[0].tolist(),**p))
    return dict(status='orcamento_concluido',estado=state[0].tolist(),acoes=len(trace),custo=custo,traco=trace)


def _json(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)


def salvar_checkpoint(caminho,modelo,estado,controle):
    modelo.validar()
    payload=dict(formato=1,alinhado=modelo.alinhado,
        parametros={n:getattr(modelo,n).tolist() for n in ('encoder','alvo','preditor','bias')},
        estado=list(map(float,estado)),controle=controle.snapshot())
    encoded=_json(payload)
    envelope=dict(payload=payload,sha256=hashlib.sha256(encoded.encode()).hexdigest())
    destino=Path(caminho).resolve();destino.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.checkpoint_',dir=destino.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(_json(envelope)+'\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,destino)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def restaurar_checkpoint(caminho):
    envelope=json.loads(Path(caminho).read_text());p=envelope['payload']
    if hashlib.sha256(_json(p).encode()).hexdigest()!=envelope['sha256']:raise ValueError('Checksum divergente.')
    if p['formato']!=1 or type(p['alinhado']) is not bool:raise ValueError('Formato inválido.')
    for key in ('autorizado','encerrado'):
        if type(p['controle'][key]) is not bool:raise ValueError('Estado de controle inválido.')
    modelo=ModeloLatente();shapes=dict(encoder=(2,3),alvo=(2,3),preditor=(4,3),bias=(1,3))
    for n,shape in shapes.items():
        a=np.array(p['parametros'][n],dtype=float)
        if a.shape!=shape or not np.isfinite(a).all():raise ValueError('Parâmetro inválido: '+n)
        setattr(modelo,n,a)
    state=np.array(p['estado'],dtype=float)
    if state.shape!=(2,) or not np.isfinite(state).all():raise ValueError('Estado inválido.')
    modelo.alinhado=p['alinhado'];controle=ControleExecucao(**p['controle'])
    if modelo.alinhado and not np.allclose(modelo.encoder,modelo.alvo):raise ValueError('Bases declaradas alinhadas divergem.')
    # Carregar artefatos não inicia threads, tarefas nem retoma autorização revogada.
    return modelo,state,controle


async def experimento(semente=7,epocas=150,checkpoint=None):
    treino=gerar_transicoes(semente+1,1024);teste=gerar_transicoes(semente+2,256)
    modelo=ModeloLatente(semente);antes=modelo.diagnostico(*teste)
    historia=modelo.treinar(*treino,epocas=epocas)
    depois=modelo.diagnostico(*teste)
    snapshot=modelo.copia(congelar=True)
    iniciais=[np.array([1.5,0]),np.array([-1.5,0]),np.array([1.,.5]),np.array([-1.,-.5])]
    def avaliar_estado(x,i):
        result=controlar(snapshot,x,[0,0],ControleExecucao(),semente=semente+100*i)
        z=np.asarray(x).reshape(1,2);cost0=0.
        for _ in range(20):z=transicao(z,[[0.]]);cost0+=float(np.sum(z*z))
        return dict(**result,custo_sem_controle=cost0)
    resultados=await asyncio.gather(*(asyncio.to_thread(avaliar_estado,x,i) for i,x in enumerate(iniciais)))
    stop=ControleExecucao();stop.parar()
    interrompido=controlar(snapshot,iniciais[0],[0,0],stop)
    if checkpoint:salvar_checkpoint(checkpoint,snapshot,resultados[-1]['estado'],stop)
    return dict(natureza='modelo de mundo linear sintético inspirado em joint-embedding; não Meta JEPA/LLaMA',
        antes=antes,depois=depois,historico=historia,controles=resultados,
        custo_medio=float(np.mean([r['custo'] for r in resultados])),
        custo_medio_sem_controle=float(np.mean([r['custo_sem_controle'] for r in resultados])),
        encerramento_cooperativo=interrompido,
        checkpoint=str(Path(checkpoint).resolve()) if checkpoint else None,
        checkpoint_encerrado=bool(checkpoint),
        limites=['Mundo de duas coordenadas e dinâmica linear determinística.',
            'Ajuste final por mínimos quadrados após congelar e alinhar o encoder.',
            'MPC limitado por amostragem; não prova de ótimo ou robustez fora do simulador.',
            'Penalidades de variância/covariância não demonstram impossibilidade de colapso.',
            'Checkpoints são locais e explícitos; não autorreplicação ou evasão de encerramento.'])


def main(args=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--semente',type=int,default=7);p.add_argument('--epocas',type=int,default=150)
    p.add_argument('--saida',type=Path);p.add_argument('--checkpoint',type=Path)
    a=p.parse_args(args);result=asyncio.run(experimento(a.semente,a.epocas,a.checkpoint))
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if a.saida:a.saida.write_text(text+'\n',encoding='utf-8')
    print(text);return 0


if __name__=='__main__':raise SystemExit(main())
