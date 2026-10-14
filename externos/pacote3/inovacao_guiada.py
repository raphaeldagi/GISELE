"""Laboratório de hipóteses, intervenções isoladas e confirmação com conservação.

Novo mecanismo do projeto com técnicas numéricas conhecidas. Não demonstra
novidade científica, cognição geral ou AGI/ASI; não gera código para eval/exec.
"""
from dataclasses import dataclass,replace
from pathlib import Path
import argparse
import json
import math

import numpy as np
from recursiva_paraconsistente import GeometriaRestrita,MotorEvidencias,MetaProbabilidade
from transferencia_metacognitiva import (
    Configuracao,gerar_tarefas,inteiro,hash_json,contexto_gradiente,
    auditoria_dez,resumo,comparacao_pareada,
)


@dataclass(frozen=True)
class Intervencao:
    tipo:str='identidade'
    valor:float=0.

    def __post_init__(self):
        if self.tipo not in ('identidade','limite_tangente','secante','media_gradiente'):
            raise ValueError('Operador fora da gramática.')
        intervalos={'identidade':(0.,0.),'limite_tangente':(.1,1.),'secante':(.1,1.),'media_gradiente':(.1,.9)}
        a,b=intervalos[self.tipo]
        if not isinstance(self.valor,(int,float)) or isinstance(self.valor,bool) or not math.isfinite(self.valor) or not a<=self.valor<=b:
            raise ValueError('Parâmetro de intervenção inválido.')

    def dados(self):return dict(tipo=self.tipo,valor=self.valor)
    @property
    def checksum(self):return hash_json(self.dados())


def passo_secante(x,g,x_anterior,g_anterior,fallback,fator=.8):
    if x_anterior is None:return fallback,False
    s=x-x_anterior;y=g-g_anterior;ss=float(s@s);sy=float(s@y)
    if not math.isfinite(ss) or not math.isfinite(sy) or ss<=1e-12 or sy<=1e-10:return fallback,False
    return float(np.clip(fator*ss/sy,.002,.4)),True


