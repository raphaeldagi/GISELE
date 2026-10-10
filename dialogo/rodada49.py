"""Rodada 49 do diálogo Python <-> Java: o valor de um conjunto de experimentos dependentes (P1841, P1842). Com `--preparar PASTA`, o Python grava em
PASTA/sensores49.txt as 300 instâncias da semente 80 (p, as 4 utilidades e as 6 acurácias em hexadecimal; os 6 custos inteiros), na mesma sequência de
sorteios da calculos.p1842_conjuntos. As duas linguagens calculam o VOI de cada conjunto (enumerando as respostas, com o conjunto em ordem crescente), o ótimo
dentro do orçamento 6 e os dois gulosos (olhar 1 e 2, com os mesmos desempates), e imprimem, por instância, o ótimo, os dois valores gulosos e os conjuntos
escolhidos, e os totais. Só + − × ÷ e comparações. Rodar da raiz: python3 dialogo/rodada49.py PASTA"""

import os
import random
import sys

K, ORC = 6, 6


def preparar(pasta, instancias=300, semente=80):
    r = random.Random(semente)
    with open(os.path.join(pasta, "sensores49.txt"), "w") as f:
        for _ in range(instancias):
            p = r.random()
            u = [[r.random(), r.random()], [r.random(), r.random()]]
            qs = [0.55 + 0.4 * r.random() for _ in range(K)]
            cs = [r.randint(1, 5) for _ in range(K)]
            f.write(" ".join(x.hex() for x in [p, u[0][0], u[0][1], u[1][0], u[1][1]] + qs) + " " + " ".join(str(c) for c in cs) + "\n")


def ler(pasta):
    saida = []
    for l in open(os.path.join(pasta, "sensores49.txt")).read().split("\n"):
        if l:
            xs = l.split()
            v = [float.fromhex(x) for x in xs[:5 + K]]
            saida.append((v[0], [[v[1], v[2]], [v[3], v[4]]], v[5:], [int(x) for x in xs[5 + K:]]))
    return saida


def voi(p, u, qs, conj):
    sem = max(p * u[a][1] + (1 - p) * u[a][0] for a in (0, 1))
    total = 0.0
    for m in range(1 << len(conj)):
        l1, l0 = p, 1 - p
        for b, i in enumerate(conj):
            if (m >> b) & 1:
                l1 *= qs[i]
                l0 *= 1 - qs[i]
            else:
                l1 *= 1 - qs[i]
                l0 *= qs[i]
        total += max(l1 * u[a][1] + l0 * u[a][0] for a in (0, 1))
    return max(total - sem, 0.0)


def resolver(p, u, qs, cs):
    memo = {}

    def v(c):
        c = tuple(sorted(c))
        if c not in memo:
            memo[c] = voi(p, u, qs, c)
        return memo[c]
    ot = 0.0
    for m in range(1 << K):
        if sum(cs[i] for i in range(K) if m >> i & 1) <= ORC:
            x = v([i for i in range(K) if m >> i & 1])
            if x > ot:
                ot = x
    saidas = []
    for olhar in (1, 2):
        esc, resto = [], ORC
        while True:
            idx = [i for i in range(K) if i not in esc and cs[i] <= resto]
            if not idx:
                break
            melhor, j = -1.0, -1
            for i in idx:
                g = (v(esc + [i]) - v(esc)) / cs[i]
                if g > melhor:
                    melhor, j = g, i
            if melhor <= 1e-15:
                if olhar < 2:
                    break
                mp, pi, pj = -1.0, -1, -1
                for i in idx:
                    for jj in idx:
                        if i < jj and cs[i] + cs[jj] <= resto:
                            g = (v(esc + [i, jj]) - v(esc)) / (cs[i] + cs[jj])
                            if g > mp:
                                mp, pi, pj = g, i, jj
                if pi < 0 or mp <= 1e-15:
                    break
                esc += [pi, pj]
                resto -= cs[pi] + cs[pj]
                continue
            esc.append(j)
            resto -= cs[j]
        saidas.append((v(esc), sorted(esc)))
    return ot, saidas


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        preparar(sys.argv[2])
        return
    so = s1 = s2 = 0.0
    for k, (p, u, qs, cs) in enumerate(ler(sys.argv[1])):
        ot, ((g1, e1), (g2, e2)) = resolver(p, u, qs, cs)
        so += ot
        s1 += g1
        s2 += g2
        print(f"instancia {k}: otimo {ot.hex()} guloso1 {g1.hex()} {e1} guloso2 {g2.hex()} {e2}".replace(", ", ","))
    print(f"totais: otimo {so.hex()} guloso1 {s1.hex()} guloso2 {s2.hex()}")


if __name__ == "__main__":
    main()
