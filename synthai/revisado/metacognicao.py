"""Metacognição (P9, P83, P152, P265): medir a si mesma com as réguas da série.

- auc: a discriminação de um escore (P83);
- comparacao_pareada: diferença média, desvio e t entre duas versões nas mesmas sementes (regra da Parte 9);
- normalizado: o retorno numa régua em que o acaso vale 0 e a referência que vê tudo vale 1 (o Υ da P265)."""

from math import isfinite, sqrt
from statistics import fmean, stdev


def auc(escores, rotulos):
    pos = [e for e, r in zip(escores, rotulos) if r]
    neg = [e for e, r in zip(escores, rotulos) if not r]
    if not pos or not neg:
        return float("nan")
    neg = sorted(neg)
    from bisect import bisect_left, bisect_right
    total = sum(bisect_left(neg, e) + 0.5 * (bisect_right(neg, e) - bisect_left(neg, e)) for e in pos)
    return total / (len(pos) * len(neg))


def comparacao_pareada(a, b):
    """b − a: (média, desvio amostral, t), com ao menos dois pares finitos.

    Com variância nula, t é NaN: a média continua informativa, mas não
    há estimativa de erro padrão para sustentar o teste t convencional.
    A função não verifica independência nem adequação do pareamento.
    """
    a, b = list(a), list(b)
    if len(a) != len(b):
        raise ValueError("as amostras devem ter o mesmo comprimento")
    if len(a) < 2:
        raise ValueError("são necessários ao menos dois pares")
    if not all(isfinite(x) for x in a + b):
        raise ValueError("as observações devem ser finitas")
    d = [y - x for x, y in zip(a, b)]
    if not all(isfinite(x) for x in d):
        raise ValueError("as diferenças devem ser finitas")
    m = fmean(x / len(d) for x in d) * len(d)
    dp = stdev(d)
    return m, dp, (m / (dp / sqrt(len(d))) if dp > 0 else float("nan"))


def normalizado(retorno, acaso, referencia):
    return (retorno - acaso) / (referencia - acaso)
