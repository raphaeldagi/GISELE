"""Rodada 65 do diálogo Python <-> Java (Parte 98): a geração autorregressiva — amostrar o próximo token do softmax, bit a bit.
Dado um vetor de logits e um número uniforme u em [0,1) DADO DE FORA (determinístico, para a tradução ser bit a bit, já que o RNG
difere entre as línguas), calcula p = softmax(logits) com o EXP PRÓPRIO (a única fronteira da Parte 52), acumula a CDF e devolve o
primeiro token cujo acumulado passa de u (o método da transformada inversa). A busca na CDF é só soma e comparação. Rodar da raiz: python3 dialogo/rodada65.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

CASOS = [([2.0, 1.0, 0.5, 0.0, -1.0], 0.37),
         ([0.1, 0.2, 0.3, 0.25, 0.0], 0.95),
         ([-1.0, 3.0, 2.0, 2.9, 0.5], 0.05),
         ([1.0, 1.0, 1.0, 1.0, 1.0], 0.5),
         ([5.0, -2.0, 0.0, 1.0, 3.0], 0.999)]


def softmax(logits):
    m = logits[0]
    for x in logits:
        if x > m:
            m = x
    e = [exp_(x - m) for x in logits]
    s = 0.0
    for x in e:
        s = s + x
    return [x / s for x in e]


def amostrar(logits, u):
    """Inversão de CDF: devolve (token, p[token]). Acumula p até passar de u."""
    p = softmax(logits)
    acum = 0.0
    for i in range(len(p)):
        acum = acum + p[i]
        if u < acum:
            return i, p[i]
    return len(p) - 1, p[-1]


def main():
    for c, (logits, u) in enumerate(CASOS):
        tok, pt = amostrar(logits, u)
        print(f"caso {c} token {tok} p {pt.hex()}")
    print("fim")


if __name__ == "__main__":
    main()
