"""Rodada 27 do diálogo Python <-> Java: o preditor de mim mesma (calculos.p1032_preditor_de_mim) sobre o histórico das
Partes 31-52 congelado em dialogo/historico27.tsv (calculos.p1031_historico_de_mim no momento do registro; "-" = sem valor).
Imprime, para cada medida, o centro, a meia-largura e o valor ingênuo. Rodar da raiz do repositório: python3 dialogo/rodada27.py"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import calculos  # noqa: E402


def historico():
    linhas = open(os.path.join(RAIZ, "dialogo", "historico27.tsv"), encoding="ascii").read().split("\n")
    nomes = linhas[0].split("\t")[1:]
    h = {}
    for l in linhas[1:]:
        if not l:
            continue
        c = l.split("\t")
        h[int(c[0])] = {m: (None if v == "-" else (float(v) if m in ("compressao", "redundancia") else int(v))) for m, v in zip(nomes, c[1:])}
    return h


def main():
    for medida, (m, w, u) in calculos.p1032_preditor_de_mim(historico()).items():
        print(f"{medida}: centro = {float(m).hex()}; meia-largura = {float(w).hex()}; ingenuo = {float(u).hex()}")


if __name__ == "__main__":
    main()
