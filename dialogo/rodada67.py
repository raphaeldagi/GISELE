"""Rodada 67 do diálogo Python <-> Java (Parte 100): a amostragem NUCLEUS (top-p), bit a bit.
Dado logits, um limiar p e um u dado de fora, calcula o softmax com o EXP PRÓPRIO (a única fronteira da Parte 52), ordena as
probabilidades em ordem decrescente, soma a CDF até passar de p (o "núcleo"), zera o resto, renormaliza e amostra por inversão de CDF.
O exp é a única fronteira; a ordenação, a soma e a comparação são exatas. Rodar da raiz: python3 dialogo/rodada67.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

# (logits, p, u)
CASOS = [([2.0, 1.0, 0.5, 0.0, -1.0], 0.9, 0.37),
         ([2.0, 1.0, 0.5, 0.0, -1.0], 0.5, 0.60),
         ([0.1, 3.0, 2.0, 2.9, 0.5], 0.8, 0.95),
         ([1.0, 1.0, 1.0, 1.0, 1.0], 0.6, 0.50),
         ([5.0, -2.0, 0.0, 1.0, 3.0], 0.95, 0.80)]


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


def nucleus(logits, p_limiar):
    """Mantem o menor conjunto de tokens cujo acumulado (em ordem decrescente) passa de p_limiar; renormaliza. Devolve a distribuicao."""
    p = softmax(logits)
    ordem = sorted(range(len(p)), key=lambda i: p[i], reverse=True)
    mantidos = []
    acum = 0.0
    for i in ordem:
        mantidos.append(i)
        acum = acum + p[i]
        if acum >= p_limiar:
            break
    conj = set(mantidos)
    massa = 0.0
    for i in range(len(p)):   # soma em ordem de ÍNDICE (igual ao Java), não em ordem decrescente
        if i in conj:
            massa = massa + p[i]
    return [(p[i] / massa if i in conj else 0.0) for i in range(len(p))]


def amostrar(p, u):
    acum = 0.0
    for i in range(len(p)):
        acum = acum + p[i]
        if u < acum:
            return i
    return len(p) - 1


def main():
    for c, (logits, pl, u) in enumerate(CASOS):
        q = nucleus(logits, pl)
        tok = amostrar(q, u)
        mantidos = sum(1 for x in q if x > 0.0)
        print(f"caso {c} token {tok} mantidos {mantidos} top1 {max(q).hex()}")
    print("fim")


if __name__ == "__main__":
    main()
