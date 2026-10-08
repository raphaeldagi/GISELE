"""Metacognição (P9, P83, P152, P265): medir a si mesma com as réguas da série.

- auc: a discriminação de um escore (P83);
- comparacao_pareada: diferença média, desvio e t entre duas versões nas mesmas sementes (regra da Parte 9);
- normalizado: o retorno numa régua em que o acaso vale 0 e a referência que vê tudo vale 1 (o Υ da P265)."""

from math import sqrt


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
    """b − a nas mesmas sementes: (média, desvio, t)."""
    d = [y - x for x, y in zip(a, b)]
    m = sum(d) / len(d)
    dp = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return m, dp, (m / (dp / sqrt(len(d))) if dp > 0 else float("inf"))


def normalizado(retorno, acaso, referencia):
    return (retorno - acaso) / (referencia - acaso)
