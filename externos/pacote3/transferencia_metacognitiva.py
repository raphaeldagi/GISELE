"""Transferência limitada de controle: quadráticas, memória congelada e avaliação pareada.

Não é um LLM nem AGI/ASI. Gradientes e verificadores pertencem a um simulador
confiável. O teste permanece separado da escolha dos parâmetros.
"""
from dataclasses import dataclass
from pathlib import Path
import argparse
import hashlib
import json
import math

import numpy as np
from recursiva_paraconsistente import GeometriaRestrita,MotorEvidencias,MetaProbabilidade,revisar_observacao


FAMILIAS=('suave','anisotropica','rigida','ruidosa')
FASES={'treino':1,'validacao':2,'teste':3,'fora_faixa':4}
CONTEXTOS=('baixo','medio','alto')


def hash_json(objeto):
    return hashlib.sha256(json.dumps(objeto,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def inteiro(valor,nome,minimo,maximo):
    if type(valor) is not int or not minimo<=valor<=maximo:raise ValueError(f'{nome} fora do orçamento.')
    return valor


@dataclass(frozen=True)
class Configuracao:
    passo:float
    ruido:float
    adaptativa:bool
    acoplamento_meta:bool=True

    def __post_init__(self):
        if (not isinstance(self.passo,(int,float)) or isinstance(self.passo,bool) or
            not math.isfinite(self.passo) or not .005<=self.passo<=.4 or
            not isinstance(self.ruido,(int,float)) or isinstance(self.ruido,bool) or
            not math.isfinite(self.ruido) or not 0<=self.ruido<=.1 or type(self.adaptativa) is not bool or
            type(self.acoplamento_meta) is not bool):
            raise ValueError('Configuração inválida.')

    def dados(self):return dict(passo=self.passo,ruido=self.ruido,adaptativa=self.adaptativa,acoplamento_meta=self.acoplamento_meta)
    @property
    def chave(self):return hash_json(self.dados())


@dataclass(frozen=True)
class Tarefa:
    id:str
    fase:str
    familia:str
    chave_aleatoria:tuple
    h:np.ndarray
    alvo:np.ndarray
    inicial:np.ndarray
    sigma_gradiente:float
    chance_conflito:float

    def custo(self,x):
        d=x-self.alvo;return float(d@self.h@d)
    def gradiente(self,x):return 2*self.h@(x-self.alvo)
    def ruido(self,tentativa,dominio):
        inteiro(tentativa,'Tentativa',1,64);inteiro(dominio,'Domínio',100,199)
        return np.random.default_rng(np.random.SeedSequence([*self.chave_aleatoria,tentativa,dominio]))


def gerar_tarefas(fase,quantidade=12,dimensao=8,semente=31):
    if fase not in FASES:raise ValueError('Fase inválida.')
    inteiro(quantidade,'Quantidade',4,128);inteiro(dimensao,'Dimensão',3,32);inteiro(semente,'Semente',0,2**32-1)
    if quantidade%4:raise ValueError('Quantidade deve ser múltipla de quatro para balancear famílias.')
    geo=GeometriaRestrita(dimensao);tarefas=[]
    for i in range(quantidade):
        familia=FAMILIAS[i%4];chave=(semente,FASES[fase],i)
        rng=np.random.default_rng(np.random.SeedSequence([*chave,91]))
        cond,escala,sigma,conflito={
            'suave':(1.,1.,0.,0.),'anisotropica':(8.,3.,0.,0.),
            'rigida':(32.,12.,0.,0.),'ruidosa':(8.,3.,.2,.1)}[familia]
        if fase=='fora_faixa':cond*=4;escala*=2;sigma+=.15
        q=np.linalg.qr(rng.normal(size=(dimensao,dimensao)))[0]
        espectro=np.geomspace(escala/cond,escala,dimensao)
        h=(q*espectro)@q.T;alvo=geo.retrair(rng.normal(size=dimensao));inicial=geo.retrair(rng.normal(size=dimensao))
        for a in (h,alvo,inicial):a.setflags(write=False)
        tarefas.append(Tarefa(f'{fase}:{semente}:{dimensao}:{i}',fase,familia,chave,h,alvo,inicial,sigma,conflito))
    return tuple(tarefas)


@dataclass(frozen=True)
class MemoriaCongelada:
    # (contexto, tentativas sem conflito, rejeições numéricas), fontes somente treino.
    contagens:tuple
    fontes:tuple
    configuracao:str

    def dados(self):return dict(contagens=self.contagens,fontes=self.fontes,configuracao=self.configuracao,fase='treino')
    @property
    def checksum(self):return hash_json(self.dados())
    def fator(self,contexto):
        for c,n,r in self.contagens:
            if c==contexto and n>=8:return 1-.6*(r+1)/(n+2)
        return 1.


class MemoriaFalhas:
    def __init__(self,configuracao):
        self.configuracao=configuracao.chave;self.contagens={c:[0,0] for c in CONTEXTOS}
        self.fontes=set();self.eventos=set()

    def registrar(self,tarefa,tentativa,contexto,motivo):
        if tarefa.fase!='treino':raise ValueError('Memória global só recebe tarefas de treino.')
        if contexto not in CONTEXTOS or motivo not in ('aceita','conflito','custo','deslocamento','restricao'):
            raise ValueError('Diagnóstico inválido.')
        evento=(tarefa.id,tentativa)
        if evento in self.eventos:raise ValueError('Resultado já registrado.')
        self.eventos.add(evento);self.fontes.add(tarefa.id)
        if motivo!='conflito':
            self.contagens[contexto][0]+=1;self.contagens[contexto][1]+=int(motivo!='aceita')

    def congelar(self):
        return MemoriaCongelada(tuple((c,*self.contagens[c]) for c in CONTEXTOS),tuple(sorted(self.fontes)),self.configuracao)


def contexto_gradiente(gradiente,custo):
    razao=float(np.linalg.norm(gradiente)/math.sqrt(max(custo,1e-12)))
    return 'baixo' if razao<3 else ('medio' if razao<6 else 'alto')


def auditoria_dez(registro,probabilidade):
    dados=[('percepcao',dict(contexto=registro['contexto'])),
        ('direcao',registro['harmonico']),('pragmatica',dict(passo=registro['passo_usado'])),
        ('axiomas',dict(residuo=registro['residuo'])),('probabilidade',probabilidade),
        ('metacognicao',dict(motivo=registro['motivo'])),('dissonancia',registro['logica']),
        ('variabilidade',dict(ruido=registro['ruido_usado'])),
        ('escrutinio',dict(aceita=registro['aceita'])),('integracao',dict(custo=registro['custo']))]
    node=None
    for i,(operacao,resultado) in enumerate(dados,1):
        coerente=revisar_observacao(node)
        json.dumps(resultado,allow_nan=False)
        node=dict(nivel=i,operacao=operacao,resultado=resultado,observa=node,hash_entrada=hash_json(node),evidencia_nova=False,
            juizo_metacognitivo=dict(coerente=coerente,revisa_nivel_anterior=i-1,
                probabilidade_monitorada=probabilidade,evento_usado_uma_vez=registro['tentativa']))
    if not revisar_observacao(node):raise RuntimeError('Auditoria recursiva inconsistente.')
    return node


def executar_tarefa(tarefa,configuracao,orcamento=24,memoria=None,coletor=None,detalhes=False):
    inteiro(orcamento,'Orçamento',4,64)
    if memoria is not None and (not configuracao.adaptativa or not configuracao.acoplamento_meta or memoria.configuracao!=configuracao.chave):
        raise ValueError('Memória incompatível com a configuração.')
    if coletor is not None and (tarefa.fase!='treino' or coletor.configuracao!=configuracao.chave):
        raise ValueError('Coletor de treino incompatível.')
    geo=GeometriaRestrita(len(tarefa.alvo));x=tarefa.inicial.copy();anterior=x.copy()
    inicial=tarefa.custo(x);custo=inicial;passo=configuracao.passo;delta=configuracao.ruido
    meta=MetaProbabilidade();tracos=[];aceitas=0;motivos={c:0 for c in ('aceita','conflito','custo','deslocamento','restricao')}
    for tentativa in range(1,orcamento+1):
        # As coordenadas exógenas avançam por tentativa, inclusive após rejeição.
        grad=tarefa.gradiente(x)+tarefa.sigma_gradiente*tarefa.ruido(tentativa,101).normal(size=geo.dim)
        contexto=contexto_gradiente(grad,custo)
        if tentativa==1 and memoria is not None:passo*=memoria.fator(contexto)
        passo_usado=passo;delta_usado=delta;antes=x.copy();custo_antes=custo
        h=geo.score_harmonico(x,anterior);tangente=geo.tangente(x)
        perturbacao=delta*tarefa.ruido(tentativa,102).normal(size=geo.dim)
        candidata=geo.retrair(x-passo*tangente@(grad+perturbacao));proposto=tarefa.custo(candidata)
        residuo=float(np.max(np.abs(geo.residuos(candidata))));deslocamento=float(np.linalg.norm(candidata-x))
        conflito=bool(tarefa.ruido(tentativa,103).random()<tarefa.chance_conflito)
        logica=MotorEvidencias();logica.anotar('admissivel','geometria',float(residuo<=1e-9),float(residuo>1e-9))
        if conflito:logica.anotar('admissivel','oposicao_sintetica',0.,1.)
        avaliacao=logica.avaliar('admissivel')
        motivo=('conflito' if avaliacao['estado']=='ambos' else 'restricao' if residuo>1e-9 else
            'deslocamento' if deslocamento>1. else 'custo' if proposto>custo+1e-12 else 'aceita')
        aceita=motivo=='aceita'
        if aceita:x=candidata;custo=proposto;aceitas+=1
        anterior=antes;ganho=custo_antes-custo
        meta.registrar(tentativa,bool(aceita and ganho>1e-6*max(inicial,1e-12)))
        if coletor is not None:coletor.registrar(tarefa,tentativa,contexto,motivo)
        if configuracao.adaptativa:
            if motivo in ('custo','deslocamento','restricao'):passo=max(.002,passo*.5);delta*=.7
            elif motivo=='conflito':delta*=.7  # conflito de fonte não mede curvatura.
            elif ganho>1e-3*max(custo_antes,1e-12):
                acoplamento=.8+.4*meta.media if configuracao.acoplamento_meta else 1.
                direcao=.97+.03*max(0.,h['cosseno']) if configuracao.acoplamento_meta else 1.
                passo=min(.4,passo*1.06*acoplamento*direcao);delta*=.95
            else:delta=min(.1,delta+.002)
        motivos[motivo]+=1
        registro=dict(tentativa=tentativa,orientacao='versa' if tentativa%2 else 'reversa',
            contexto=contexto,passo_usado=passo_usado,ruido_usado=delta_usado,aceita=aceita,motivo=motivo,
            custo_antes=custo_antes,custo_proposto=proposto,custo=custo,residuo=residuo,deslocamento=deslocamento,
            harmonico=h,logica=avaliacao,passo_proximo=passo,ruido_proximo=delta,
            taxa_melhoria_heuristica=meta.media)
        if detalhes:tracos.append(registro)
    ratio=custo/max(inicial,1e-12)
    return dict(id=tarefa.id,fase=tarefa.fase,familia=tarefa.familia,custo_inicial=inicial,custo_final=custo,
        razao_custo=ratio,sucesso=bool(ratio<=.01),tentativas=orcamento,
        avaliacoes_objetivo=orcamento+1,avaliacoes_gradiente=orcamento,aceitas=aceitas,motivos=motivos,
        estado_final=x.tolist(),residuo_final=float(np.max(np.abs(geo.residuos(x)))),
        observacoes_locais=len(meta.ids),tracos=tracos,
        auditoria_final=auditoria_dez(registro,meta.modelo_aninhado()) if detalhes else None)


def avaliar(tarefas,configuracao,orcamento,memoria=None,coletor=None,detalhes_primeiro=False):
    return [executar_tarefa(t,configuracao,orcamento,memoria,coletor,detalhes_primeiro and i==0) for i,t in enumerate(tarefas)]


def resumo(resultados):
    razoes=np.array([r['razao_custo'] for r in resultados])
    return dict(tarefas=len(resultados),media_razao_custo=float(np.mean(razoes)),
        mediana_razao_custo=float(np.median(razoes)),max_razao_custo=float(np.max(razoes)),
        taxa_sucesso=float(np.mean([r['sucesso'] for r in resultados])),
        avaliacoes_objetivo=sum(r['avaliacoes_objetivo'] for r in resultados),
        avaliacoes_gradiente=sum(r['avaliacoes_gradiente'] for r in resultados))


def comparacao_pareada(base,meta,semente=31):
    if not base or [r['id'] for r in base]!=[r['id'] for r in meta]:raise ValueError('Pareamento de tarefas obrigatório.')
    diferencas=np.array([b['razao_custo']-m['razao_custo'] for b,m in zip(base,meta)])
    grupos=[np.array([i for i,r in enumerate(base) if r['familia']==f]) for f in FAMILIAS]
    rng=np.random.default_rng(np.random.SeedSequence([semente,511]));medias=[]
    for _ in range(1200):
        indices=np.concatenate([rng.choice(g,size=len(g),replace=True) for g in grupos if len(g)])
        medias.append(float(np.mean(diferencas[indices])))
    return dict(unidade_amostral='tarefa; ciclos internos não são amostras independentes',
        sinal='positivo favorece a segunda política',media_diferenca=float(np.mean(diferencas)),
        mediana_diferenca=float(np.median(diferencas)),ganhos=int(np.sum(diferencas>1e-12)),
        perdas=int(np.sum(diferencas< -1e-12)),empates=int(np.sum(np.abs(diferencas)<=1e-12)),
        bootstrap_estratificado_95=np.quantile(medias,[.025,.975]).tolist(),
        bootstrap_replicas=1200,intervalo_descritivo_sem_garantia_universal=True,
        diferencas_pareadas=diferencas.tolist())


def selecionar(treino,validacao,orcamento,adaptativa,acoplamento_meta=True):
    if not treino or not validacao or any(t.fase!='treino' for t in treino) or any(t.fase!='validacao' for t in validacao):
        raise ValueError('Fases de seleção inválidas; teste não pode selecionar.')
    if set(t.id for t in treino)&set(t.id for t in validacao):raise ValueError('Instâncias sobrepostas.')
    registros=[];opcoes=[]
    for passo in (.025,.05,.1,.2):
        for ruido in (0.,.04):
            c=Configuracao(passo,ruido,adaptativa,acoplamento_meta);coletor=MemoriaFalhas(c) if adaptativa and acoplamento_meta else None
            rt=avaliar(treino,c,orcamento,coletor=coletor)
            memoria=coletor.congelar() if coletor else None
            rv=avaliar(validacao,c,orcamento,memoria)
            st=resumo(rt);sv=resumo(rv)
            registros.append(dict(configuracao=c.dados(),treino=st,validacao=sv,
                memoria_checksum=memoria.checksum if memoria else None))
            opcoes.append((sv['media_razao_custo'],c.chave,c,memoria))
    _,_,escolhida,memoria=min(opcoes,key=lambda x:(x[0],x[1]))
    return escolhida,memoria,registros


def protocolo(semente=31,dimensao=8,orcamento=24,treino_n=12,validacao_n=8,teste_n=32,fora_n=16):
    conjuntos={fase:gerar_tarefas(fase,n,dimensao,semente) for fase,n in
        [('treino',treino_n),('validacao',validacao_n),('teste',teste_n),('fora_faixa',fora_n)]}
    fixa,_,rf=selecionar(conjuntos['treino'],conjuntos['validacao'],orcamento,False,False)
    meta,memoria,rm=selecionar(conjuntos['treino'],conjuntos['validacao'],orcamento,True)
    retrocesso,_,rr=selecionar(conjuntos['treino'],conjuntos['validacao'],orcamento,True,False)
    congelamento=hash_json(dict(fixa=fixa.dados(),meta=meta.dados(),retrocesso=retrocesso.dados(),memoria=memoria.dados()))
    grupos={}
    for fase in ('teste','fora_faixa'):
        tarefas=conjuntos[fase]
        a=avaliar(tarefas,fixa,orcamento);b=avaliar(tarefas,meta,orcamento,memoria,detalhes_primeiro=fase=='teste')
        sem=avaliar(tarefas,meta,orcamento,None)
        classica=avaliar(tarefas,retrocesso,orcamento)
        grupos[fase]=dict(fixa=resumo(a),meta=resumo(b),meta_sem_memoria=resumo(sem),retrocesso=resumo(classica),
            fixa_vs_meta=comparacao_pareada(a,b,semente),
            retrocesso_vs_meta=comparacao_pareada(classica,b,semente),
            sem_memoria_vs_memoria=comparacao_pareada(sem,b,semente),
            por_familia={f:dict(fixa=resumo([r for r in a if r['familia']==f]),
                meta=resumo([r for r in b if r['familia']==f])) for f in FAMILIAS},
            casos=dict(fixa=a,meta=b,meta_sem_memoria=sem,retrocesso=classica))
    if congelamento!=hash_json(dict(fixa=fixa.dados(),meta=meta.dados(),retrocesso=retrocesso.dados(),memoria=memoria.dados())):
        raise RuntimeError('Parâmetros alterados durante o teste.')
    return dict(natureza='controle metacognitivo em quadráticas restritas; não AGI/ASI',
        semente=semente,dimensao=dimensao,orcamento_por_tarefa=orcamento,
        configuracoes=dict(fixa=fixa.dados(),meta=meta.dados(),retrocesso=retrocesso.dados()),memoria_treino=memoria.dados(),
        congelamento_checksum=congelamento,memoria_inalterada_no_teste=True,
        manifesto_instancias={f:[t.id for t in ts] for f,ts in conjuntos.items()},
        selecao=dict(fixa=rf,meta=rm,retrocesso=rr,configuracoes_por_politica=8,criterio='menor média de razão de custo na validação'),
        resultados=grupos,perguntas=[
            dict(orientacao='versa',pergunta='O que uma rejeição numérica ensina sobre a próxima tentativa?',
                resposta='Reduzir o passo local; agregar diagnósticos apenas no treino e congelar a memória antes do teste.'),
            dict(orientacao='reversa',pergunta='Que observação refutaria a utilidade da memória?',
                resposta='A política selecionada sem memória igualar ou superar o resultado com memória em tarefas reservadas.')],
        limites=['Objetivos sintéticos conhecidos, gradientes analíticos com ruído declarado e verificador confiável.',
            'Adaptação local reinicia em cada tarefa; não há aprendizagem global entre tarefas de teste.',
            'Teste de mesma distribuição usa novas instâncias; fora_faixa altera condicionamento, escala e ruído simultaneamente.',
            'Ablação sem memória conserva os parâmetros escolhidos para a política completa; não é seleção independente.',
            'Retrocesso é uma referência numérica simples, não um otimizador de estado da arte.',
            'Bootstrap descritivo por tarefa e família; não prova promoção geral, cognição plena ou AGI/ASI.'])


def main(args=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--semente',type=int,default=31);p.add_argument('--dimensao',type=int,default=8)
    p.add_argument('--orcamento',type=int,default=24);p.add_argument('--saida',type=Path)
    a=p.parse_args(args);r=protocolo(a.semente,a.dimensao,a.orcamento)
    texto=json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)
    if a.saida:a.saida.write_text(texto+'\n',encoding='utf-8')
    print(texto);return 0


if __name__=='__main__':raise SystemExit(main())
