"""Rodada 11 do diálogo Python <-> Java: quanto do português se define em português. O grafo de definições da
OpenWordNet-PT (synthai/dicionario.py, DicionarioPT, P641) e o fecho parcial θ = 0,6 a partir das 300 palavras mais usadas
nas glosas (fecho_parcial, P381). Com `--preparar PASTA`, escreve o grafo (PASTA/grafo11.txt) e o currículo
(PASTA/ordem11.txt) que o Java lê. Rodar da raiz do repositório: python3 dialogo/rodada11.py"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthai.dicionario import DicionarioPT, fecho_parcial  # noqa: E402


def main():
    d = DicionarioPT()
    defs = d.grafo_de_definicoes()
    freq = {}
    for s in defs.values():
        for w in s:
            freq[w] = freq.get(w, 0) + 1
    ordem = sorted(freq, key=lambda w: (-freq[w], w))
    todas = set(defs) | set(freq)
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "grafo11.txt"), "w", encoding="utf-8") as f:
            for x in sorted(todas):
                f.write(x + "\t" + " ".join(sorted(defs.get(x, ()))) + "\t" + ("1" if x in defs else "0") + "\n")
        with open(os.path.join(sys.argv[2], "ordem11.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(ordem[:300]) + "\n")
        return
    # o fecho só propaga por palavras com definição; as outras só entram como âncoras
    conhecidas = fecho_parcial(set(ordem[:300]), defs, 0.6)
    definidas = sorted(conhecidas & set(defs))
    print(f"lemas definidos em portugues = {len(defs)}; palavras no grafo = {len(todas)}")
    print(f"entendidos (theta 0,6, 300 ancoras) = {len(definidas)}; sha = {hashlib.sha256(chr(10).join(definidas).encode()).hexdigest()}")


if __name__ == "__main__":
    main()
