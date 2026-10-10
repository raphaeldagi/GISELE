"""Rodada 44 do diálogo Python <-> Java: a lei de escala da forma de GPT, por álgebra. Lê dialogo/escala44.tsv (d, passos, bits em hexadecimal; medidos
uma vez pela P1541 e guardados) e, para cada d, ajusta bits = A·n^(−α) pelas equações normais da reta ln bits = ln A − α ln n (laços, log e exp
próprios da rodada 26); o n* em que a reta cruza o trigrama (2,768 bits); e a diferença entre d = 48 e d = 24 em 8.000 passos.
Rodar da raiz do repositório: python3 dialogo/rodada44.py"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from rodada26 import exp_, log_  # noqa: E402

TRIGRAMA = 2.768


def ler():
    pontos = {}
    with open(os.path.join(AQUI, "escala44.tsv")) as f:
        for linha in f:
            d, n, b = linha.split()
            pontos.setdefault(int(d), []).append((int(n), float.fromhex(b)))
    return pontos


def ajuste(pts):
    """(A, α, n*) pelas equações normais, em laços."""
    k = len(pts)
    sx = sy = 0.0
    for n, b in pts:
        sx += log_(float(n))
        sy += log_(b)
    mx, my = sx / k, sy / k
    sxx = sxy = 0.0
    for n, b in pts:
        x, y = log_(float(n)) - mx, log_(b) - my
        sxx += x * x
        sxy += x * y
    alfa = -(sxy / sxx)
    A = exp_(my + alfa * mx)
    n_estrela = exp_((log_(A) - log_(TRIGRAMA)) / alfa)
    return A, alfa, n_estrela


def main():
    pontos = ler()
    for d in sorted(pontos):
        A, alfa, ne = ajuste(pontos[d])
        print(f"d={d} pontos={len(pontos[d])} A={A.hex()} alfa={alfa.hex()} n_estrela={ne.hex()}")
    b24 = dict(pontos[24])[8000]
    b48 = dict(pontos[48])[8000]
    print(f"bits(d=48) - bits(d=24) em 8000 passos = {(b48 - b24).hex()}")


if __name__ == "__main__":
    main()
