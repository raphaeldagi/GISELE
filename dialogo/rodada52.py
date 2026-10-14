"""Rodada 52 do diálogo Python <-> Java (Parte 85, pendência da Parte 84): a TRAJETÓRIA INTEIRA de um recozimento, não só uma decisão. Um LCG de 64 bits
gera, a cada passo, a direção (bit de cima) e o u da aceitação (próximos 53 bits de um segundo avanço). Paisagem pequena de 20 estados (parábola + poço em
i=3), T de 2,0 a 0,01 em 300 passos, Metropolis com o exp PRÓPRIO (dialogo/exatas.py). Imprime, a cada passo, i, T e a energia corrente em hexadecimal, e no
fim o melhor i e a melhor energia. Rodar da raiz: python3 dialogo/rodada52.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

M64 = (1 << 64) - 1
N, PASSOS = 20, 300


def energia(i):
    e = 0.01 * ((i - 15) * (i - 15))
    if i == 3:
        e = -5.0
    elif i in (2, 4):
        e = -3.0
    return e


def main():
    lcg = 52
    i = 10
    melhor_i, melhor_e = i, energia(i)
    for k in range(PASSOS):
        T = 2.0 * (0.01 / 2.0) ** (k / (PASSOS - 1))
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & M64
        direcao = 1 if (lcg >> 63) else -1
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & M64
        u = (lcg >> 11) / float(1 << 53)
        j = i + direcao
        if 0 <= j < N:
            dE = energia(j) - energia(i)
            if dE <= 0.0 or u < exp_(-dE / T):
                i = j
        ei = energia(i)
        if ei < melhor_e:
            melhor_i, melhor_e = i, ei
        print(f"passo {k} i {i} T {T.hex()} E {ei.hex()}")
    print(f"melhor: i {melhor_i} E {melhor_e.hex()}")


if __name__ == "__main__":
    main()
