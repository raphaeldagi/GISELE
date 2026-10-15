"""O baralho como sinal que mistura NÚMERO e PALAVRA (Parte 103, P2531/P2532).

O pedido do usuário ("a IA do dicionário pode ser treinada com Poker e outros jogos de cartas que tenham números e
palavras") vira, de forma segura e offline (só biblioteca padrão), um caso mínimo do regime do Global Workspace
(Parte 102): uma carta tem um VALOR (número, 1..13) e um NAIPE (palavra). A cor (vermelho/preto) é função só do naipe.
Um decisor que vê só o número é CEGO à cor; um que vê número + palavra a recupera. O ganho de juntar as duas fontes
aparece só quando a tarefa precisa do que uma fonte não vê — o mesmo veredito de regime do workspace (P2501)."""

import math
import random

NAIPES = ("ouros", "espadas", "copas", "paus")   # palavra
VERMELHOS = {"ouros", "copas"}                     # a cor é função SÓ do naipe (a palavra)


def baralho():
    """As 52 cartas como pares (valor:número 1..13, naipe:palavra)."""
    return [(v, n) for n in NAIPES for v in range(1, 14)]


def cor(naipe):
    """A cor de uma carta é função só do naipe (a palavra), não do valor (o número)."""
    return "vermelho" if naipe in VERMELHOS else "preto"


def codigo(carta):
    """Converte a carta em UM número 0..51 (o dicionário-como-números, caso mínimo): valor-1 + 13*índice-do-naipe."""
    v, naipe = carta
    return (v - 1) + 13 * NAIPES.index(naipe)


def entropia_dos_saques(n=10000, semente=103):
    """A entropia empírica de n saques uniformes do baralho, em bits (o baralho como informação). O teto fechado é
    log2(52) = 5,7004; a amostra finita subestima (entropia de frequências observadas)."""
    r = random.Random(semente)
    cartas = baralho()
    from collections import Counter
    c = Counter(codigo(r.choice(cartas)) for _ in range(n))
    tot = sum(c.values())
    return -sum((k / tot) * math.log2(k / tot) for k in c.values())


def _amostrar_pares(n, semente):
    r = random.Random(semente)
    cartas = baralho()
    pares = []
    for _ in range(n):
        a, b = r.choice(cartas), r.choice(cartas)
        pares.append((a, b, cor(a[1]) == cor(b[1])))
    return pares


def acerto_so_numero(n=4000, semente=103):
    """Tarefa: "as duas cartas são da mesma cor?". O decisor que vê SÓ o valor (número) é cego à cor: a melhor regra
    fixa (prever sempre o rótulo majoritário, ou qualquer função só do valor) acerta ~0,5 — moeda. Devolve a acurácia."""
    pares = _amostrar_pares(n, semente)
    # a melhor decisão possível a partir só dos valores: prever o rótulo mais comum (a cor não depende do valor)
    maioria = sum(1 for _, _, y in pares if y) >= len(pares) / 2
    return sum(1 for _, _, y in pares if y == maioria) / len(pares)


def acerto_numero_e_palavra(n=4000, semente=103):
    """O decisor que vê valor + naipe (número + palavra) recupera a cor e acerta exatamente a tarefa: 1,00."""
    pares = _amostrar_pares(n, semente)
    return sum(1 for a, b, y in pares if (cor(a[1]) == cor(b[1])) == y) / len(pares)
