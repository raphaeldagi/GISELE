"""Rodada 48 do diálogo Python <-> Java: escolher experimentos com orçamento (a U(a) = E[ΔK | a]/Custo(a) do texto recebido na Parte 74). Com `--preparar
PASTA`, o Python grava em PASTA/mochila48.txt as 300 instâncias da P1662 (semente 74): por instância, o orçamento e os 30 experimentos (VOI e H em
hexadecimal, custo inteiro). As duas linguagens calculam o ótimo exato (mochila 0-1 por programação dinâmica nos custos) e os dois gulosos (por VOI/custo e
por H/custo, empates pelo índice), e imprimem os três valores de cada instância e os totais. Rodar da raiz: python3 dialogo/rodada48.py PASTA"""

import math
import os
import random
import sys


def preparar(pasta, instancias=300, itens=30, fracao=0.2, semente=74):
    r = random.Random(semente)  # a mesma sequência de sorteios da calculos.p1662_orcamento
    with open(os.path.join(pasta, "mochila48.txt"), "w") as f:
        for _ in range(instancias):
            vs, hs, cs = [], [], []
            for _ in range(itens):
                p = r.random()
                u = [[r.random(), r.random()], [r.random(), r.random()]]
                com = p * max(u[0][1], u[1][1]) + (1.0 - p) * max(u[0][0], u[1][0])
                sem = max(p * u[0][1] + (1.0 - p) * u[0][0], p * u[1][1] + (1.0 - p) * u[1][0])
                vs.append(max(com - sem, 0.0))
                hs.append(-sum(q * math.log2(q) for q in (p, 1.0 - p) if q > 0.0))
                cs.append(r.randint(1, 20))
            f.write(f"{int(fracao * sum(cs))}\n")
            f.write(" ".join(f"{v.hex()} {h.hex()} {c}" for v, h, c in zip(vs, hs, cs)) + "\n")


def ler(pasta):
    linhas = [l for l in open(os.path.join(pasta, "mochila48.txt")).read().split("\n") if l]
    saida = []
    for k in range(0, len(linhas), 2):
        xs = linhas[k + 1].split()
        saida.append((int(linhas[k]), [float.fromhex(xs[i]) for i in range(0, len(xs), 3)],
                      [float.fromhex(xs[i]) for i in range(1, len(xs), 3)], [int(xs[i]) for i in range(2, len(xs), 3)]))
    return saida


def resolver(B, vs, hs, cs):
    melhor = [0.0] * (B + 1)
    for v, c in zip(vs, cs):
        for b in range(B, c - 1, -1):
            if melhor[b - c] + v > melhor[b]:
                melhor[b] = melhor[b - c] + v

    def guloso(chave):
        resto, total = B, 0.0
        for i in sorted(range(len(vs)), key=lambda i: (-(chave[i] / cs[i]), i)):
            if cs[i] <= resto:
                resto -= cs[i]
                total += vs[i]
        return total
    return melhor[B], guloso(vs), guloso(hs)


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        preparar(sys.argv[2])
        return
    so = s1 = s2 = 0.0
    otimos = 0
    for k, (B, vs, hs, cs) in enumerate(ler(sys.argv[1])):
        ot, g1, g2 = resolver(B, vs, hs, cs)
        so += ot
        s1 += g1
        s2 += g2
        otimos += g1 >= ot - 1e-12
        print(f"instancia {k}: otimo {ot.hex()} guloso_voi {g1.hex()} guloso_h {g2.hex()}")
    print(f"totais: otimo {so.hex()} guloso_voi {s1.hex()} guloso_h {s2.hex()} guloso_otimo_em {otimos}")


if __name__ == "__main__":
    main()
