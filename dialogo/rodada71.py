"""Rodada 71 do diálogo Python <-> Java (Parte 104): a codificação posicional senoidal, bit a bit.
Pendência da rodada 70: o sin/cos é a 6ª face da fronteira da Parte 52? Imprime DOIS blocos: 'proprio' (seno/cosseno PRÓPRIOS,
série de Taylor) e 'naive' (math.sin/Math.sin da libm). A comparação é feita bloco a bloco: o próprio deve ser IGUAL; o naive mostra
se a libm difere entre as línguas. PE(pos)[2i]=sin(pos*wi), [2i+1]=cos(pos*wi), wi=10000^(-2i/d). Da raiz: python3 dialogo/rodada71.py"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import cos_, sin_  # noqa: E402

D = 8
POS = [0, 1, 2, 5, 13, 40]


def freqs():
    return [10000.0 ** (-2.0 * i / D) for i in range(D // 2)]


def pe(pos, proprio):
    s, c = (sin_, cos_) if proprio else (math.sin, math.cos)
    v = []
    for w in freqs():
        v.append(s(pos * w))
        v.append(c(pos * w))
    return v


def main():
    for rotulo, proprio in (("proprio", True), ("naive", False)):
        for pos in POS:
            print(rotulo + " " + str(pos) + " " + " ".join(x.hex() for x in pe(pos, proprio)))
    print("fim")


if __name__ == "__main__":
    main()
