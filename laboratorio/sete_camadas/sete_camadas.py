"""Sete camadas operacionais e dez níveis de observação: experimento, não AGI/ASI.

Cosseno duplicado significa cos(2θ)=2*cos(θ)**2-1. A geometria é vetorial
euclidiana com uma relação algébrica trigonométrica, não geometria algébrica
geral. Probabilidade de acerto condicionada e mistura calibrada substituem
a expressão sem evento definido 'probabilidade da própria probabilidade'.
"""
from dataclasses import dataclass
import argparse
import asyncio
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np


@dataclass(frozen=True)
class Configuracao:
    semente: int = 42
    ciclos: int = 4
    epocas: int = 35
    largura: int = 12
    epsilon: float = 0.15
    meta_limpa: float = 0.85
    meta_adversa: float = 0.70
    modo: str = 'ambos'

    def validar(self):
        if not 2 <= self.ciclos <= 30 or not 1 <= self.epocas <= 150 or not 6 <= self.largura <= 64:
            raise ValueError('Use 2–30 ciclos, 1–150 épocas e largura 6–64.')
        if not math.isfinite(self.epsilon) or not 0 <= self.epsilon <= .5:
            raise ValueError('epsilon deve ser finito e pertencer a [0,.5].')
        if not all(math.isfinite(x) and .5 <= x <= 1 for x in (self.meta_limpa,self.meta_adversa)):
            raise ValueError('Metas observadas devem estar entre .5 e 1.')
        if self.modo not in ('sincrono','assincrono','ambos'):
            raise ValueError('Modo inválido.')


def normalizar(v):
    v=np.asarray(v,dtype=float)
    if not np.isfinite(v).all(): raise ValueError('Vetor não finito.')
    n=np.linalg.norm(v)
    return v/n if n>1e-12 else np.zeros_like(v)


def vetor_recursivo(anterior,observacao,taxa=.25):
    if not 0<=taxa<=1:raise ValueError('Taxa fora de [0,1].')
    return normalizar((1-taxa)*normalizar(anterior)+taxa*normalizar(observacao))


def geometria(x,referencia):
    x=np.asarray(x,dtype=float);r=normalizar(referencia)
    if x.ndim!=2 or x.shape[1]!=4 or r.shape!=(4,) or not np.isfinite(x).all():
        raise ValueError('Esperados vetores finitos com quatro coordenadas.')
    n=np.linalg.norm(x,axis=1,keepdims=True);safe=np.maximum(n,1e-12)
    c=(x@r[:,None])/safe
    c=np.clip(c,-1,1)
    # Referência nula define a convenção c=0; não inventa uma direção.
    dc=r[None,:]/safe-c*x/(safe**2)
    dc[n[:,0]<=1e-12]=0
    return np.concatenate((x,c,2*c*c-1),axis=1),dc,c


def sigmoide(z):
    z=np.asarray(z,dtype=float)
    return np.exp(-np.logaddexp(0,-z))


class RedeSeteCamadas:
    """Uma entrada, cinco blocos residuais tanh e uma saída: sete mapas afins."""
    def __init__(self,semente=0,largura=12):
        rng=np.random.default_rng(semente);dims=[(6,largura)]+[(largura,largura)]*5+[(largura,1)]
        self.parametros=[(rng.normal(0,.5/math.sqrt(a),(a,b)),np.zeros((1,b))) for a,b in dims]
        self.residual=.2

    def copia(self):
        nova=object.__new__(type(self));nova.residual=self.residual
        nova.parametros=[(w.copy(),b.copy()) for w,b in self.parametros]
        return nova

    def frente(self,x):
        h=x;caches=[]
        for i,(w,b) in enumerate(self.parametros):
            anterior=h;z=h@w+b
            if i==6:h=z;caches.append((anterior,None))
            else:
                a=np.tanh(z);h=a if i==0 else h+self.residual*a;caches.append((anterior,a))
        return h,caches

    def gradientes(self,x,y):
        logits,caches=self.frente(x);y=np.asarray(y).reshape(-1,1)
        loss=float(np.mean(np.logaddexp(0,logits)-y*logits))
        delta=(sigmoide(logits)-y)/len(x);grads=[None]*7
        for i in range(6,-1,-1):
            anterior,a=caches[i];w,_=self.parametros[i]
            if i==6:dz=delta;identidade=0
            elif i==0:dz=delta*(1-a*a);identidade=0
            else:dz=delta*self.residual*(1-a*a);identidade=delta
            grads[i]=(anterior.T@dz,np.sum(dz,axis=0,keepdims=True))
            delta=dz@w.T+identidade
        return loss,grads,delta

    def atualizar(self,grads,taxa):
        norm=math.sqrt(sum(float(np.sum(a*a)+np.sum(b*b)) for a,b in grads))
        escala=min(1.,5./max(norm,1e-12))
        for (w,b),(dw,db) in zip(self.parametros,grads):w-=taxa*escala*dw;b-=taxa*escala*db


