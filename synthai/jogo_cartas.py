"""O pôquer mínimo: decisão sob informação OCULTA (Parte 104, P2561-P2563).

A Parte 103 deixou o baralho como sinal número+palavra com informação completa. O jogo só fica interessante quando há uma
carta escondida — é a volta ao tema das Partes 83/84 (decisão bayesiana, valor da informação), agora em cartas. Offline,
determinístico, só biblioteca padrão. Cartas i.i.d. uniformes 1..13 (com reposição) para manter as contas fechadas."""

import random

N = 13  # valores 1..13


def prob_ganhar_por_carta(c):
    """P(ganhar | sua carta c) no duelo de carta alta, cartas i.i.d. uniformes 1..13: P(opp<c) + 0,5 P(opp=c) = ((c-1)+0,5)/13.
    Linear em c, inclinação 1/13."""
    return ((c - 1) + 0.5) / N


def inclinacao_analitica():
    """A inclinação da reta P(ganhar|c): 1/13."""
    return 1.0 / N


def ev_simetrico(n=20000, semente=104):
    """O EV empírico do jogo simétrico (ambos sorteiam, maior ganha, empate 0,5): deve ser 0,5 por simetria."""
    r = random.Random(semente)
    tot = 0.0
    for _ in range(n):
        a, b = r.randint(1, N), r.randint(1, N)
        tot += 1.0 if a > b else (0.5 if a == b else 0.0)
    return tot / n


def prob_ganhar_dado_aposta(c, t):
    """P(ganhar | sua carta c, adversário só aposta com carta >= t): a posterior é uniforme em {t..13}."""
    faixa = list(range(t, N + 1))
    menores = sum(1 for k in faixa if k < c)
    empates = sum(1 for k in faixa if k == c)
    return (menores + 0.5 * empates) / len(faixa)


def limiar_pagar(t=7):
    """A menor carta com que pagar a aposta ganha > 0,5, dado que o adversário só aposta com carta >= t (a metade de cima).
    Forma fechada: a posterior é uniforme em {t..13}, média (t+13)/2."""
    for c in range(1, N + 1):
        if prob_ganhar_dado_aposta(c, t) > 0.5:
            return c
    return None


def fracao_info_muda(n=20000, semente=104):
    """A fração de mãos em que VER a carta do adversário muda a decisão de um jogo em que você pagaria às cegas: é
    P(sua carta perde) = P(opp > você) = (1 - P(empate))/2 = 6/13. O valor da informação oculta (VOI das Partes 83/84)."""
    r = random.Random(semente)
    muda = 0
    for _ in range(n):
        voce, opp = r.randint(1, N), r.randint(1, N)
        if opp > voce:   # às cegas você pagaria e perderia; vendo, desistiria
            muda += 1
    return muda / n
