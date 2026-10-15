"""Rodada 66 do diálogo Python <-> Java (Parte 99): a amostragem com TEMPERATURA e TOP-K, bit a bit.
Dado logits, uma temperatura T e um corte k, divide os logits por T (só divisão), mantém os k maiores e zera o resto (só comparação),
renormaliza, calcula o softmax com o EXP PRÓPRIO (a única fronteira da Parte 52) e amostra por inversão de CDF com um u dado de fora.
Também imprime a entropia da distribuição. O exp é a única fronteira; T, top-k e CDF são divisão, comparação e soma. Rodar da raiz: python3 dialogo/rodada66.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_, log_  # noqa: E402

# (logits, T, k, u)
CASOS = [([2.0, 1.0, 0.5, 0.0, -1.0], 1.0, 5, 0.37),
         ([2.0, 1.0, 0.5, 0.0, -1.0], 0.5, 5, 0.60),
         ([2.0, 1.0, 0.5, 0.0, -1.0], 2.0, 5, 0.60),
         ([2.0, 1.0, 0.5, 0.0, -1.0], 1.0, 2, 0.60),
         ([0.1, 3.0, 2.0, 2.9, 0.5], 0.8, 3, 0.95)]


def softmax_top_k(logits, T, k):
    """Divide por T, mantém os k maiores (os outros recebem −infinito efetivo via máscara), softmax com exp próprio."""
    z = [x / T for x in logits]
    # limiar do k-ésimo maior (ordenação por comparação)
    ordenado = sorted(range(len(z)), key=lambda i: z[i], reverse=True)
    mantidos = set(ordenado[:k])
    m = None
    for i in range(len(z)):
        if i in mantidos and (m is None or z[i] > m):
            m = z[i]
    e = [exp_(z[i] - m) if i in mantidos else 0.0 for i in range(len(z))]
    s = 0.0
    for x in e:
        s = s + x
    return [x / s for x in e]


def entropia(p):
    h = 0.0
    for x in p:
        if x > 0.0:
            h = h - x * log_(x)
    return h


def amostrar(p, u):
    acum = 0.0
    for i in range(len(p)):
        acum = acum + p[i]
        if u < acum:
            return i
    return len(p) - 1


def main():
    for c, (logits, T, k, u) in enumerate(CASOS):
        p = softmax_top_k(logits, T, k)
        tok = amostrar(p, u)
        h = entropia(p)
        print(f"caso {c} token {tok} top1 {max(p).hex()} entropia {h.hex()}")
    print("fim")


if __name__ == "__main__":
    main()