class Confiabilidade:
    """P(acerto | faixa de confiança), Beta(1,1), ajustada somente na calibração."""
    def __init__(self):self.contagens=np.zeros(5);self.acertos=np.zeros(5)

    @staticmethod
    def indice(p):return np.minimum(4,((np.maximum(p,1-p)-.5)*10).astype(int)).reshape(-1)

    def ajustar(self,p,y):
        ids=self.indice(p);ok=((p.reshape(-1)>=.5)==np.asarray(y).reshape(-1))
        self.contagens=np.bincount(ids,minlength=5).astype(float)
        self.acertos=np.bincount(ids,weights=ok,minlength=5)

    def prever(self,p):
        ids=self.indice(p)
        return ((self.acertos[ids]+1)/(self.contagens[ids]+2)).reshape(-1,1)

    def copia(self):
        c=Confiabilidade();c.contagens=self.contagens.copy();c.acertos=self.acertos.copy();return c


class Artefato:
    def __init__(self,rede,referencia,versao=0):
        self.rede=rede;self.referencia=normalizar(referencia);self.versao=versao
        self.temperatura=1.;self.confiabilidade=Confiabilidade()

    def copia(self):
        c=Artefato(self.rede.copia(),self.referencia.copy(),self.versao)
        c.temperatura=self.temperatura;c.confiabilidade=self.confiabilidade.copia();return c

    def congelada(self):
        c=self.copia()
        for w,b in c.rede.parametros:w.setflags(write=False);b.setflags(write=False)
        for v in (c.referencia,c.confiabilidade.contagens,c.confiabilidade.acertos):v.setflags(write=False)
        return c

    def probabilidades(self,x):
        f,_,_=geometria(x,self.referencia)
        return sigmoide(self.rede.frente(f)[0]/self.temperatura)

    def calibrar(self,x,y):
        f,_,_=geometria(x,self.referencia);z=self.rede.frente(f)[0];y=y.reshape(-1,1)
        opcoes=[.5,.75,1.,1.25,1.5,2.]
        self.temperatura=min(opcoes,key=lambda t:float(np.mean(np.logaddexp(0,z/t)-y*z/t)))
        self.confiabilidade.ajustar(sigmoide(z/self.temperatura),y)

    def gradiente_entrada(self,x,y):
        f,dc,c=geometria(x,self.referencia)
        # Temperatura é uma escala positiva; a direção do ataque BCE é a mesma.
        _,_,df=self.rede.gradientes(f,y)
        return df[:,:4]+(df[:,4:5]+4*c*df[:,5:6])*dc

    def atacar(self,x,y,epsilon,passos=5,semente=99):
        rng=np.random.default_rng(semente);original=np.asarray(x,dtype=float)
        if not math.isfinite(epsilon) or epsilon<0:raise ValueError('Orçamento de ataque inválido.')
        def perdas(v):
            f,_,_=geometria(v,self.referencia)
            z=self.rede.frente(f)[0]/self.temperatura
            return (np.logaddexp(0,z)-y.reshape(-1,1)*z).reshape(-1)
        pior=original.copy();maxima=perdas(pior)
        def reter(v):
            nonlocal pior,maxima
            loss=perdas(v);ids=loss>maxima
            pior[ids]=v[ids];maxima[ids]=loss[ids]
        a=original+rng.uniform(-epsilon,epsilon,original.shape)
        reter(a)
        for _ in range(passos):
            a+=epsilon/3*np.sign(self.gradiente_entrada(a,y))
            a=np.clip(a,original-epsilon,original+epsilon)
            reter(a)
        return pior

    def treinar(self,x,y,epocas,taxa,peso_adverso,epsilon,semente):
        rng=np.random.default_rng(semente)
        for epoca in range(epocas):
            ordem=rng.permutation(len(x))
            for inicio in range(0,len(x),64):
                ids=ordem[inicio:inicio+64];bx=x[ids];by=y[ids]
                adverso=bx+epsilon*np.sign(self.gradiente_entrada(bx,by))
                f,_,_=geometria(bx,self.referencia);fa,_,_=geometria(adverso,self.referencia)
                _,g,_=self.rede.gradientes(f,by);_,ga,_=self.rede.gradientes(fa,by)
                combinado=[((1-peso_adverso)*a+peso_adverso*c,(1-peso_adverso)*b+peso_adverso*d) for (a,b),(c,d) in zip(g,ga)]
                self.rede.atualizar(combinado,taxa/(1+epoca/epocas))


