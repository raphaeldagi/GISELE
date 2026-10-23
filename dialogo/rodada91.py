"""Rodada 91 do diálogo Python <-> Java (Parte 136): a descida do gradiente de synthai.passos (os passos do módulo recebido
inovacao_guiada.py: fixo, secante de Barzilai-Borwein protegida, média exponencial do gradiente e limite da norma), bit a bit.
A = I + MᵀM/(2d) com M de um LCG, partida do mesmo LCG, d = 6, 24 passos. Imprime os 25 custos de cada método em hexadecimal.
Da raiz: python3 dialogo/rodada91.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from synthai.passos import descer  # noqa: E402

D = 6
SEMENTE = 9136


def dados():
    x = SEMENTE
    def u():
        nonlocal x
        x = (1103515245 * x + 12345) % 2147483648
        return 2.0 * (x / 2147483648.0) - 1.0
    M = [[u() for _ in range(D)] for _ in range(D)]
    A = []
    for i in range(D):
        linha = []
        for j in range(D):
            t = 0.0
            for k in range(D):
                t += M[k][i] * M[k][j]
            linha.append((1.0 if i == j else 0.0) + t / (2.0 * D))
        A.append(linha)
    x0 = [u() for _ in range(D)]
    return A, x0


def main():
    A, x0 = dados()
    alvo = [0.0] * D
    casos = (("fixo", dict(metodo="fixo", passo=0.05)), ("secante", dict(metodo="secante", passo=0.05)),
             ("media", dict(metodo="media", passo=0.05, beta=0.6)), ("limite", dict(metodo="fixo", passo=0.3, limite=0.05)))
    for nome, kw in casos:
        for t, c in enumerate(descer(A, x0, alvo, 24, **kw)):
            print(nome + " " + str(t) + " " + c.hex())
    print("fim")


if __name__ == "__main__":
    main()
