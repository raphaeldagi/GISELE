"""Rodada 31 do diálogo Python <-> Java: o alfabeto do português. Os 13 primeiros 4-gramas da Rodada 12 (documentos, ocorrências)
reordenados com a chave de um dicionário português (a palavra sem acentos e minúscula, pela decomposição NFD sem as marcas;
depois a original como desempate), contra a ordem dos códigos Unicode. Conta os pares que mudam de ordem relativa. Com
`--preparar PASTA` escreve PASTA/gramas31.txt (n-grama TAB documentos TAB ocorrências), que o Java lê.
Rodar da raiz do repositório: python3 dialogo/rodada31.py"""

import os
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)


def gramas():
    import calculos
    from synthai.engenharia_reversa import padroes_repetidos
    docs, _ = calculos._meus_textos()
    return padroes_repetidos(docs, 4, topo=13)


def chave_pt(g):
    t = unicodedata.normalize("NFD", g)
    return "".join(c for c in t if not unicodedata.category(c).startswith("M")).lower()


def reordenar(gs):
    """As duas ordens: Unicode (a da Rodada 12) e português; e os pares (i, j) cuja ordem relativa muda."""
    uni = sorted(gs, key=lambda x: (-x[1], -x[2], x[0]))
    pt = sorted(gs, key=lambda x: (-x[1], -x[2], chave_pt(x[0]), x[0]))
    pos = {g[0]: i for i, g in enumerate(pt)}
    trocas = [(a[0], b[0]) for i, a in enumerate(uni) for b in uni[i + 1:] if pos[a[0]] > pos[b[0]]]
    return uni, pt, trocas


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "gramas31.txt"), "w", encoding="utf-8") as f:
            for g, nd, nt in gramas():
                f.write(f"{g}\t{nd}\t{nt}\n")
        return
    if len(sys.argv) == 2:
        gs = []
        for l in open(os.path.join(sys.argv[1], "gramas31.txt"), encoding="utf-8").read().split("\n"):
            if l:
                g, nd, nt = l.split("\t")
                gs.append((g, int(nd), int(nt)))
    else:
        gs = gramas()
    uni, pt, trocas = reordenar(gs)
    for g, nd, nt in pt:
        print(f"{g} | {nd} | {nt}")
    print(f"pares que mudam de ordem: {len(trocas)}")
    for a, b in trocas:
        print(f"  {a} <-> {b}")


if __name__ == "__main__":
    main()
