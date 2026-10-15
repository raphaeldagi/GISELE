"""A indução reversa (Bellman) sobre uma árvore de decisão de duas ruas (Parte 107). Offline, só biblioteca padrão, exato
(sem simulação). Resolve a árvore DE TRÁS PARA FRENTE: o valor de uma decisão agora inclui o valor da decisão que ela
desbloqueia depois. É a SynthaiPlanejadora (P182/P93) feita EXATA por programação dinâmica. Só +, −, max e comparações —
nenhuma transcendental, portável por construção (Parte 52)."""

import itertools

ESTADOS = ("A", "B")
ACOES = (0, 1)

# MDP do teste: r[(s,a)] recompensa, T[(s,a)] estado seguinte.
MDP_TESTE = {
    "r": {("A", 0): 1.0, ("A", 1): 0.0, ("B", 0): 0.0, ("B", 1): 3.0},
    "T": {("A", 0): "A", ("A", 1): "B", ("B", 0): "A", ("B", 1): "B"},
}


def iteracao_valor(mdp, horizonte):
    """Indução reversa: V[0]=0; V[h][s] = maxₐ (r(s,a) + V[h-1][T(s,a)]). Devolve a lista [V0, V1, ..., V_horizonte]."""
    V = [{s: 0.0 for s in ESTADOS}]
    for _ in range(horizonte):
        Vant = V[-1]
        V.append({s: max(mdp["r"][(s, a)] + Vant[mdp["T"][(s, a)]] for a in ACOES) for s in ESTADOS})
    return V


def valor_otimo(mdp, inicio="A", horizonte=2):
    """O valor ótimo de `horizonte` decisões a partir de `inicio` (indução reversa)."""
    return iteracao_valor(mdp, horizonte)[horizonte][inicio]


def valor_miope(mdp, inicio="A", passos=2):
    """O valor do agente GULOSO (míope): a cada passo toma a ação de maior recompensa IMEDIATA, ignorando o futuro."""
    s, tot = inicio, 0.0
    for _ in range(passos):
        a = 0 if mdp["r"][(s, 0)] >= mdp["r"][(s, 1)] else 1
        tot += mdp["r"][(s, a)]
        s = mdp["T"][(s, a)]
    return tot


def mdp_separavel():
    """Um MDP de controle SEPARÁVEL por estágio: toda ação mantém o estado (T(s,a)=s), então a ação de agora NÃO muda o
    futuro alcançável — não há o que planejar, e o guloso (míope) coincide com a indução reversa (razão 1,0)."""
    return {
        "r": {("A", 0): 1.0, ("A", 1): 0.0, ("B", 0): 0.0, ("B", 1): 3.0},
        "T": {("A", 0): "A", ("A", 1): "A", ("B", 0): "B", ("B", 1): "B"},
    }


def _mdp_espelho(mdp):
    """O MDP com as ações TROCADAS (0<->1): o ótimo prefere a ação de rótulo oposto, então saber qual MDP importa."""
    r = {(s, a): mdp["r"][(s, 1 - a)] for s in ESTADOS for a in ACOES}
    T = {(s, a): mdp["T"][(s, 1 - a)] for s in ESTADOS for a in ACOES}
    return {"r": r, "T": T}


def _valor_politica(mdp, politica, inicio, horizonte):
    """Valor esperado (aqui determinístico) de uma política dependente do tempo politica[h][s] = ação, a partir de inicio."""
    s, tot = inicio, 0.0
    for h in range(horizonte):
        a = politica[h][s]
        tot += mdp["r"][(s, a)]
        s = mdp["T"][(s, a)]
    return tot


def voi_estado_oculto(mdp0, mdp1, crenca=0.5, inicio="A", horizonte=2):
    """O valor de SABER qual MDP (estado oculto): valor sabendo − valor crendo. Sabendo: joga o ótimo de cada um. Crendo:
    escolhe UMA política que maximiza o valor esperado sob a crença (sem saber qual). VOI = sabendo − crendo ≥ 0."""
    sabendo = crenca * valor_otimo(mdp0, inicio, horizonte) + (1 - crenca) * valor_otimo(mdp1, inicio, horizonte)
    melhor = None
    for combo in itertools.product(ACOES, repeat=len(ESTADOS) * horizonte):
        politica = [{ESTADOS[j]: combo[h * len(ESTADOS) + j] for j in range(len(ESTADOS))} for h in range(horizonte)]
        esp = crenca * _valor_politica(mdp0, politica, inicio, horizonte) + (1 - crenca) * _valor_politica(mdp1, politica, inicio, horizonte)
        if melhor is None or esp > melhor:
            melhor = esp
    return sabendo - melhor


def voi_espelho():
    """O VOI quando os dois MDPs são espelhos (preferem primeiras ações opostas): > 0."""
    return voi_estado_oculto(MDP_TESTE, _mdp_espelho(MDP_TESTE))


def voi_identico():
    """Controle: dois MDPs idênticos → saber não acrescenta nada → VOI = 0."""
    return voi_estado_oculto(MDP_TESTE, MDP_TESTE)
