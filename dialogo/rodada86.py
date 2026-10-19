"""Rodada 86 do diálogo Python <-> Java (Parte 119): o MCCFR com amostragem EXTERNA no pôquer de Kuhn, bit a bit. Para cada jogador
(o viajante), sorteia o acaso e as ações do adversário (LCG inteiro; o uniforme é x/2³¹, exato) e percorre só as ações do viajante.
T = 3.000; imprime a estratégia MÉDIA nos 12 conjuntos. Só +, −, ×, ÷, comparações e inteiros. Da raiz: python3 dialogo/rodada86.py"""

T = 3000
SEMENTE = 1195
HIST = ("", "pb", "p", "b")
DIST = [(a, b) for a in (1, 2, 3) for b in (1, 2, 3) if a != b]
x = SEMENTE


def proximo():
    global x
    x = (1103515245 * x + 12345) % 2147483648
    return x


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


def es(reg, soma, c1, c2, h, i):
    u = terminal(h, c1, c2)
    if u is not None:
        return u if i == 0 else -u
    j = len(h) % 2
    k = indice(c1 if j == 0 else c2, h)
    s = estrategia(reg, k)
    if j == i:
        u0 = es(reg, soma, c1, c2, h + "p", i)
        u1 = es(reg, soma, c1, c2, h + "b", i)
        no = s[0] * u0 + s[1] * u1
        reg[k][0] = reg[k][0] + (u0 - no)
        reg[k][1] = reg[k][1] + (u1 - no)
        return no
    soma[k][0] = soma[k][0] + s[0]
    soma[k][1] = soma[k][1] + s[1]
    return es(reg, soma, c1, c2, h + ("p" if proximo() / 2147483648.0 < s[0] else "b"), i)


def treinar():
    global x
    x = SEMENTE
    reg = [[0.0, 0.0] for _ in range(12)]
    soma = [[0.0, 0.0] for _ in range(12)]
    for _ in range(T):
        for i in (0, 1):
            c1, c2 = DIST[(proximo() >> 16) % 6]
            es(reg, soma, c1, c2, "", i)
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
