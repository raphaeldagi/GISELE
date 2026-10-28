"""Parte 158 (a pendência 1 da Parte 157): o expoente de Zipf pela distribuição das FREQUÊNCIAS, à maneira de Clauset, Shalizi e Newman (2009), sem
ordenar a amostra. Só biblioteca padrão, offline.

Se o posto r tem frequência ∝ r^−s, o número de tipos com frequência ≥ x cai como x^−1/s, e a frequência x de um tipo segue uma lei de potência discreta
p(x) = x^−α / ζ(α, x_min) para x ≥ x_min, com α = 1 + 1/s (ζ de Hurwitz). A máxima verossimilhança de α zera o escore
(1/m) Σ ln x_i = E_α[ln x] (m = tipos com x ≥ x_min), resolvido por bisseção; s = 1/(α − 1). O ζ e a sua derivada saem de uma soma até K e do resto de
Euler–Maclaurin (integral + meio termo + correção de Bernoulli)."""
import math


def _zeta_e_dlog(a, xmin, K=2000):
    """(ζ(a, xmin), Σ_{k≥xmin} k^−a ln k): soma direta até xmin + K − 1 e resto de Euler–Maclaurin a partir de N = xmin + K."""
    z = d = 0.0
    for k in range(xmin, xmin + K):
        w = k ** -a
        z += w
        d += w * math.log(k)
    N = xmin + K
    lnN = math.log(N)
    wN = N ** -a
    # resto: ∫_N^∞ x^−a dx + f(N)/2 − f'(N)/12
    z += N ** (1 - a) / (a - 1) + wN / 2 + a * N ** (-a - 1) / 12
    # g(x) = x^−a ln x: ∫_N^∞ g = N^(1−a) (ln N/(a−1) + 1/(a−1)²); g' = x^(−a−1)(1 − a ln x)
    d += N ** (1 - a) * (lnN / (a - 1) + 1 / (a - 1) ** 2) + wN * lnN / 2 - N ** (-a - 1) * (1 - a * lnN) / 12
    return z, d


def media_log_esperada(a, xmin):
    z, d = _zeta_e_dlog(a, xmin)
    return d / z


def alfa_mle(frequencias, xmin=1, lo=1.05, hi=6.0, tol=1e-10):
    """O α de máxima verossimilhança da lei de potência discreta nas frequências ≥ xmin (as frequências dos TIPOS vistos, em qualquer ordem)."""
    xs = [x for x in frequencias if x >= xmin]
    alvo = sum(math.log(x) for x in xs) / len(xs)
    while hi - lo > tol:
        m = (lo + hi) / 2
        if media_log_esperada(m, xmin) > alvo:  # E[ln x] decresce com α
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def s_de_alfa(a):
    """O expoente da lei posto-frequência que corresponde a α: s = 1/(α − 1)."""
    return 1 / (a - 1)
