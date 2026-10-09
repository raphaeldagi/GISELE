"""Rodada 2 do diálogo Python <-> Java: o fecho parcial do dicionário (synthai/dicionario.py, P381) em Python, impresso
no mesmo formato que Rodada02.java. Com `--preparar PASTA`, escreve antes o grafo de definições em PASTA/grafo02.txt
(uma linha por palavra: a palavra, um TAB e as palavras que a definem, separadas por espaço), que o Java lê.
Rodar da raiz do repositório: python3 dialogo/rodada02.py"""

import hashlib
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthai.dicionario import Dicionario, fecho_parcial  # noqa: E402

THETAS = (1.0, 0.9, 0.8, 0.7, 0.6)
ANCORAS = 2000


def fecho_ingenuo(ancoradas, defs, theta):
    """O mesmo fecho, com o teto em ponto flutuante (math.ceil(theta * n)), o erro que a previsão 2 espera."""
    conhecidas = set(ancoradas)
    precisa = {x: math.ceil(theta * len(s)) for x, s in defs.items()}
    tem = {x: 0 for x in defs}
    usado_por = {}
    for x, s in defs.items():
        for y in s:
            usado_por.setdefault(y, []).append(x)
    fila = list(conhecidas)
    for x in defs:
        if x not in conhecidas and precisa[x] == 0:
            conhecidas.add(x)
            fila.append(x)
    while fila:
        y = fila.pop()
        for x in usado_por.get(y, ()):
            if x not in conhecidas:
                tem[x] += 1
                if tem[x] >= precisa[x]:
                    conhecidas.add(x)
                    fila.append(x)
    return conhecidas


def sha(palavras):
    return hashlib.sha256("\n".join(sorted(palavras)).encode()).hexdigest()


def main():
    defs = Dicionario().grafo_de_definicoes()
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "grafo02.txt"), "w", encoding="utf-8") as f:
            for x in sorted(defs):
                f.write(x + "\t" + " ".join(sorted(defs[x])) + "\n")
        return
    usos = {x: 0 for x in defs}
    for s in defs.values():
        for y in s:
            usos[y] += 1
    ancoras = sorted(defs, key=lambda x: (-usos[x], x))[:ANCORAS]
    print(f"palavras = {len(defs)}, arestas = {sum(len(s) for s in defs.values())}")
    print(f"ancoras = {ANCORAS}, sha = {sha(ancoras)}")
    for t in THETAS:
        a, b = fecho_parcial(ancoras, defs, t), fecho_ingenuo(ancoras, defs, t)
        print(f"theta = {t.hex()}: inteiro n = {len(a)} sha = {sha(a)}; ingenuo n = {len(b)} sha = {sha(b)}")


if __name__ == "__main__":
    main()
