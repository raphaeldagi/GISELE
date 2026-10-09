"""Rodada 12 do diálogo Python <-> Java: a engenharia reversa dos meus próprios textos (synthai/engenharia_reversa.py, P672 e
P674). Os 12 4-gramas de palavras que aparecem em mais documentos das Partes 31-40 (com o número de documentos e de
ocorrências) e, no dialogo/DIALOGO.md, quantas falas cada voz tem e quantas palavras por fala.
Rodar da raiz do repositório: python3 dialogo/rodada12.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import calculos  # noqa: E402
from synthai.engenharia_reversa import falas_do_dialogo, padroes_repetidos, palavras  # noqa: E402


def main():
    docs, dialogo = calculos._meus_textos()
    for g, nd, nt in padroes_repetidos(docs, 4, topo=12):
        print(f"{g} | {nd} | {nt}")
    for voz, fs in falas_do_dialogo(dialogo).items():
        n = sum(len(palavras(f)) for f in fs)
        print(f"{voz}: {len(fs)} falas, {n} palavras, {(n / len(fs)).hex()} por fala")


if __name__ == "__main__":
    main()
