"""Rodada 61 do diálogo Python <-> Java (Parte 94, pendência da Parte 93): uma cabeça de ATENÇÃO causal inteira, bit a bit.
Dado um contexto de T posições com embeddings de dimensão d, calcula Q=XWq, K=XWk, V=XWv, os escores causais
e[i][j] = (Q[i]·K[j])/√d para j<=i, o softmax sobre j (com o EXP PRÓPRIO — o exp é a fronteira da Parte 52; √d e a ÷ são
exatos no IEEE), a saída o[i] = Σ_j p[i][j]·V[j], e decide o próximo token por argmax de uma projeção linear da última saída.
Pesos e entrada FIXOS (determinístico, para a tradução ser bit a bit). Rodar da raiz: python3 dialogo/rodada61.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

T, D = 4, 3
# entrada X (T x D) e pesos Wq, Wk, Wv (D x D), projeção de saída Wo (D x V) — todos fixos.
X = [[0.5, -1.0, 0.25], [1.0, 0.0, -0.5], [-0.75, 0.5, 1.0], [0.1, -0.2, 0.3]]
WQ = [[0.2, -0.1, 0.4], [0.3, 0.5, -0.2], [-0.4, 0.1, 0.6]]
WK = [[0.1, 0.3, -0.5], [-0.2, 0.4, 0.2], [0.6, -0.3, 0.1]]
WV = [[0.5, 0.2, -0.1], [0.1, -0.4, 0.3], [-0.2, 0.6, 0.4]]
WO = [[0.3, -0.2], [0.1, 0.5], [-0.4, 0.2]]  # D x 2 (dois tokens candidatos)


def matvec(M, v):
    # v (len D) vezes a matriz (D x m): resultado (len m), somas na mesma ordem
    m = len(M[0])
    out = [0.0] * m
    for j in range(m):
        s = 0.0
        for k in range(len(v)):
            s = s + v[k] * M[k][j]
        out[j] = s
    return out


def sqrt_(x):
    import math
    return math.sqrt(x)  # sqrt IEEE (correto, obrigatório); igual a Math.sqrt bit a bit (NÃO pow(x,0.5), que é a fronteira)


def atencao():
    Q = [matvec(WQ, X[i]) for i in range(T)]
    K = [matvec(WK, X[i]) for i in range(T)]
    V = [matvec(WV, X[i]) for i in range(T)]
    escala = sqrt_(float(D))
    saidas = []
    for i in range(T):
        e = []
        for j in range(i + 1):  # máscara causal: só j <= i
            dot = 0.0
            for k in range(D):
                dot = dot + Q[i][k] * K[j][k]
            e.append(dot / escala)
        m = e[0]
        for x in e:
            if x > m:
                m = x
        ex = [exp_(x - m) for x in e]
        s = 0.0
        for x in ex:
            s = s + x
        p = [x / s for x in ex]
        o = [0.0] * D
        for j in range(i + 1):
            for k in range(D):
                o[k] = o[k] + p[j] * V[j][k]
        saidas.append(o)
    return saidas


def main():
    saidas = atencao()
    for i in range(T):
        for k in range(D):
            print(f"pos {i} saida {k} {saidas[i][k].hex()}")
    # decisão: argmax da projeção linear da última saída
    logits = matvec(WO, saidas[T - 1])
    for k in range(len(logits)):
        print(f"logit {k} {logits[k].hex()}")
    arg = 0 if logits[0] >= logits[1] else 1
    print(f"decisao {arg}")
    print("fim")


if __name__ == "__main__":
    main()
