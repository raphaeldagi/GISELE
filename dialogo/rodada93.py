"""Rodada 93 do diálogo Python <-> Java (Parte 141): o reservatório e o posto efetivo de synthai.reservatorio (de
externos/pacote3/aprendizagem_continua.py) bit a bit. 64 vetores de 4 dimensões de um LCG; o Reservatorio REAL de 16 com o gerador trocado
por um que tira randrange(n) = int(u·n) do mesmo LCG; o posto efetivo da matriz guardada por Jacobi cíclico, com o exp e o log PRÓPRIOS da
rodada 26 e somas em laço. Confere antes que o posto desta tradução fica a menos de 1e-12 do posto_efetivo do módulo.
Da raiz: python3 dialogo/rodada93.py"""
import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
_spec = importlib.util.spec_from_file_location("rodada26", os.path.join(AQUI, "rodada26.py"))
r26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r26)
exp_, log_ = r26.exp_, r26.log_
from synthai.reservatorio import Reservatorio, posto_efetivo  # noqa: E402

x = 14193


def u():
    global x
    x = (1103515245 * x + 12345) % 2147483648
    return x / 2147483648.0


class LCG:
    def randrange(self, n):
        return int(u() * n)


def jacobi(S):
    d = len(S)
    A = [list(l) for l in S]
    for _ in range(60):
        fora = 0.0
        for i in range(d):
            for j in range(d):
                if i != j:
                    fora += A[i][j] * A[i][j]
        if fora < 1e-300:
            break
        for p in range(d - 1):
            for q in range(p + 1, d):
                if abs(A[p][q]) < 1e-300:
                    continue
                th = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(d):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(d):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted(A[i][i] for i in range(d))


def posto(H):
    n, d = len(H), len(H[0])
    med = []
    for j in range(d):
        t = 0.0
        for l in H:
            t += l[j]
        med.append(t / n)
    Hc = [[l[j] - med[j] for j in range(d)] for l in H]
    Z = []
    for i in range(d):
        linha = []
        for j in range(d):
            t = 0.0
            for k in range(n):
                t += Hc[k][i] * Hc[k][j]
            linha.append(t)
        Z.append(linha)
    s = sorted((math.sqrt(max(v, 0.0)) for v in jacobi(Z)), reverse=True)
    s = [v for v in s if v > 0]
    soma = 0.0
    for v in s:
        soma += v
    h = 0.0
    for v in s:
        h += (v / soma) * log_(v / soma)
    return exp_(-h)


def main():
    res = Reservatorio(16)
    res.rng = LCG()
    for i in range(64):
        res.adicionar((i, [2.0 * u() - 1.0 for _ in range(4)]))
    H = [v for _, v in res.itens]
    p = posto(H)
    assert abs(p - posto_efetivo(H)) < 1e-12
    print("indices " + " ".join(str(i) for i, _ in res.itens))
    print("posto " + p.hex())
    print("fim")


if __name__ == "__main__":
    main()
