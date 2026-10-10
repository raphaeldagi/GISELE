"""Rodada 35 do diálogo Python <-> Java: o dobro que falta nos narcisistas. Para cada base b de 3 a 16 e cada k de 2 a 7, conta os
narcisistas de k dígitos e calcula a conta da Parte 60 (P1250: soma inteira dos arranjos sem zero à esquerda, dividida por
(b − 1)·b^(k−1), vezes o fator de congruência g da P1249), e marca as células com interruptor (algum d·b^p = d^k além de 1 na
posição 0). Rodar da raiz do repositório: python3 dialogo/rodada35.py"""

from itertools import combinations_with_replacement

BASES, KS = range(3, 17), range(2, 8)
NOVAS = (3, 4, 5, 7, 9, 11, 13, 14, 15)


def fat(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def celula(b, k):
    """(medido, numerador, denominador, g, com interruptor, conta com o fator)."""
    pot = [d ** k for d in range(b)]
    medido, num = 0, 0
    for ds in combinations_with_replacement(range(b), k):
        s = 0
        for d in ds:
            s += pot[d]
        if not b ** (k - 1) <= s < b ** k:
            continue
        m = fat(k)
        for d in range(b):
            m //= fat(ds.count(d))
        z = ds.count(0)
        num += m * (k - z) // k
        dig, x = [], s
        while x:
            x, r = divmod(x, b)
            dig.append(r)
        if sorted(dig) == list(ds):
            medido += 1
    den = (b - 1) * b ** (k - 1)
    g = 1
    for c in range(1, b):
        if (b - 1) % c == 0 and all((d ** k - d) % c == 0 for d in range(b)):
            g = c
    inter = any(d ** (k - 1) == b ** p for d in range(2, b) for p in range(k))
    return medido, num, den, g, inter, (num / den) * g


def grupos(celulas):
    """{nome: (medido, conta)} somados num laço (sem sum(), que no Python 3.12+ compensa)."""
    filtros = [("sem interruptor, impares", lambda b, i: not i and b % 2 == 1),
               ("sem interruptor, pares", lambda b, i: not i and b % 2 == 0),
               ("sem interruptor, bases novas", lambda b, i: not i and b in NOVAS),
               ("sem interruptor", lambda b, i: not i), ("com interruptor", lambda b, i: i)]
    saida = []
    for nome, f in filtros:
        m, e = 0, 0.0
        for (b, k), c in celulas:
            if f(b, c[4]):
                m += c[0]
                e += c[5]
        saida.append((nome, m, e))
    return saida


def main():
    celulas = [((b, k), celula(b, k)) for b in BASES for k in KS]
    for (b, k), (m, num, den, g, inter, e) in celulas:
        print(f"b={b} k={k} medido={m} num={num} den={den} g={g} interruptor={int(inter)} conta={e.hex()}")
    gs = grupos(celulas)
    for nome, m, e in gs:
        print(f"{nome}: medido={m} conta={e.hex()} razao={(m / e).hex()}")
    print(f"razao com/sem interruptor = {((gs[4][1] / gs[4][2]) / (gs[3][1] / gs[3][2])).hex()}")


if __name__ == "__main__":
    main()