def dados(semente,n):
    rng=np.random.default_rng(semente);x=rng.normal(0,1,(n,4))
    y=(.8*x[:,0]-.6*x[:,1]+.3*x[:,2]*x[:,3]>0).astype(float).reshape(-1,1)
    return x,y


def wilson(acertos,n,z=1.96):
    p=acertos/n;d=1+z*z/n
    centro=(p+z*z/(2*n))/d
    raio=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0,centro-raio),min(1,centro+raio)]


def avaliar(artefato,x,y,epsilon):
    p=artefato.probabilidades(x);a=artefato.atacar(x,y,epsilon)
    pa=artefato.probabilidades(a)
    acertos=int(np.sum((p>=.5)==y));adversos=int(np.sum((pa>=.5)==y))
    q=artefato.confiabilidade.prever(p);ok=((p>=.5)==y).astype(float)
    return dict(acuracia=acertos/len(x),adversa=adversos/len(x),
        brier=float(np.mean((p-y)**2)),brier_confiabilidade=float(np.mean((q-ok)**2)),
        probabilidade_media=float(np.mean(p)),probabilidade_acerto=float(np.mean(q)),
        intervalo_limpo=wilson(acertos,len(x)),intervalo_adverso=wilson(adversos,len(x)),
        n=len(x),max_perturbacao=float(np.max(np.abs(a-x))))


async def avaliar_par(atual,candidata,x,y,epsilon,modo):
    # Congelar snapshots antes das tarefas: nenhum treinamento concorre com estas leituras.
    snapshots=(atual.congelada(),candidata.congelada())
    x=x.copy();y=y.copy();x.setflags(write=False);y.setflags(write=False)
    if modo=='assincrono':
        rs=await asyncio.gather(*(asyncio.to_thread(avaliar,s,x,y,epsilon) for s in snapshots))
    else:rs=[avaliar(s,x,y,epsilon) for s in snapshots]
    return rs


