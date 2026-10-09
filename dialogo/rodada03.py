"""Rodada 3 do diálogo Python <-> Java: a avalanche do dicionário. Ancora as palavras em ordem de frequência nas
definições, uma a uma, com o fecho incremental (synthai/dicionario.py, P421), e imprime, para cada θ, o k em que a
cobertura passa de 50% e o maior salto causado por uma palavra. Com `--preparar PASTA`, escreve o grafo
(PASTA/grafo03.txt) e o currículo (PASTA/ordem03.txt) que o Java lê. O tempo vai para a saída de erro (não é comparado).
Rodar da raiz do repositório: python3 dialogo/rodada03.py"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthai.dicionario import Dicionario, fecho_incremental  # noqa: E402

THETAS = (1.0, 0.9, 0.8, 0.7, 0.6)


def main():
    d = Dicionario()
    defs = d.grafo_de_definicoes()
    freq = {}
    for _, _, _, glosa in d.sinsets:
        for w in d.palavras_da_definicao(glosa):
            freq[w] = freq.get(w, 0) + 1
    ordem = sorted(defs, key=lambda x: (-freq.get(x, 0), x))
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "grafo03.txt"), "w", encoding="utf-8") as f:
            for x in sorted(defs):
                f.write(x + "\t" + " ".join(sorted(defs[x])) + "\n")
        with open(os.path.join(sys.argv[2], "ordem03.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(ordem) + "\n")
        return
    n = len(defs)
    for t in THETAS:
        t0 = time.perf_counter()
        cob = fecho_incremental(ordem, defs, t)
        dt = time.perf_counter() - t0
        saltos = [cob[i + 1] - cob[i] for i in range(len(cob) - 1)]
        km = max(range(len(saltos)), key=saltos.__getitem__)
        meio = next((i for i, c in enumerate(cob) if 2 * c >= n), -1)
        print(f"theta = {t.hex()}: k50 = {meio}; maior salto = {saltos[km]} palavras, em k = {km + 1} ({ordem[km]})")
        print(f"tempo python theta {t}: {dt:.3f} s", file=sys.stderr)


if __name__ == "__main__":
    main()