def executar(tarefa,configuracao,intervencao=Intervencao(),orcamento=24,detalhes=False):
    """Mesmo retrocesso da referência, com um operador adicional declarativo."""
    inteiro(orcamento,'Orçamento',4,64)
    if not configuracao.adaptativa or configuracao.acoplamento_meta:raise ValueError('Referência deve usar retrocesso simples.')
    geo=GeometriaRestrita(len(tarefa.inicial));x=tarefa.inicial.copy();anterior=x.copy()
    custo=tarefa.custo(x);inicial=custo;passo=configuracao.passo;delta=configuracao.ruido
    ponto_obs=None;grad_obs=None;media=None;meta=MetaProbabilidade();tracos=[];aceitas=0
    motivos={c:0 for c in ('aceita','conflito','custo','deslocamento','restricao')}
    for tentativa in range(1,orcamento+1):
        antes=x.copy();custo_antes=custo
        g=tarefa.gradiente(x)+tarefa.sigma_gradiente*tarefa.ruido(tentativa,101).normal(size=geo.dim)
        estimativa,secante_valida=passo_secante(x,g,ponto_obs,grad_obs,passo)
        repeticao=bool(ponto_obs is not None and np.linalg.norm(x-ponto_obs)<=1e-12)
        variacao=float(np.linalg.norm(g-grad_obs)) if repeticao else 0.
        efetivo=passo;direcao=g.copy()
        if intervencao.tipo=='secante':efetivo,_=passo_secante(x,g,ponto_obs,grad_obs,passo,intervencao.valor)
        elif intervencao.tipo=='media_gradiente':
            media=g.copy() if media is None else intervencao.valor*g+(1-intervencao.valor)*media
            direcao=media
        perturbacao=delta*tarefa.ruido(tentativa,102).normal(size=geo.dim)
        deslocamento_tangente=-efetivo*geo.tangente(x)@(direcao+perturbacao)
        norma_original=float(np.linalg.norm(deslocamento_tangente));limitado=False
        if intervencao.tipo=='limite_tangente' and norma_original>intervencao.valor:
            deslocamento_tangente*=intervencao.valor/norma_original;limitado=True
        candidata=geo.retrair(x+deslocamento_tangente);proposto=tarefa.custo(candidata)
        residuo=float(np.max(np.abs(geo.residuos(candidata))));deslocamento=float(np.linalg.norm(candidata-x))
        conflito=bool(tarefa.ruido(tentativa,103).random()<tarefa.chance_conflito)
        logica=MotorEvidencias();logica.anotar('admissivel','geometria',float(residuo<=1e-9),float(residuo>1e-9))
        if conflito:logica.anotar('admissivel','oposicao_sintetica',0.,1.)
        avaliacao=logica.avaliar('admissivel')
        motivo=('conflito' if avaliacao['estado']=='ambos' else 'restricao' if residuo>1e-9 else
            'deslocamento' if deslocamento>1. else 'custo' if proposto>custo+1e-12 else 'aceita')
        aceita=motivo=='aceita'
        if aceita:x=candidata;custo=proposto;aceitas+=1
        ganho=custo_antes-custo;h=geo.score_harmonico(antes,anterior)
        meta.registrar(tentativa,bool(aceita and ganho>1e-6*max(inicial,1e-12)))
        delta_usado=delta
        if motivo in ('custo','deslocamento','restricao'):passo=max(.002,passo*.5);delta*=.7
        elif motivo=='conflito':delta*=.7
        elif ganho>1e-3*max(custo_antes,1e-12):passo=min(.4,passo*1.06);delta*=.95
        else:delta=min(.1,delta+.002)
        motivos[motivo]+=1
        registro=dict(tentativa=tentativa,orientacao='versa' if tentativa%2 else 'reversa',
            contexto=contexto_gradiente(g,custo_antes),passo_usado=efetivo,ruido_usado=delta_usado,
            aceita=aceita,motivo=motivo,custo_antes=custo_antes,custo_proposto=proposto,custo=custo,
            residuo=residuo,deslocamento=deslocamento,harmonico=h,logica=avaliacao,
            norma_tangente_original=norma_original,clipping_aplicado=limitado,
            secante_valida=secante_valida,passo_secante_diagnostico=estimativa,
            mesmo_estado_observado=repeticao,variacao_gradiente_mesmo_estado=variacao,
            estado_observado=antes.tolist(),gradiente_observado=g.tolist())
        if detalhes:tracos.append(registro)
        ponto_obs=antes;grad_obs=g.copy();anterior=antes
    return dict(id=tarefa.id,fase=tarefa.fase,familia=tarefa.familia,custo_inicial=inicial,custo_final=custo,
        razao_custo=custo/max(inicial,1e-12),sucesso=bool(custo<=.01*max(inicial,1e-12)),
        tentativas=orcamento,avaliacoes_objetivo=orcamento+1,avaliacoes_gradiente=orcamento,
        aceitas=aceitas,motivos=motivos,estado_final=x.tolist(),
        residuo_final=float(np.max(np.abs(geo.residuos(x)))),observacoes_locais=len(meta.ids),tracos=tracos,
        auditoria_final=auditoria_dez(registro,meta.modelo_aninhado()) if detalhes else None)


def avaliar(tarefas,configuracao,intervencao,orcamento,detalhes=False):
    return [executar(t,configuracao,intervencao,orcamento,detalhes) for t in tarefas]


def diagnosticar(resultados):
    if not resultados or any(r['fase']!='treino' or not r['tracos'] for r in resultados):
        raise ValueError('Diagnóstico exige trajetórias de treino.')
    tracos=[e for r in resultados for e in r['tracos']]
    return dict(fase='treino',fontes=tuple(r['id'] for r in resultados),eventos=len(tracos),
        rejeicoes_deslocamento=sum(e['motivo']=='deslocamento' for e in tracos),
        rejeicoes_custo=sum(e['motivo']=='custo' for e in tracos),
        secantes_validas=sum(e['secante_valida'] for e in tracos),
        variacoes_mesmo_estado=sum(e['mesmo_estado_observado'] and e['variacao_gradiente_mesmo_estado']>.15 for e in tracos),
        metacognicao_sem_novas_observacoes=True)


