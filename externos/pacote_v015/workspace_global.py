"""Laboratório de integração funcional inspirado em GWT/RPT/AST.
Não mede experiência subjetiva, Phi da IIT nem probabilidade de consciência.
Proveniência é metadado conhecido, não detecção de experiência real/imaginada.
"""
import argparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import copy
from dataclasses import dataclass
import math
from pathlib import Path
import random
import threading
from paradoxos_formais import analisar,instancia
from persistencia_atomica import escrever_json
from versao import VERSAO

MODULOS=('sensor_a','sensor_b','memoria','previsao','homeostase','metamonitor','escrutinio')

@dataclass(frozen=True)
class Fragmento:
    modulo: str
    origem: str
    conteudo: tuple
    prioridade: float

class WorkspaceGlobal:
    def __init__(self,recorrencia=True,difusao=True,atencao_adaptativa=True,energia=.8):
        if any(type(x) is not bool for x in (recorrencia,difusao,atencao_adaptativa)) or isinstance(energia,bool) or not isinstance(energia,(int,float)) or not math.isfinite(energia) or not 0<=energia<=1:raise ValueError('Configuração inválida.')
        self.recorrencia=recorrencia;self.difusao=difusao;self.atencao_adaptativa=atencao_adaptativa;self.energia=float(energia)
        self.modulos={m:dict(cache={},ultimo=None,recebidas=0) for m in MODULOS}
        self.atencao=[1/len(MODULOS)]*len(MODULOS);self.historico=deque(maxlen=128);self.ciclo=0;self.stm=None;self._lock=threading.Lock()
    def _propor(self,m,entrada,snapshot):
        estado=snapshot['modulos'][m];conteudo=None;origem='interno';prioridade=0.
        if m=='sensor_a' and entrada['a'] is not None:conteudo=(('a',entrada['a']),);origem='observacao';prioridade=1.
        elif m=='sensor_b' and entrada['b'] is not None:conteudo=(('b',entrada['b']),);origem='observacao';prioridade=1.
        elif m=='memoria' and estado['cache']:conteudo=tuple(sorted(estado['cache'].items()));origem='memoria';prioridade=.4
        elif m=='previsao' and estado['cache']:conteudo=tuple(sorted(estado['cache'].items()));origem='simulacao';prioridade=.3
        elif m=='homeostase':conteudo=(('energia',snapshot['energia']),);prioridade=4. if snapshot['energia']<.1 else 2. if snapshot['energia']<.25 else .05
        elif m=='metamonitor':conteudo=(('ultimo_modulo',estado['ultimo'].modulo if estado['ultimo'] else 'nenhum'),);prioridade=.08
        elif m=='escrutinio' and entrada['logica'] is not None:conteudo=(('status_logico',entrada['logica']['status']),);origem='analise';prioridade=3.
        if conteudo is None:return None
        if self.atencao_adaptativa:prioridade+=.1*(1-snapshot['atencao'][MODULOS.index(m)])
        return Fragmento(m,origem,conteudo,prioridade)
    def _validar_fragmento(self,p,m,entrada,snapshot):
        origens={'sensor_a':'observacao','sensor_b':'observacao','memoria':'memoria','previsao':'simulacao','homeostase':'interno','metamonitor':'interno','escrutinio':'analise'}
        if not isinstance(p,Fragmento) or p.modulo!=m or p.origem!=origens[m] or type(p.conteudo) is not tuple or not 1<=len(p.conteudo)<=2 or isinstance(p.prioridade,bool) or not isinstance(p.prioridade,(int,float)) or not math.isfinite(p.prioridade) or not 0<=p.prioridade<=10:raise ValueError('Identidade/proveniência de fragmento inválida.')
        dados={}
        for par in p.conteudo:
            if type(par) is not tuple or len(par)!=2 or type(par[0]) is not str or par[0] in dados:raise ValueError('Conteúdo duplicado/inválido.')
            dados[par[0]]=par[1]
        if m in ('sensor_a','sensor_b','memoria','previsao'):
            if any(k not in ('a','b') or type(v) not in (int,bool) or v not in (0,1) for k,v in dados.items()):raise ValueError('Bits do fragmento inválidos.')
            if m.startswith('sensor_'):
                k=m[-1]
                if set(dados)!={k} or entrada[k] is None or dados[k]!=entrada[k]:raise ValueError('Sensor fabricou observação.')
            elif any(k not in snapshot['modulos'][m]['cache'] or snapshot['modulos'][m]['cache'][k]!=v for k,v in dados.items()):raise ValueError('Conteúdo sem suporte na memória local.')
        elif m=='homeostase':
            if set(dados)!={'energia'} or type(dados['energia']) not in (int,float) or dados['energia']!=snapshot['energia']:raise ValueError('Estado homeostático inválido.')
        elif m=='metamonitor':
            ultimo=snapshot['modulos'][m]['ultimo'];esperado=ultimo.modulo if ultimo else 'nenhum'
            if dados!={'ultimo_modulo':esperado}:raise ValueError('Metamonitor sem suporte.')
        elif dados!={'status_logico':entrada['logica']['status'] if entrada['logica'] else None} or entrada['logica'] is None:raise ValueError('Diagnóstico lógico inválido.')

    def _torneio(self,candidatos):
        nivel=list(candidatos);comparacoes=0
        if not nivel:raise ValueError('Nenhum candidato válido.')
        while len(nivel)>1:
            proximo=[]
            for i in range(0,len(nivel),2):
                if i+1==len(nivel):proximo.append(nivel[i]);continue
                a,b=nivel[i:i+2];comparacoes+=1
                proximo.append(a if a.prioridade>=b.prioridade else b)
            nivel=proximo
        return nivel[0],comparacoes
    def _difundir(self,fragmento,destinos):
        for m in destinos:
            estado=self.modulos[m];estado['recebidas']+=1;estado['ultimo']=fragmento
            if fragmento.origem in ('observacao','memoria'):
                for k,v in fragmento.conteudo:
                    if k in ('a','b'):estado['cache'][k]=v
    def passo(self,a=None,b=None,formulas=None,modo='sincrono'):
        if not self._lock.acquire(blocking=False):raise RuntimeError('Ciclo já está em execução.')
        salvo=None
        try:
            salvo=copy.deepcopy({k:v for k,v in self.__dict__.items() if k!='_lock'})
            return self._passo(a,b,formulas,modo)
        except BaseException:
            if salvo is not None:
                lock=self._lock;self.__dict__.clear();self.__dict__.update(salvo);self._lock=lock
            raise
        finally:self._lock.release()
    def _passo(self,a,b,formulas,modo):
        if modo not in ('sincrono','assincrono') or self.ciclo>=1000:raise ValueError('Modo/orçamento inválido.')
        for valor in (a,b):
            if valor is not None and (type(valor) not in (bool,int) or valor not in (0,1)):raise ValueError('Observação deve ser bit ou None.')
        logica=analisar(formulas,4096) if formulas is not None else None
        if not self.recorrencia:
            for estado in self.modulos.values():estado['cache']={};estado['ultimo']=None
        snapshot=copy.deepcopy(dict(modulos=self.modulos,energia=self.energia,atencao=self.atencao))
        entrada=dict(a=a,b=b,logica=logica)
        if modo=='assincrono':
            with ThreadPoolExecutor(max_workers=len(MODULOS)) as executor:propostas=list(executor.map(lambda m:self._propor(m,entrada,snapshot),MODULOS))
        else:propostas=[self._propor(m,entrada,snapshot) for m in MODULOS]
        candidatos=[p for p in propostas if p is not None]
        for m,p in zip(MODULOS,propostas):
            if p is not None:self._validar_fragmento(p,m,entrada,snapshot)
        vencedor,comparacoes=self._torneio(candidatos);prev=self.atencao.copy();indice=MODULOS.index(vencedor.modulo)
        brier=sum((int(i==indice)-p)**2 for i,p in enumerate(prev))
        destinos=MODULOS if self.difusao else (vencedor.modulo,)
        self._difundir(vencedor,destinos);self.stm=vencedor;self.ciclo+=1
        energia_antes=self.energia
        self.energia=min(1.,self.energia+.15) if vencedor.modulo=='homeostase' else max(0.,self.energia-.02)
        if self.atencao_adaptativa:self.atencao=[.8*p+.2*int(i==indice) for i,p in enumerate(prev)]
        r=dict(ciclo=self.ciclo,fragmento=dict(modulo=vencedor.modulo,origem=vencedor.origem,conteudo=list(vencedor.conteudo)),
            candidatos=len(candidatos),comparacoes=comparacoes,stm_chunks=1,destinos=list(destinos),energia_antes=energia_antes,energia_depois=self.energia,
            atencao_previa=prev,brier_atencao_pre_update=brier,logica=logica,
            proveniencias_propostas=[p.origem for p in candidatos],consciencia_subjetiva='nao_avaliada')
        self.historico.append(r);return r
    def responder(self):
        cache=self.modulos['previsao']['cache']
        return int(cache['a'])^int(cache['b']) if set(cache)=={'a','b'} else None


