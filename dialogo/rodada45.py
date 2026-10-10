"""Rodada 45 do diálogo Python <-> Java: os autovalores da atenção. Com `--preparar PASTA`, o Python pré-treina um GPT (synthai/gpt.py; d = 16, T = 16,
h = 32, 2.000 passos nas definições inglesas, semente 71) e grava W_Q e W_K em PASTA/qk45.txt (hexadecimal). Depois, as duas linguagens calculam
M = W_Q W_Kᵀ, MᵀM, os autovalores por Jacobi clássico (só + − × ÷ e √, na mesma ordem) e a razão de participação. Rodar da raiz: python3 dialogo/rodada45.py PASTA"""

import math
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)


def preparar(pasta):
    import calculos
    from synthai.gpt import GPT
    treino, _ = calculos.p1511_corpus_de_glosas("en")
    g = GPT(calculos.VOCAB_GPT, T=16, d=16, h=32, semente=71)
    g.treinar(treino, passos=2000, lr=0.005, semente=71)
    with open(os.path.join(pasta, "qk45.txt"), "w") as f:
        for nome in ("Q", "K"):
            for linha in g.p[nome]:
                f.write(" ".join(x.hex() for x in linha) + "\n")


def ler(pasta):
    linhas = [l for l in open(os.path.join(pasta, "qk45.txt")).read().split("\n") if l]
    d = len(linhas) // 2
    Q = [[float.fromhex(x) for x in l.split()] for l in linhas[:d]]
    K = [[float.fromhex(x) for x in l.split()] for l in linhas[d:]]
    return Q, K


def jacobi(S, varreduras=60):
    n = len(S)
    A = [list(l) for l in S]
    for _ in range(varreduras):
        fora = 0.0
        for p in range(n):
            for q in range(p + 1, n):
                fora += A[p][q] * A[p][q]
        if fora == 0.0:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if A[p][q] == 0.0:
                    continue
                tau = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if tau >= 0.0 else -1.0) / (abs(tau) + math.sqrt(tau * tau + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
    return sorted((A[i][i] for i in range(n)), reverse=True)


def participacao(Q, K):
    d = len(Q)
    M = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(d):
            s = 0.0
            for k in range(d):
                s += Q[i][k] * K[j][k]
            M[i][j] = s
    MtM = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(d):
            s = 0.0
            for k in range(d):
                s += M[k][i] * M[k][j]
            MtM[i][j] = s
    lam = [x if x > 0.0 else 0.0 for x in jacobi(MtM)]
    s2 = s4 = 0.0
    for x in lam:
        s2 += x
        s4 += x * x
    return s2 * s2 / s4, lam[0] / s2, lam


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        preparar(sys.argv[2])
        return
    pr, frac, lam = participacao(*ler(sys.argv[1]))
    print("autovalores de MtM: " + " ".join(x.hex() for x in lam))
    print(f"PR={pr.hex()} fracao_maior={frac.hex()}")


if __name__ == "__main__":
    main()
