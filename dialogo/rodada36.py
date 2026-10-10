"""Rodada 36 do diálogo Python <-> Java: o último dígito. Para cada base b de 3 a 16 e k de 2 a 7, entre os candidatos
(multiconjuntos cuja soma das potências s tem k dígitos), quantos passam no teste do último dígito (s mod b está no
multiconjunto), contra o esperado se s mod b fosse uniforme (soma de "dígitos distintos" / b). Por base, nas células sem
interruptor: o excesso, a razão medido/conta (Parte 60) e a conta corrigida pelo excesso célula a célula; e a correlação de
postos entre o excesso e a razão. Rodar da raiz do repositório: python3 dialogo/rodada36.py"""

from itertools import combinations_with_replacement
from math import sqrt

BASES, KS = range(3, 17), range(2, 8)


def fat(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def celula(b, k):
    """(candidatos, passam, soma dos distintos, medido, numerador da conta, denominador, g, interruptor)."""
    pot = [d ** k for d in range(b)]
    cand = passa = dist = medido = num = 0
    for ds in combinations_with_replacement(range(b), k):
        s = 0
        for d in ds:
            s += pot[d]
        if not b ** (k - 1) <= s < b ** k:
            continue
        cand += 1
        conj = set(ds)
        dist += len(conj)
        passa += (s % b) in conj
        m = fat(k)
        for d in range(b):
            m //= fat(ds.count(d))
        z = ds.count(0)
        num += m * (k - z) // k
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
    return cand, passa, dist, medido, num, den, g, inter


def postos(xs):
    """Postos médios (1-based) com empates."""
    ordem = sorted(range(len(xs)), key=lambda i: (xs[i], i))
    r = [0.0] * len(xs)
    i = 0
    while i < len(ordem):
        j = i
        while j + 1 < len(ordem) and xs[ordem[j + 1]] == xs[ordem[i]]:
            j += 1
        for t in range(i, j + 1):
            r[ordem[t]] = (i + j + 2) / 2
        i = j + 1
    return r


def pearson(xs, ys):
    n = len(xs)
    mx = my = 0.0
    for x in xs:
        mx += x
    for y in ys:
        my += y
    mx, my = mx / n, my / n
    sxy = sxx = syy = 0.0
    for x, y in zip(xs, ys):
        sxy += (x - mx) * (y - my)
        sxx += (x - mx) * (x - mx)
        syy += (y - my) * (y - my)
    return sxy / sqrt(sxx * syy)


def por_base():
    """[(b, excesso, razão medido/conta, medido, conta, conta corrigida)] nas células sem interruptor."""
    saida = []
    for b in BASES:
        passa = dist = medido = 0
        conta = corrigida = 0.0
        for k in KS:
            cand, p, ds, m, num, den, g, inter = celula(b, k)
            if inter or cand == 0:
                continue
            passa += p
            dist += ds
            medido += m
            e = (num / den) * g
            conta += e
            corrigida += e * ((p * b) / ds)
        saida.append((b, (passa * b) / dist, medido / conta, medido, conta, corrigida))
    return saida


def main():
    linhas = por_base()
    for b, exc, raz, m, e, ec in linhas:
        print(f"b={b} excesso={exc.hex()} razao={raz.hex()} medido={m} conta={e.hex()} corrigida={ec.hex()}")
    rho = pearson(postos([x[1] for x in linhas]), postos([x[2] for x in linhas]))
    m, e, ec = 0, 0.0, 0.0
    for x in linhas:
        m += x[3]
        e += x[4]
        ec += x[5]
    print(f"spearman = {rho.hex()}")
    print(f"total: medido={m} conta={e.hex()} corrigida={ec.hex()} razao={(m / e).hex()} razao corrigida={(m / ec).hex()}")


if __name__ == "__main__":
    main()
