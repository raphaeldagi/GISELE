"""Rodada 68 do diálogo Python <-> Java (Parte 101): a penalidade de repetição (CTRL) na amostragem, bit a bit.
Antes do softmax, cada token já usado tem o logit dividido por um fator de penalidade > 1 se for positivo, ou multiplicado se for
negativo (a convenção de Keskar et al.): empurra os tokens repetidos para baixo. Depois, softmax com o EXP PRÓPRIO (a única fronteira
da Parte 52) e amostra por CDF com um u dado de fora. Dividir/multiplicar é exato; o exp é a fronteira. Rodar da raiz: python3 dialogo/rodada68.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

# (logits, usados, penalidade, u)
CASOS = [([2.0, 1.0, 0.5, 0.0, -1.0], [0], 1.3, 0.37),
         ([2.0, 1.0, 0.5, 0.0, -1.0], [0, 1], 1.3, 0.60),
         ([0.1, 3.0, 2.0, 2.9, 0.5], [1], 1.5, 0.50),
         ([1.0, -1.0, 2.0, -0.5, 0.0], [1, 3], 1.2, 0.80),
         ([5.0, -2.0, 0.0, 1.0, 3.0], [0, 4], 2.0, 0.95)]


def penalizar(logits, usados, pen):
    """Divide o logit de cada token usado por `pen` se positivo, multiplica se negativo (convencao CTRL)."""
    s = set(usados)
    out = []
    for i in range(len(logits)):
        x = logits[i]
        if i in s:
            x = x / pen if x > 0.0 else x * pen
        out.append(x)
    return out


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


def amostrar(p, u):
    acum = 0.0
    for i in range(len(p)):
        acum = acum + p[i]
        if u < acum:
            return i
    return len(p) - 1


def main():
    for c, (logits, usados, pen, u) in enumerate(CASOS):
        p = softmax(penalizar(logits, usados, pen))
        print(f"caso {c} token {amostrar(p, u)} top1 {max(p).hex()} p0 {p[0].hex()}")
    print("fim")


if __name__ == "__main__":
    main()
