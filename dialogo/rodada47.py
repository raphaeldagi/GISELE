"""Rodada 47 do diálogo Python <-> Java: quanto vale perguntar. Com `--preparar PASTA`, o Python grava em PASTA/voi47.txt os 2.000 problemas de decisão
da P1632 (semente 73: p e as quatro utilidades, em hexadecimal). As duas linguagens calculam, para cada um, o valor da informação perfeita
VOI = p·max u[·][1] + (1 − p)·max u[·][0] − max_a (p·u[a][1] + (1 − p)·u[a][0]) e a prioridade S = H(p) + max_s |u[0][s] − u[1][s]| + 1 do texto
recebido na Parte 73 (H com o log_ próprio de dialogo/exatas.py), e imprimem: quantos têm VOI = 0, a soma dos VOI, a soma dos S, quantos dos 200 de maior S
(empates pelo índice) têm VOI = 0, e o VOI médio dos 200 de maior VOI e dos 200 de maior S. Rodar da raiz: python3 dialogo/rodada47.py PASTA"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import log_  # noqa: E402


def preparar(pasta, n=2000, semente=73):
    r = random.Random(semente)
    with open(os.path.join(pasta, "voi47.txt"), "w") as f:
        for _ in range(n):
            p = r.random()
            u = [r.random(), r.random(), r.random(), r.random()]  # u00 u01 u10 u11, na ordem da P1632
            f.write(" ".join(x.hex() for x in [p] + u) + "\n")


def ler(pasta):
    return [[float.fromhex(x) for x in l.split()] for l in open(os.path.join(pasta, "voi47.txt")).read().split("\n") if l]


def calcular(linhas):
    ln2 = log_(2.0)
    voi, s = [], []
    for p, u00, u01, u10, u11 in linhas:
        com = p * max(u01, u11) + (1.0 - p) * max(u00, u10)
        sem = max(p * u01 + (1.0 - p) * u00, p * u11 + (1.0 - p) * u10)
        v = com - sem
        if v < 0.0:
            v = 0.0
        h = 0.0
        for q in (p, 1.0 - p):
            if q > 0.0:
                h -= q * log_(q) / ln2
        voi.append(v)
        s.append(h + max(abs(u00 - u10), abs(u01 - u11)) + 1.0)
    return voi, s


def topo(chave, k):
    return sorted(range(len(chave)), key=lambda i: (-chave[i], i))[:k]


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        preparar(sys.argv[2])
        return
    voi, s = calcular(ler(sys.argv[1]))
    sv = ss = 0.0
    for v, x in zip(voi, s):
        sv += v
        ss += x
    ts, tv = topo(s, 200), topo(voi, 200)
    mts = mtv = 0.0
    for i in ts:
        mts += voi[i]
    for i in tv:
        mtv += voi[i]
    print(f"n={len(voi)} voi_zero={sum(1 for v in voi if v == 0.0)} soma_voi={sv.hex()} soma_s={ss.hex()}")
    print(f"topo_s_voi_zero={sum(1 for i in ts if voi[i] == 0.0)} voi_medio_topo_voi={(mtv / 200).hex()} voi_medio_topo_s={(mts / 200).hex()}")


if __name__ == "__main__":
    main()
