"""Rodada 88 do diálogo Python <-> Java (Parte 120): o CFR VANILLA no pôquer Leduc, bit a bit. As regras (6 cartas, carta pública,
apostas 2 e 4, no máximo 2 aumentos por rodada) e as 120 distribuições na ordem de itertools.permutations; T = 3 iterações; imprime a
estratégia MÉDIA dos 288 conjuntos de informação em ordem de chave. Só +, −, ×, ÷, max e comparações. Da raiz: python3 dialogo/rodada88.py"""

from itertools import permutations

T = 3
DIST = tuple((a // 2, b // 2, c // 2) for a, b, c in permutations(range(6), 3))
APOSTA = (2, 4)


def rodada(h):
    return h.split("/")[-1], h.count("/")


def acoes(h):
    s, _ = rodada(h)
    if s.endswith("r"):
        return ("f", "c", "r") if s.count("r") < 2 else ("f", "c")
    return ("c", "r")


def jogador(h):
    return len(rodada(h)[0]) % 2


def acabou(s):
    return s == "cc" or (len(s) >= 2 and s.endswith("rc"))


def proximo(h, a):
    h2 = h + a
    s, r = rodada(h2)
    return h2 + "/" if r == 0 and acabou(s) else h2


def contribuicoes(h):
    pos = [1, 1]
    for r, s in enumerate(h.split("/")):
        devido = [0, 0]
        for i, a in enumerate(s):
            if a == "c":
                devido[i % 2] = max(devido)
            elif a == "r":
                devido[i % 2] = max(devido) + APOSTA[r]
        pos[0] += devido[0]
        pos[1] += devido[1]
    return pos


def terminal(h, c1, c2, b):
    s, r = rodada(h)
    if s.endswith("f"):
        pos = contribuicoes(h[:-1])
        return -float(pos[0]) if (len(s) - 1) % 2 == 0 else float(pos[1])
    if r == 1 and acabou(s):
        pos = contribuicoes(h)
        f1 = 10 + c1 if c1 == b else c1
        f2 = 10 + c2 if c2 == b else c2
        return float(pos[1]) if f1 > f2 else (-float(pos[0]) if f2 > f1 else 0.0)
    return None


def chave(h, c1, c2, b):
    j = jogador(h)
    return str(c1 if j == 0 else c2) + "|" + str(b if "/" in h else -1) + "|" + h


REG, SOMA = {}, {}


def estrategia(k, n):
    if k not in REG:
        return [1.0 / n] * n
    pos = [x if x > 0.0 else 0.0 for x in REG[k]]
    s = 0.0
    for x in pos:
        s += x
    return [x / s for x in pos] if s > 0.0 else [1.0 / n] * n


def cfr(c1, c2, b, h, p1, p2):
    u = terminal(h, c1, c2, b)
    if u is not None:
        return u
    j = jogador(h)
    acs = acoes(h)
    k = chave(h, c1, c2, b)
    s = estrategia(k, len(acs))
    util = [0.0] * len(acs)
    no = 0.0
    for i, a in enumerate(acs):
        util[i] = cfr(c1, c2, b, proximo(h, a), p1 * s[i], p2) if j == 0 else cfr(c1, c2, b, proximo(h, a), p1, p2 * s[i])
        no += s[i] * util[i]
    sinal = 1.0 if j == 0 else -1.0
    adv, prop = (p2, p1) if j == 0 else (p1, p2)
    r = REG.setdefault(k, [0.0] * len(acs))
    m = SOMA.setdefault(k, [0.0] * len(acs))
    for i in range(len(acs)):
        r[i] += adv * sinal * (util[i] - no)
        m[i] += prop * s[i]
    return no


def treinar():
    REG.clear()
    SOMA.clear()
    for _ in range(T):
        for c1, c2, b in DIST:
            cfr(c1, c2, b, "", 1.0, 1.0)
    media = {}
    for k, m in SOMA.items():
        s = 0.0
        for x in m:
            s += x
        media[k] = [x / s for x in m] if s > 0.0 else [1.0 / len(m)] * len(m)
    return media


def main():
    m = treinar()
    for k in sorted(m):
        print(k + " " + " ".join(x.hex() for x in m[k]))
    print("fim " + str(len(m)))


if __name__ == "__main__":
    main()