class MetaRecursiva:
    """Auto-observação operacional, com evidências contadas uma vez por ciclo."""
    def __init__(self):
        self.sucessos=1;self.falhas=1;self.eventos=set();self.historico=[]

    @property
    def confianca(self):return self.sucessos/(self.sucessos+self.falhas)

    @staticmethod
    def revisar_anterior(node):
        """Juízo recursivo sobre o resultado anterior, sem criar observações externas."""
        if node is None:return dict(consistente=True,niveis_revisados=0,motivos=[])
        filho=MetaRecursiva.revisar_anterior(node['observa'])
        motivos=list(filho['motivos'])
        for nome,valor in node['resultado'].items():
            if isinstance(valor,(int,float)) and not isinstance(valor,bool):
                if not math.isfinite(valor):motivos.append(f"{node['nivel']}:{nome}:não finito")
                elif (nome.startswith('prob_') or nome=='media_beta') and not 0<=valor<=1:
                    motivos.append(f"{node['nivel']}:{nome}:fora de [0,1]")
        if node['nivel']!=filho['niveis_revisados']+1:motivos.append('ordem de dependências inválida')
        return dict(consistente=not motivos,niveis_revisados=filho['niveis_revisados']+1,motivos=motivos)

    def plano(self,ciclo,orientacao):
        peso=min(.65,.25+.08*(ciclo-1))
        if self.historico and self.historico[-1]['dissonancia']>.15:peso=min(.75,peso+.1)
        taxa=.12*(.75+.25*self.confianca)
        if orientacao=='versa':
            pergunta='Qual mudança verificável reduz erros sob ataque sem abandonar o desempenho nominal?'
            resposta=f'Testar treino adversarial com peso {peso:.3f}, taxa {taxa:.4f}, mantendo contratos e reserva intactos.'
            papeis=['lógica criativa pergunta','criatividade lógica responde']
        else:
            pergunta='Que pressuposto ou dilema pode refutar a utilidade da mudança proposta?'
            resposta='Comparar a candidata com a versão congelada; rejeitar regressão nominal excessiva e registrar custo, dissonância e falhas.'
            papeis=['criatividade lógica pergunta','lógica criativa responde']
        return dict(pergunta=pergunta,resposta=resposta,papeis=papeis,peso=peso,taxa=taxa)

    def observar(self,ciclo,baseline,candidata,aceita,orientacao):
        if ciclo in self.eventos:raise ValueError('Evidência metacognitiva já consumida.')
        self.eventos.add(ciclo)
        delta=candidata['adversa']-baseline['adversa']
        # Nível dois julga a recomendação do nível um pelo ganho efetivamente observado.
        util=delta>.002 and candidata['acuracia']>=baseline['acuracia']-.03
        self.sucessos+=int(util);self.falhas+=int(not util)
        confianca=self.confianca
        q=candidata['probabilidade_acerto']
        # Mistura de hipóteses, não P(P(A)) nem multiplicação repetida da mesma evidência.
        q_meta=confianca*q+(1-confianca)*.5
        diss=max(0,candidata['acuracia']-candidata['adversa'])
        valores=[
            ('inferência',dict(prob_evento=candidata['probabilidade_media'])),
            ('probabilidade condicionada',dict(prob_acerto_calibrada=q)),
            ('metacognição analítica',dict(brier=candidata['brier'],brier_confiabilidade=candidata['brier_confiabilidade'])),
            ('probabilidade da recomendação',dict(media_beta=confianca,sucessos=self.sucessos-1,falhas=self.falhas-1)),
            ('dissonância operacional',dict(lacuna_limpa_adversa=diss)),
            ('metacognição da metacognição',dict(recomendacao_util=util,ganho_adverso=delta)),
            ('metacognição dentro da probabilidade',dict(prob_acerto_mistura=q_meta,politica='mistura heurística; garantia de calibração não demonstrada')),
            ('dilema pragmático',dict(aceita=aceita,regressao_nominal=baseline['acuracia']-candidata['acuracia'])),
            ('auditoria axiomática',dict(evidencia_unica=True,profundidade_limitada=10,reserva_usada=False)),
            ('auto-observação integrada',dict(ciclo=ciclo,eventos_distintos=len(self.eventos),prova_de_cognicao_plena=False)),
        ]
        anterior=None
        for i,(nome,valor) in enumerate(valores,1):
            juizo=self.revisar_anterior(anterior)
            hash_entrada=hashlib.sha256(json.dumps(anterior,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            anterior=dict(nivel=i,operacao=nome,resultado=valor,observa=anterior,
                juizo_metacognitivo_sobre_anterior=juizo,hash_entrada=hash_entrada,
                cria_evidencia_independente=False)
        percurso=list(range(1,11)) if orientacao=='versa' else list(range(10,0,-1))
        resumo=dict(dissonancia=diss,delta=delta,confianca=confianca)
        self.historico.append(resumo)
        return dict(resultado_metacognitivo=anterior,percurso=percurso,
            revisao_recursiva_final=self.revisar_anterior(anterior),
            probabilidade_dentro_da_metacognicao=q,metacognicao_dentro_da_probabilidade=q_meta,
            limites='Médias Beta e mistura são descrições heurísticas sob seleção adaptativa; não certificam probabilidades de sucesso fora do benchmark.')


async def executar(config):
    config.validar();inicio=time.perf_counter()
    treino=dados(config.semente+11,512)
    calibracao=dados(config.semente+23,192)
    desenvolvimento=dados(config.semente+37,256)
    # A reserva só será gerada/consultada depois de congelar a seleção.
    atual=Artefato(RedeSeteCamadas(config.semente,config.largura),[1,0,0,0])
    atual.calibrar(*calibracao);meta=MetaRecursiva();tracos=[]
    for ciclo in range(1,config.ciclos+1):
        orientacao='versa' if ciclo%2 else 'reversa';plano=meta.plano(ciclo,orientacao)
        candidata=atual.copia();candidata.versao=atual.versao+1
        candidata.referencia=vetor_recursivo(atual.referencia,np.mean(treino[0],axis=0))
        modo=config.modo if config.modo!='ambos' else ('sincrono' if ciclo%2 else 'assincrono')
        treino_args=(*treino,config.epocas,plano['taxa'],plano['peso'],config.epsilon,config.semente+ciclo)
        if modo=='assincrono':await asyncio.to_thread(candidata.treinar,*treino_args)
        else:candidata.treinar(*treino_args)
        candidata.calibrar(*calibracao)
        baseline,resultado=await avaliar_par(atual,candidata,*desenvolvimento,config.epsilon,modo)
        aceita=(resultado['adversa']>baseline['adversa']+.002 and resultado['acuracia']>=baseline['acuracia']-.03)
        observacao=meta.observar(ciclo,baseline,resultado,aceita,orientacao)
        if aceita:atual=candidata
        tracos.append(dict(ciclo=ciclo,orientacao=orientacao,modo=modo,
            sete_camadas=['axiomas','geometria recursiva','diálogo invertível','rede de sete mapas afins','avaliação adversarial','metacognição recursiva','integração versionada'],
            pergunta=plano['pergunta'],resposta=plano['resposta'],papeis=plano['papeis'],
            candidata=resultado,baseline=baseline,aceita=aceita,versao_vigente=atual.versao,
            observacao=observacao))
        escolhido=resultado if aceita else baseline
        if ciclo>=2 and escolhido['acuracia']>=config.meta_limpa and escolhido['adversa']>=config.meta_adversa:break
    confirmado=avaliar(atual,*dados(config.semente+53,512),config.epsilon)
    atingiu=confirmado['acuracia']>=config.meta_limpa and confirmado['adversa']>=config.meta_adversa
    return dict(natureza='protótipo experimental; não demonstra AGI/ASI ou consciência',
        status='meta_observada_no_benchmark' if atingiu else 'meta_nao_atingida_no_orcamento',
        criterio_observado=atingiu,criterio='limiares pontuais reservados; não prova estatística de promoção',
        camadas_operacionais=7,camadas_afins_rede=7,niveis_observacao=10,
        cosseno_duplicado='cos(2θ)=2 cos²(θ)−1',metacognicao_dentro_metacognicao=True,
        ciclos_executados=len(tracos),versao_final=atual.versao,confirmacao=confirmado,
        confirmacao_consultada_uma_vez=True,segundos=round(time.perf_counter()-inicio,3),
        execucao_futura_automatica=False,tracos=tracos,
        limites=['Domínio sintético único; não generalidade aberta.',
            'Ataque PGD delimitado por norma infinito; não robustez universal.',
            'Seleção adaptativa usa desenvolvimento repetido; confirmação não retorna ao treino.',
            'Inversão muda investigação e percurso de auditoria, preservando dependências de cálculo.',
            'Autopoiese é manutenção de snapshots/estratégias sob contratos fixos, não autonomia biológica.',
            'Dez observações aninhadas não constituem dez fontes independentes de evidência.'])


def main(args=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--semente',type=int,default=42);p.add_argument('--ciclos',type=int,default=4)
    p.add_argument('--epocas',type=int,default=35)
    p.add_argument('--modo',choices=['sincrono','assincrono','ambos'],default='ambos')
    p.add_argument('--saida',type=Path)
    a=p.parse_args(args)
    resultado=asyncio.run(executar(Configuracao(semente=a.semente,ciclos=a.ciclos,epocas=a.epocas,modo=a.modo)))
    texto=json.dumps(resultado,ensure_ascii=False,indent=2,allow_nan=False)
    if a.saida:a.saida.write_text(texto+'\n',encoding='utf-8')
    print(texto)
    return 0


if __name__=='__main__':raise SystemExit(main())