def gerar_hipoteses(diagnostico):
    if diagnostico.get('fase')!='treino':raise ValueError('Hipóteses só usam diagnóstico de treino.')
    definicoes=[
        ('limite_tangente',.7,diagnostico['rejeicoes_deslocamento']>=1,
         'Propostas grandes desperdiçam avaliações antes do retrocesso.',
         'Limitar a norma tangente a 0,7 preservando a direção.',
         'Sem melhora na seleção ou confirmação, o limite não é incorporado.'),
        ('secante',.8,diagnostico['rejeicoes_custo']>=3 and diagnostico['secantes_validas']>=3,
         'A escala do passo pode acompanhar melhor a curvatura observada.',
         'Usar 0,8(s·s)/(s·y), protegido, reutilizando gradientes.',
         'Custos maiores ou secantes sem fundamento refutam a utilidade desta configuração.'),
        ('media_gradiente',.6,diagnostico['variacoes_mesmo_estado']>=2,
         'Gradientes diferentes no mesmo estado sugerem instabilidade da observação.',
         'Usar média exponencial com peso 0,6 para o gradiente atual.',
         'O atraso da média pode superar o benefício; avaliar em tarefas distintas.')]
    hipoteses=[]
    for tipo,valor,ativa,hipotese,resposta,refutacao in definicoes:
        if ativa:
            op=Intervencao(tipo,valor)
            hipoteses.append(dict(hipotese=hipotese,pergunta='Que intervenção isolada testa esta hipótese?',
                resposta=resposta,refutacao=refutacao,intervencao=op.dados(),checksum=op.checksum,
                fontes=diagnostico['fontes'],diagnostico_checksum=hash_json(diagnostico)))
    return hipoteses


def gate_confirmacao(base,candidata):
    if not base or [r['id'] for r in base]!=[r['id'] for r in candidata]:raise ValueError('Confirmação pareada obrigatória.')
    if any(r['fase']!='confirmacao' for r in base+candidata):raise ValueError('Confirmação não pode usar seleção/teste.')
    diferencas=np.array([a['razao_custo']-b['razao_custo'] for a,b in zip(base,candidata)])
    minimo=max(1e-5,.05*resumo(base)['media_razao_custo'])
    pior_perda=float(max(0.,-np.min(diferencas)))
    invariantes=all(r['residuo_final']<=1e-9 and r['custo_final']<=r['custo_inicial']+1e-12 for r in candidata)
    ganho=float(np.mean(diferencas));aprovada=bool(invariantes and ganho>=minimo and pior_perda<=.02)
    return dict(aprovada=aprovada,ganho_medio=ganho,ganho_minimo=minimo,pior_perda=pior_perda,
        teto_perda=.02,invariantes=bool(invariantes),criterio_empirico_sem_certificacao_estatistica=True)


def colecoes(semente,dimensao,treino_n=12,selecao_n=8,confirmacao_n=12,teste_n=32,fora_n=16):
    conjuntos=dict(treino=gerar_tarefas('treino',treino_n,dimensao,semente),
        selecao=tuple(replace(t,fase='selecao',id=t.id.replace('validacao:','selecao:',1))
            for t in gerar_tarefas('validacao',selecao_n,dimensao,semente)),
        confirmacao=tuple(replace(t,fase='confirmacao',id=t.id.replace('validacao:','confirmacao:',1))
            for t in gerar_tarefas('validacao',confirmacao_n,dimensao,(semente+104729)%(2**32))),
        teste=gerar_tarefas('teste',teste_n,dimensao,semente),
        fora_faixa=gerar_tarefas('fora_faixa',fora_n,dimensao,semente))
    ids=[t.id for grupo in conjuntos.values() for t in grupo];chaves=[t.chave_aleatoria for grupo in conjuntos.values() for t in grupo]
    if len(set(ids))!=len(ids) or len(set(chaves))!=len(chaves):raise ValueError('Instâncias sobrepostas.')
    return conjuntos


def ajustar_referencia(treino,orcamento):
    if not treino or any(t.fase!='treino' for t in treino):raise ValueError('Ajuste só recebe treino.')
    tabela=[];opcoes=[]
    for passo in (.025,.05,.1,.2):
        for ruido in (0.,.04):
            c=Configuracao(passo,ruido,True,False)
            resultados=avaliar(treino,c,Intervencao(),orcamento);s=resumo(resultados)
            tabela.append(dict(configuracao=c.dados(),resultado=s));opcoes.append((s['media_razao_custo'],c.chave,c))
    return min(opcoes,key=lambda v:(v[0],v[1]))[2],tabela


