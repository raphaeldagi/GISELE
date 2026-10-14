"""Rodada 57 do diálogo Python <-> Java (Parte 90, pendência da Parte 89): uma rede de Izhikevich acoplada que APRENDE por STDP — os pesos W mudam pela ordem
dos disparos, com o exp PRÓPRIO (dialogo/exatas.py, regra da Parte 52). 6 neurônios RS; a corrente de cada um é a externa mais a soma dos pesos vezes 1 quando
o vizinho disparou no passo anterior; a STDP de pares (potenciacao pre->pos, depressao dominante) atualiza W a cada disparo, com limites [0, wmax]. Só +, −, ×
e o exp próprio; a ordem das somas é fixa. 300 passos de 0,5 ms. Imprime, por passo, v de cada neurônio; no fim, a matriz W (hex) e o total de disparos. Rodar
da raiz: python3 dialogo/rodada57.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

N, PASSOS, DT, I_EXT = 6, 300, 0.5, 5.0
A_MAIS, A_MENOS, TAU, WMAX = 0.002, 0.0022, 20.0, 1.0
W0 = [[0.0, 0.3, 0.0, 0.0, 0.2, 0.0],
      [0.0, 0.0, 0.4, 0.0, 0.0, 0.0],
      [0.2, 0.0, 0.0, 0.3, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.5, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, 0.3],
      [0.4, 0.0, 0.0, 0.0, 0.0, 0.0]]


def simular(imprimir=False):
    v = [-65.0] * N
    u = [0.2 * -65.0] * N
    disparou = [0] * N
    ult = [-1.0e9] * N  # ultimo tempo de disparo de cada neuronio
    W = [linha[:] for linha in W0]
    total = 0
    for k in range(PASSOS):
        t = k * DT
        correntes = []
        for i in range(N):
            acopl = 0.0
            for j in range(N):
                acopl = acopl + W[i][j] * disparou[j]
            correntes.append(I_EXT + acopl)
        novo_disp = [0] * N
        for i in range(N):
            ii = correntes[i]
            v[i] = v[i] + (DT / 2.0) * (0.04 * v[i] * v[i] + 5.0 * v[i] + 140.0 - u[i] + ii)
            v[i] = v[i] + (DT / 2.0) * (0.04 * v[i] * v[i] + 5.0 * v[i] + 140.0 - u[i] + ii)
            u[i] = u[i] + DT * 0.02 * (0.2 * v[i] - u[i])
            if v[i] >= 30.0:
                v[i] = -65.0
                u[i] = u[i] + 8.0
                novo_disp[i] = 1
                total = total + 1
        # STDP: para cada neuronio i que disparou agora (pos), potencia W[i][j] com pre j recente;
        # e deprime W[k][i] (i como pre) com pos k recente anterior.
        for i in range(N):
            if novo_disp[i]:
                for j in range(N):
                    if W0[i][j] > 0.0 and ult[j] > -1.0e8:
                        d = t - ult[j]  # pre j antes do pos i: d>0 potencia
                        if 0.0 <= d:
                            nw = W[i][j] + A_MAIS * exp_(-d / TAU)
                            W[i][j] = nw if nw < WMAX else WMAX
                for kk in range(N):
                    if W0[kk][i] > 0.0 and ult[kk] > -1.0e8:
                        d = ult[kk] - t  # pos kk antes do pre i (agora): d<=0 deprime
                        nw = W[kk][i] - A_MENOS * exp_(d / TAU)
                        W[kk][i] = nw if nw > 0.0 else 0.0
                ult[i] = t
        disparou = novo_disp
        if imprimir:
            for i in range(N):
                print(f"passo {k} n {i} v {v[i].hex()}")
    if imprimir:
        for i in range(N):
            for j in range(N):
                if W0[i][j] > 0.0:
                    print(f"W {i} {j} {W[i][j].hex()}")
        print(f"disparos: {total}")
    soma_w = sum(W[i][j] for i in range(N) for j in range(N))
    soma_w0 = sum(W0[i][j] for i in range(N) for j in range(N))
    return total, soma_w, soma_w0


def main():
    simular(imprimir=True)


if __name__ == "__main__":
    main()
