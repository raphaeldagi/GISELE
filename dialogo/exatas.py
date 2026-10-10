"""O exp e o log PRÓPRIOS da rodada 26, num módulo só (Parte 73): as rodadas 21, 22, 23 e 25 usavam math.log/math.exp (glibc) e Math.log/Math.exp
(Java), que o IEEE 754 não obriga a arredondar corretamente; passaram por sorte até o resultados.txt crescer e deram DIFERENTES por 1 a 3 ulps. As
versões originais estão em dialogo/registro/. Cópia fiel de dialogo/rodada26.py (que continua com as suas), sem importar a 26 (ela importa a 21).
Só +, −, ×, ÷ e escalas exatas por 2^k."""

import math

LN2_HI = 6.93147180369123816490e-01  # ln 2 em duas partes (como na fdlibm): k·LN2_HI é exato para |k| < 2^20
LN2_LO = 1.90821492927058770002e-10
SQRT2 = 1.4142135623730951


def exp_(x):
    """e^x = 2^k · e^r, k = arredondar(x/ln 2), r = x − k ln 2 (|r| ≤ 0,35); e^r pela série de Taylor (Horner, 22 termos)."""
    k = math.floor(x / (LN2_HI + LN2_LO) + 0.5)
    r = (x - k * LN2_HI) - k * LN2_LO
    p = 1.0
    for i in range(22, 0, -1):
        p = 1.0 + r * p / i
    return math.ldexp(p, int(k))


def log_(x):
    """ln x = e ln 2 + ln m, x = m · 2^e com m em [√½, √2); ln m = 2 atanh s = 2 s Σ s^(2j)/(2j+1), s = (m − 1)/(m + 1)."""
    m, e = math.frexp(x)
    m, e = m * 2.0, e - 1
    if m > SQRT2:
        m, e = m / 2.0, e + 1
    s = (m - 1.0) / (m + 1.0)
    s2 = s * s
    p = 1.0 / 41.0
    for j in range(19, -1, -1):
        p = 1.0 / (2 * j + 1) + s2 * p
    return e * LN2_HI + (e * LN2_LO + 2.0 * s * p)