def custos_fase(execucao):
    casos=[r for lote in execucao for r in lote]
    return dict(execucoes_tarefa=len(casos),avaliacoes_objetivo=sum(r['avaliacoes_objetivo'] for r in casos),
        avaliacoes_gradiente=sum(r['avaliacoes_gradiente'] for r in casos))


def protocolo(semente=59,dimensao=8,orcamento=24,treino_n=12,selecao_n=8,confirmacao_n=12,teste_n=32,fora_n=16):
    conjuntos=colecoes(semente,dimensao,treino_n,selecao_n,confirmacao_n,teste_n,fora_n)
    referencia,ajuste=ajustar_referencia(conjuntos['treino'],orcamento)
    rt=avaliar(conjuntos['treino'],referencia,Intervencao(),orcamento,True)
    diagnostico=diagnosticar(rt);hipoteses=gerar_hipoteses(diagnostico)
    congelamento=hash_json(dict(referencia=referencia.dados(),hipoteses=hipoteses))
    rs=avaliar(conjuntos['selecao'],referencia,Intervencao(),orcamento);lotes_selecao=[rs];tabela=[];melhor=None
    for h in hipoteses:
        op=Intervencao(**h['intervencao']);r=avaliar(conjuntos['selecao'],referencia,op,orcamento)
        lotes_selecao.append(r);escore=resumo(r)['media_razao_custo']
        tabela.append(dict(intervencao=op.dados(),resultado=resumo(r),diferencas=comparacao_pareada(rs,r,semente),casos=r))
        if melhor is None or (escore,op.checksum)<(melhor[0],melhor[1]):melhor=(escore,op.checksum,op)
    vencedora=melhor[2] if melhor and melhor[0]<resumo(rs)['media_razao_custo']-1e-8 else None
    rb=avaliar(conjuntos['confirmacao'],referencia,Intervencao(),orcamento);lotes_conf=[rb]
    if vencedora is not None:
        rc=avaliar(conjuntos['confirmacao'],referencia,vencedora,orcamento);lotes_conf.append(rc)
        confirmacao=gate_confirmacao(rb,rc)
    else:
        rc=[];confirmacao=dict(aprovada=False,motivo='Nenhuma candidata melhorou a seleção; conservar referência.')
    incorporada=vencedora if confirmacao['aprovada'] else Intervencao()
    decisao_checksum=hash_json(dict(referencia=referencia.dados(),intervencao=incorporada.dados(),confirmacao=confirmacao))
    testes={};contabilidade={}
    for fase in ('teste','fora_faixa'):
        a=avaliar(conjuntos[fase],referencia,Intervencao(),orcamento)
        b=avaliar(conjuntos[fase],referencia,incorporada,orcamento,False)
        testes[fase]=dict(referencia=resumo(a),incorporada=resumo(b),comparacao=comparacao_pareada(a,b,semente),
            casos=dict(referencia=a,incorporada=b))
        contabilidade[fase]=custos_fase([a,b])
    if congelamento!=hash_json(dict(referencia=referencia.dados(),hipoteses=hipoteses)) or decisao_checksum!=hash_json(
        dict(referencia=referencia.dados(),intervencao=incorporada.dados(),confirmacao=confirmacao)):
        raise RuntimeError('Especificação alterada após congelamento.')
    contabilidade['ajuste_treino']=dict(execucoes_tarefa=sum(e['resultado']['tarefas'] for e in ajuste),
        avaliacoes_objetivo=sum(e['resultado']['avaliacoes_objetivo'] for e in ajuste),
        avaliacoes_gradiente=sum(e['resultado']['avaliacoes_gradiente'] for e in ajuste))
    contabilidade['diagnostico_treino']=custos_fase([rt]);contabilidade['selecao']=custos_fase(lotes_selecao)
    contabilidade['confirmacao']=custos_fase(lotes_conf)
    return dict(natureza='laboratório de inovação guiada por falhas; não AGI/ASI',semente=semente,dimensao=dimensao,
        orcamento=orcamento,referencia=referencia.dados(),diagnostico=diagnostico,hipoteses=hipoteses,
        congelamento_checksum=congelamento,ajuste=ajuste,selecao=tabela,
        referencia_selecao=dict(resultado=resumo(rs),casos=rs),
        casos_confirmacao=dict(referencia=rb,candidata=rc),
        candidata_selecionada=vencedora.dados() if vencedora else None,confirmacao=confirmacao,
        intervencao_incorporada=incorporada.dados(),decisao_checksum=decisao_checksum,
        parametros_inalterados_no_teste=True,resultados=testes,contabilidade=contabilidade,
        diagnostico_exemplos=[r for r in rt if any(e['motivo']!='aceita' for e in r['tracos'])][:3],
        manifesto={fase:[dict(id=t.id,chave=t.chave_aleatoria,
            dados_checksum=hash_json(dict(h=t.h.tolist(),alvo=t.alvo.tolist(),inicial=t.inicial.tolist()))) for t in grupo]
            for fase,grupo in conjuntos.items()},
        limites=['Hipóteses instanciadas por regras de diagnóstico, não invenção científica irrestrita.',
            'Clipping, passo secante protegido e EMA são técnicas conhecidas, novas nesta integração.',
            'Comparações contrafactuais repetem a tarefa/ruído; estados divergem conforme as intervenções.',
            'Gate empírico de uma vencedora, sem garantia de generalização ou prova formal.',
            'Seleção e confirmação podem rejeitar todas as propostas; não se tenta a segunda na confirmação.',
            'Custos de investigação são adicionais e explicitados; consultas do teste são iguais por política.',
            'Objetivos e verificadores do simulador são confiáveis; sem cognição plena ou AGI/ASI.'])


