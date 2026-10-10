"""Rodada 21 do diálogo Python <-> Java: a série é um ciclo? Semelhança entre as seções do resultados.txt (palavras da
Rodada 19, como conjuntos): cosseno dos vetores binários pesados por idf = ln(K/df). Imprime a semelhança da última seção
com cada uma, as médias por distância 1 e 20 e o índice do ciclo (média com 1-10 / média com 11-30). Com `--preparar PASTA`,
escreve PASTA/secoes21.txt (parte TAB palavras ordenadas), que o Java lê. Rodar da raiz: python3 dialogo/rodada21.py"""

import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("rodada19", os.path.join(AQUI, "rodada19.py"))
r19 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r19)


def conjuntos():
    docs, sec = r19.documentos(), r19.secoes()
    return [(n, sorted(r19.numeros(sec[n]))) for n in sorted(k for k in docs if k in sec)]


def semelhancas(cs):
    K = len(cs)
    df = {}
    for _, ws in cs:
        for w in ws:
            df[w] = df.get(w, 0) + 1
    idf2 = {w: math.log(K / c) ** 2 for w, c in df.items()}
    norma = []
    for _, ws in cs:
        t = 0.0
        for w in ws:
            t += idf2[w]
        norma.append(t)
    sim = [[0.0] * K for _ in range(K)]
    for i in range(K):
        a = set(cs[i][1])
        for j in range(K):
            t = 0.0
            for w in cs[j][1]:
                if w in a:
                    t += idf2[w]
            sim[i][j] = t / math.sqrt(norma[i] * norma[j]) if norma[i] > 0 and norma[j] > 0 else 0.0
    return sim


def media_distancia(sim, L):
    t, n = 0.0, 0
    for i in range(len(sim) - L):
        t += sim[i][i + L]
        n += 1
    return t / n


def indice(sim, cs):
    pos = {n: i for i, (n, _) in enumerate(cs)}
    u = len(cs) - 1
    com = lambda a, b: [sim[u][pos[k]] for k in range(a, b + 1) if k in pos]
    c, m = com(1, 10), com(11, 30)
    tc = tm = 0.0
    for x in c:
        tc += x
    for x in m:
        tm += x
    return (tc / len(c)) / (tm / len(m))


def main():
    cs = conjuntos()
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "secoes21.txt"), "w", encoding="ascii") as f:
            for n, ws in cs:
                f.write(f"{n}\t{' '.join(ws)}\n")
        return
    sim = semelhancas(cs)
    u = len(cs) - 1
    for j, (n, _) in enumerate(cs):
        print(f"sim(parte {cs[u][0]}, parte {n}) = {sim[u][j].hex()}")
    print(f"media a distancia 1 = {media_distancia(sim, 1).hex()}; a distancia 20 = {media_distancia(sim, 20).hex()}")
    print(f"indice do ciclo = {indice(sim, cs).hex()}")


if __name__ == "__main__":
    main()
