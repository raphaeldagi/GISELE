"""Rodada 59 do diálogo Python <-> Java (Parte 92, pendência da Parte 91): um passo de Adam, bit a bit. Adam usa b1^t e b2^t na correção de viés — o `pow`,
que é a fronteira da Parte 52. Aqui b1^t e b2^t vêm de MULTIPLICAÇÃO REPETIDA (pow inteiro próprio, portável), não da `pow` da libm; √ é correto no IEEE; e
o forward (softmax/perda) usa exp/log próprios. Um passo de Adam sobre os logits da camada de saída, nos mesmos 5 casos da rodada 58. Imprime os logits novos
(hex) e a perda depois. Rodar da raiz: python3 dialogo/rodada59.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_, log_  # noqa: E402

LR, B1, B2, EPS = 0.1, 0.9, 0.999, 1e-8
CASOS = [([2.0, 1.0, 0.5, 0.0], 2),
         ([0.1, 0.2, 0.3, 0.25], 0),
         ([-1.0, 3.0, 2.0, 2.9], 3),
         ([1.0, 1.0, 1.0, 1.0], 1),
         ([5.0, -2.0, 0.0, 1.0], 1)]


def pow_int(base, n):
    """base^n por multiplicacao repetida (portavel bit a bit): o resultado e a mesma sequencia de produtos nas duas linguas."""
    r = 1.0
    for _ in range(n):
        r = r * base
    return r


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


def adam_passo(logits, alvo, passos=3):
    """Aplica `passos` passos de Adam sobre os logits (recalculando o gradiente p - onehot a cada passo). Devolve (logits finais, perda final)."""
    import math
    n = len(logits)
    w = list(logits)
    m = [0.0] * n
    v = [0.0] * n
    for t in range(1, passos + 1):
        p = softmax(w)
        g = [p[i] - (1.0 if i == alvo else 0.0) for i in range(n)]
        c1 = 1.0 - pow_int(B1, t)
        c2 = 1.0 - pow_int(B2, t)
        for i in range(n):
            m[i] = B1 * m[i] + (1.0 - B1) * g[i]
            v[i] = B2 * v[i] + (1.0 - B2) * g[i] * g[i]
            mhat = m[i] / c1
            vhat = v[i] / c2
            w[i] = w[i] - LR * mhat / (math.sqrt(vhat) + EPS)
    p = softmax(w)
    return w, -log_(p[alvo])


def main():
    for c, (logits, alvo) in enumerate(CASOS):
        w, perda = adam_passo(list(logits), alvo)
        for i in range(len(w)):
            print(f"caso {c} w {i} {w[i].hex()}")
        print(f"caso {c} perda {perda.hex()}")
    print("fim")


if __name__ == "__main__":
    main()
