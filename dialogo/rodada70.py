"""Rodada 70 do diálogo Python <-> Java (Parte 103): a atenção de MÚLTIPLAS CABEÇAS concatenadas, bit a bit.
A pendência da rodada 69: a concatenação das cabeças e a projeção de saída mudam a ordem das somas? Resposta medida: não — a
concatenação é só layout; a projeção soma sobre a dimensão concatenada na MESMA ordem de índice nos dois lados. O único
transcendental é o exp do softmax de cada cabeça (Parte 52). Entradas e pesos fixos (determinístico). Da raiz: python3 dialogo/rodada70.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

# d_model=4, H=2 cabeças de dh=2; T=3 posições. Entradas e pesos fixos.
X = [
    [0.5, -0.2, 0.1, 0.4],
    [-0.3, 0.8, 0.2, -0.1],
    [0.2, 0.2, -0.5, 0.6],
]
WQ = [[0.1, -0.2, 0.3, 0.0], [0.2, 0.1, -0.1, 0.4], [0.0, 0.3, 0.2, -0.2], [-0.1, 0.1, 0.4, 0.3]]
WK = [[0.2, 0.0, -0.1, 0.3], [0.1, 0.2, 0.3, -0.2], [-0.3, 0.1, 0.0, 0.2], [0.4, -0.1, 0.2, 0.1]]
WV = [[0.3, 0.1, 0.0, -0.2], [0.0, -0.1, 0.2, 0.3], [0.1, 0.4, -0.2, 0.1], [0.2, 0.0, 0.3, -0.1]]
WO = [[0.1, 0.2, -0.1, 0.3], [0.3, -0.2, 0.1, 0.0], [-0.1, 0.1, 0.2, 0.2], [0.2, 0.3, 0.0, -0.1]]
DH = 2  # dimensão por cabeça; cabeça 0 = colunas 0..1, cabeça 1 = colunas 2..3


def matvec(W, x):
    # acumulação sequencial (NÃO o sum() compensado/Neumaier do Python 3.12+, regra da Parte 34): mesma ordem que o Java
    out = []
    for i in range(len(W)):
        s = 0.0
        for j in range(len(x)):
            s = s + W[i][j] * x[j]
        out.append(s)
    return out


def softmax(scores):
    m = scores[0]
    for s in scores:
        if s > m:
            m = s
    e = [exp_(s - m) for s in scores]
    tot = 0.0
    for v in e:
        tot = tot + v
    return [v / tot for v in e]


def multihead():
    """Devolve a saída (T x d_model) da atenção causal de 2 cabeças concatenadas + projeção WO."""
    Q = [matvec(WQ, x) for x in X]
    K = [matvec(WK, x) for x in X]
    V = [matvec(WV, x) for x in X]
    import math
    esc = 1.0 / math.sqrt(DH)
    saida = []
    for t in range(len(X)):
        concat = [0.0] * 4
        for h in range(2):
            c0 = h * DH
            # atenção causal: posições 0..t
            scores = []
            for u in range(t + 1):
                dot = 0.0
                for d in range(DH):
                    dot = dot + Q[t][c0 + d] * K[u][c0 + d]
                scores.append(dot * esc)
            a = softmax(scores)
            for d in range(DH):
                acc = 0.0
                for u in range(t + 1):
                    acc = acc + a[u] * V[u][c0 + d]
                concat[c0 + d] = acc
        saida.append(matvec(WO, concat))   # projeção de saída soma sobre a dim concatenada em ordem de índice
    return saida


def main():
    s = multihead()
    for t, linha in enumerate(s):
        print("saida " + str(t) + " " + " ".join(v.hex() for v in linha))
    print("fim")


if __name__ == "__main__":
    main()
