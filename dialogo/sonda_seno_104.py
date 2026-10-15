"""Sonda da Parte 104: mede se a `sin`/`cos` NAIVE da libm difere entre Python e Java na codificação posicional (a 6ª face da
fronteira da Parte 52?). Usa as MESMAS frequências portáveis (sqrt) da rodada 71, trocando só sin_/cos_ próprios por math.sin/math.cos,
para isolar a transcendental. NÃO é uma rodada do diálogo (não casa com rodada[0-9]*.py; o auditor p1722 não a varre): é um experimento de
medição à parte. Resultado nesta máquina: IGUAL (Python/glibc e Java concordam bit a bit) — sin não é fronteira aqui. Da raiz: python3 dialogo/sonda_seno_104.py"""

import math

D = 8
POS = [0, 1, 2, 5, 13, 40]


def freqs():
    r = 1.0 / math.sqrt(math.sqrt(10000.0))
    w, cur = [], 1.0
    for _ in range(D // 2):
        w.append(cur)
        cur = cur * r
    return w


def pe(pos):
    v = []
    for w in freqs():
        v.append(math.sin(pos * w))   # NAIVE: a sin da libm (o que a sonda testa)
        v.append(math.cos(pos * w))
    return v


def main():
    for pos in POS:
        print("naive " + str(pos) + " " + " ".join(x.hex() for x in pe(pos)))
    print("fim")


if __name__ == "__main__":
    main()
