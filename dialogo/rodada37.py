"""Rodada 37 do diálogo Python <-> Java: o fator de congruência efetivo dos narcisistas. Para cada base b de 3 a 16 e k de 2 a
7: F = (b − 1)·(fração dos candidatos com soma das potências ≡ soma dos dígitos, mod b − 1), contra o g da Parte 60; a conta
com F no lugar de g; por base, nas células sem interruptor, as razões medido/conta. Rodar da raiz: python3 dialogo/rodada37.py"""

from itertools import combinations_with_replacement

BASES, KS = range(3, 17), range(2, 8)


def fat(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def celula(b, k):
    """(candidatos, iguais mod b − 1, medido, numerador, denominador, g, interruptor)."""
    pot = [d ** k for d in range(b)]
    cand = iguais = medido = num = 0
    for ds in combinations_with_replacement(range(b), k):
        s = sd = 0
        for d in ds:
            s += pot[d]
            sd += d
        if not b ** (k - 1) <= s < b ** k:
            continue
        cand += 1
        iguais += (s - sd) % (b - 1) == 0
        m = fat(k)
        for d in range(b):
            m //= fat(ds.count(d))
        num += m * (k - ds.count(0)) // k
        dig, x = [], s
        while x:
            x, r = divmod(x, b)
            dig.append(r)
        medido += sorted(dig) == list(ds)
    den = (b - 1) * b ** (k - 1)
    g = 1
    for c in range(1, b):
        if (b - 1) % c == 0 and all((d ** k - d) % c == 0 for d in range(b)):
            g = c
    inter = any(d ** (k - 1) == b ** p for d in range(2, b) for p in range(k))
    return cand, iguais, medido, num, den, g, inter


def main():
    longe = com_cand = 0
    tm = 0
    tg = tf = 0.0
    for b in BASES:
        m = 0
        cg = cf = 0.0
        for k in KS:
            cand, ig, med, num, den, g, inter = celula(b, k)
            if cand == 0:
                continue
            f = ((b - 1) * ig) / cand
            com_cand += 1
            longe += abs(f - g) > 0.1 * g
            print(f"b={b} k={k} candidatos={cand} iguais={ig} F={f.hex()} g={g} interruptor={int(inter)}")
            if inter:
                continue
            e = num / den
            m += med
            cg += e * g
            cf += e * f
        tm += m
        tg += cg
        tf += cf
        print(f"base {b}: medido={m} conta_g={cg.hex()} conta_F={cf.hex()} razao_g={(m / cg).hex()} razao_F={(m / cf).hex()}")
    print(f"celulas com candidatos={com_cand}; F longe de g (>10%)={longe}; fracao={(longe / com_cand).hex()}")
    print(f"total: medido={tm} conta_g={tg.hex()} conta_F={tf.hex()} razao_g={(tm / tg).hex()} razao_F={(tm / tf).hex()}")


if __name__ == "__main__":
    main()