def salvar_artefato(caminho,resultado):
    dados=dict(formato=1,referencia=resultado['referencia'],intervencao=resultado['intervencao_incorporada'],
        origem=dict(semente=resultado['semente'],decisao_checksum=resultado['decisao_checksum']))
    artefato=dict(dados=dados,checksum=hash_json(dados))
    Path(caminho).write_text(json.dumps(artefato,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def carregar_artefato(caminho):
    with Path(caminho).open('rb') as f:conteudo=f.read(65537)
    if len(conteudo)>65536:raise ValueError('Artefato excede orçamento.')
    obj=json.loads(conteudo)
    if not isinstance(obj,dict) or set(obj)!= {'dados','checksum'} or not isinstance(obj['dados'],dict):
        raise ValueError('Envelope malformado.')
    dados=obj['dados']
    if obj['checksum']!=hash_json(dados) or set(dados)!= {'formato','referencia','intervencao','origem'} or type(dados['formato']) is not int or dados['formato']!=1:
        raise ValueError('Formato/checksum inválido.')
    if not all(isinstance(dados[n],dict) for n in ('referencia','intervencao','origem')) or set(dados['referencia'])!= {'passo','ruido','adaptativa','acoplamento_meta'} or set(dados['intervencao'])!= {'tipo','valor'} or set(dados['origem'])!= {'semente','decisao_checksum'}:
        raise ValueError('Especificação malformada.')
    inteiro(dados['origem']['semente'],'Semente',0,2**32-1)
    checksum=dados['origem']['decisao_checksum']
    if not isinstance(checksum,str) or len(checksum)!=64 or any(c not in '0123456789abcdef' for c in checksum):
        raise ValueError('Identificador de decisão inválido.')
    c=Configuracao(**dados['referencia']);op=Intervencao(**dados['intervencao'])
    if not c.adaptativa or c.acoplamento_meta:raise ValueError('Referência incompatível.')
    return c,op


def main(args=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--semente',type=int,default=59);p.add_argument('--dimensao',type=int,default=8)
    p.add_argument('--orcamento',type=int,default=24);p.add_argument('--saida',type=Path);p.add_argument('--artefato',type=Path)
    a=p.parse_args(args);r=protocolo(a.semente,a.dimensao,a.orcamento)
    if a.artefato:salvar_artefato(a.artefato,r)
    texto=json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)
    if a.saida:a.saida.write_text(texto+'\n',encoding='utf-8')
    print(texto);return 0


if __name__=='__main__':raise SystemExit(main())