def experimento(semente=73001,casos=64):
    if type(semente) is not int or not 0<=semente<2**32 or type(casos) is not int or not 1<=casos<=256:raise ValueError('Orçamento inválido.')
    rng=random.Random(semente);tarefas=[(rng.randrange(2),rng.randrange(2)) for _ in range(casos)]
    variantes={'completo_sincrono':(True,True,'sincrono'),'completo_assincrono':(True,True,'assincrono'),'sem_recorrencia':(False,True,'sincrono'),'sem_difusao':(True,False,'sincrono')}
    resultados={};tracos={}
    for nome,(rec,dif,modo) in variantes.items():
        acertos=0;validas=0;logicos=0;historicos=[]
        for a,b in tarefas:
            w=WorkspaceGlobal(rec,dif)
            h=[w.passo(a=a,modo=modo),w.passo(b=b,modo=modo),w.passo(formulas=instancia(0)['formulas'],modo=modo),w.passo(modo=modo)]
            resposta=w.responder();validas+=int(resposta is not None);acertos+=int(resposta is not None and resposta==(a^b));logicos+=int(h[2]['logica']['status']=='UNSAT')
            historicos.append(h)
        resultados[nome]=dict(casos=casos,respostas_emitidas=validas,acertos=acertos,taxa_acerto=acertos/casos,contradicoes_diagnosticadas=logicos)
        tracos[nome]=historicos
    w=WorkspaceGlobal(energia=.3);h=[w.passo(a=i%2) for i in range(64)]
    return dict(versao=VERSAO,semente=semente,resumo=resultados,igualdade_sync_async=tracos['completo_sincrono']==tracos['completo_assincrono'],
        exemplo=tracos['completo_sincrono'][0],homeostase=dict(ciclos=64,descansos=sum(t['fragmento']['modulo']=='homeostase' for t in h),energia_min=min(t['energia_depois'] for t in h),energia_final=w.energia),
        capacidades=dict(modulos=len(MODULOS),gargalo_chunks=1,dimensao_fragmento_max=2,memoria_historico_max=128,proveniencia='metadado explícito, não classificação fenomenal'),
        limites=['Ablações em tarefa artificial de dois bits; não detecção ou produção de consciência.',
        'Monitor de atenção aprende frequências recentes; Brier não certifica calibração.',
        'Homeostase é variável simulada, não metabolismo ou experiência corporal.',
        'Sem cálculo IIT/Phi; sem implementação fiel de CTM/LIDA ou teste ACT validado.',
        'Paradoxos são AST proposicionais finitas; diagnóstico não resolve indecidibilidade.'])

def main(args=None):
    import json
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--semente',type=int,default=73001);p.add_argument('--casos',type=int,default=64);p.add_argument('--saida',type=Path)
    a=p.parse_args(args);r=experimento(a.semente,a.casos)
    if a.saida:escrever_json(a.saida,r)
    print(json.dumps(dict(resumo=r['resumo'],igualdade_sync_async=r['igualdade_sync_async'],homeostase=r['homeostase']),ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
