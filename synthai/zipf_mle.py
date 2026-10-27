"""Parte 157 (do relatório recebido "Reengenharia Arquitetónica do SYNTHAI", secção 5): o expoente de Zipf por MÁXIMA VEROSSIMILHANÇA contra os mínimos
quadrados em log-log de `synthai.dicionario.zipf`. Só biblioteca padrão, offline.

Modelo: num vocabulário de N tipos, o tipo de posto r sai com p(r) = r^−s / H(N, s), H(N, s) = Σ_{r=1..N} r^−s. Com contagens c_r (n = Σ c_r), a
log-verossimilhança é ℓ(s) = −s Σ c_r ln r − n ln H(N, s), côncava em s; o escore zera em  (1/n) Σ c_r ln r = E_s[ln r]  (a média observada de ln r
iguala a esperada), resolvido por bisseção. Duas leituras dos postos: os VERDADEIROS (o gerador, só numa simulação) e os EMPÍRICOS (ordenar as contagens,
o que se tem num corpus de verdade)."""
import math
import random
from bisect import bisect_left


def harmonico(N, s):
    t = 0.0
    for r in range(1, N + 1):
        t += r ** -s
    return t


def media_log_esperada(N, s):
    """E_s[ln r] sob Zipf(s) em 1..N."""
    num = den = 0.0
    for r in range(1, N + 1):
        w = r ** -s
        num += w * math.log(r)
        den += w
    return num / den


def amostrar(s, N, n, semente):
    """n fichas de Zipf(s) em 1..N (CDF acumulada + busca binária). Devolve as contagens por posto VERDADEIRO (lista de N)."""
    rng = random.Random(semente)
    acum, t = [], 0.0
    for r in range(1, N + 1):
        t += r ** -s
        acum.append(t)
    c = [0] * N
    for _ in range(n):
        i = bisect_left(acum, rng.random() * t)
        c[min(i, N - 1)] += 1
    return c


def mle(contagens, N=None, lo=0.01, hi=5.0, tol=1e-10):
    """O s de máxima verossimilhança, com as contagens dadas em ordem de posto (o índice + 1 é o posto); N = len(contagens) se não dado."""
    if N is None:
        N = len(contagens)
    n = 0
    soma = 0.0
    for r, c in enumerate(contagens, start=1):
        n += c
        soma += c * math.log(r)
    alvo = soma / n
    # E_s[ln r] decresce com s: bisseção
    while hi - lo > tol:
        m = (lo + hi) / 2
        if media_log_esperada(N, m) > alvo:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def empiricas(contagens):
    """As contagens reordenadas da maior para a menor (os postos EMPÍRICOS), sem os zeros."""
    return sorted((c for c in contagens if c > 0), reverse=True)


def ols_loglog(contagens_ordenadas, de=1, ate=None):
    """Mínimos quadrados de ln f contra ln r (o método de synthai.dicionario.zipf) nos postos `de`..`ate` das contagens já ordenadas."""
    fs = contagens_ordenadas[de - 1: ate]
    xs = [math.log(r) for r in range(de, de + len(fs))]
    ys = [math.log(f) for f in fs]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return -sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
