"""Rodada 80 do diálogo Python <-> Java (Parte 113): o CFR (Counterfactual Regret Minimization) no pôquer de Kuhn, bit a bit.
CFR vanilla simultâneo, as 6 distribuições enumeradas, T = 1.000 iterações; imprime a estratégia MÉDIA nos 12 conjuntos de informação.
Só +, −, ×, ÷ e comparações (o max(0, ·) do casamento de arrependimento é comparação). Da raiz: python3 dialogo/rodada80.py"""

T = 1000
HIST = ("", "pb", "p", "b")   # os dois primeiros são do jogador 1, os dois últimos do 2


def indice(carta, h):
    return (carta - 1) * 4 + HIST.index(h)


def terminal(h, c1, c2):
    ganha = 1.0 if c1 > c2 else -1.0
    if h == "pp":
        return ganha
    if h == "bb" or h == "pbb":
        return 2.0 * ganha
    if h == "bp":
        return 1.0
    if h == "pbp":
        return -1.0
    return None


def estrategia(reg, k):
    a = reg[k][0] if reg[k][0] > 0.0 else 0.0
    b = reg[k][1] if reg[k][1] > 0.0 else 0.0
    s = a + b
    if s > 0.0:
        return [a / s, b / s]
    return [0.5, 0.5]


def cfr(reg, soma, c1, c2, h, p1, p2):
    u = terminal(h, c1, c2)
    if u is not None:
        return u
    j = len(h) % 2
    k = indice(c1 if j == 0 else c2, h)
    s = estrategia(reg, k)
    util = [0.0, 0.0]
    no = 0.0
    for a in range(2):
        letra = "p" if a == 0 else "b"
        if j == 0:
            util[a] = cfr(reg, soma, c1, c2, h + letra, p1 * s[a], p2)
        else:
            util[a] = cfr(reg, soma, c1, c2, h + letra, p1, p2 * s[a])
        no = no + s[a] * util[a]
    sinal = 1.0 if j == 0 else -1.0
    adv = p2 if j == 0 else p1
    prop = p1 if j == 0 else p2
    for a in range(2):
        reg[k][a] = reg[k][a] + adv * sinal * (util[a] - no)
        soma[k][a] = soma[k][a] + prop * s[a]
    return no


def treinar():
    reg = [[0.0, 0.0] for _ in range(12)]
    soma = [[0.0, 0.0] for _ in range(12)]
    for _ in range(T):
        for c1 in (1, 2, 3):
            for c2 in (1, 2, 3):
                if c1 != c2:
                    cfr(reg, soma, c1, c2, "", 1.0, 1.0)
    media = []
    for k in range(12):
        s = soma[k][0] + soma[k][1]
        media.append(soma[k][1] / s if s > 0.0 else 0.5)
    return media


def main():
    m = treinar()
    for carta in (1, 2, 3):
        print("carta " + str(carta) + " " + " ".join(m[indice(carta, h)].hex() for h in HIST))
    print("fim")


if __name__ == "__main__":
    main()
