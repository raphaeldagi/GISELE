"""Rodada 71 do diálogo Python <-> Java (Parte 104): a codificação posicional senoidal, bit a bit — na versão PORTÁVEL.
Pendência da rodada 70: o sin/cos é a 6ª face da fronteira da Parte 52? Esta rodada usa o seno/cosseno PRÓPRIOS (série de Taylor, exatas.py)
e calcula as frequências sem `pow` da libm (só sqrt, exato no IEEE, e multiplicação repetida), para não depender de nenhuma transcendental da
biblioteca (a regra da Parte 52/77). A sonda separada `sonda_seno_104.py` mede o naive (math.sin/Math.sin) e achou IGUAL nesta máquina — logo
sin não é fronteira aqui —, mas o artefato COMMITADO do diálogo é o portável. PE(pos)[2i]=sin(pos*wi), [2i+1]=cos(pos*wi). Da raiz: python3 dialogo/rodada71.py"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import cos_, sin_  # noqa: E402

D = 8
POS = [0, 1, 2, 5, 13, 40]


def freqs():
    """wi = 10000^(-2i/d) para d = 8: a razão r = 10000^(-1/4) = 1/sqrt(sqrt(10000)) (só sqrt, exato), e wi = r^i por multiplicação repetida."""
    r = 1.0 / math.sqrt(math.sqrt(10000.0))
    w, cur = [], 1.0
    for _ in range(D // 2):
        w.append(cur)
        cur = cur * r
    return w


def pe(pos, proprio=True):
    """A codificação posicional de pos (d=8) com o seno/cosseno próprios (proprio=True, o único caminho portável)."""
    v = []
    for w in freqs():
        v.append(sin_(pos * w))
        v.append(cos_(pos * w))
    return v


def main():
    for pos in POS:
        print("proprio " + str(pos) + " " + " ".join(x.hex() for x in pe(pos)))
    print("fim")


if __name__ == "__main__":
    main()
