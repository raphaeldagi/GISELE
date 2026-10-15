"""Rodada 73 do diálogo Python <-> Java (Parte 106): o seno/cosseno PRÓPRIOS na faixa onde a libm divergiu, bit a bit.
A Parte 105 mediu que a `math.sin`/`Math.sin` da libm divergem 21/18 em 10 000 args de [0,001; 10]. Aqui a série de Taylor própria
(com redução em duas partes) é rodada nos MESMOS argumentos: como usa só +, −, ×, ÷ e a mesma ordem, é IGUAL bit a bit entre as
línguas — a série própria é portável onde a libm não é (a solução da fronteira, Parte 52). Da raiz: python3 dialogo/rodada73.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import cos_, sin_  # noqa: E402

N = 10000


def main():
    linhas = []
    for k in range(1, N + 1):
        x = k / 1000.0
        linhas.append("s " + sin_(x).hex() + " c " + cos_(x).hex())
    print("\n".join(linhas))
    print("fim")


if __name__ == "__main__":
    main()
