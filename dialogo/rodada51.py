"""Rodada 51 do diálogo Python <-> Java (Parte 84): a decisão de aceitar um passo no recozimento simulado (Metropolis), bit a bit. "Delírio" = aceitar
uma piora com probabilidade exp(-ΔE/T); a decisão depende de exp (a fronteira da Parte 52), então usa o exp PRÓPRIO (dialogo/exatas.py). O sorteio é o
mesmo nas duas linguagens: um LCG de 64 bits dá um u em [0,1) por (u >> 11) / 2^53. Para 400 casos (ΔE em hexadecimal, T em hexadecimal, u do LCG), imprime
exp(-ΔE/T) em hexadecimal e a decisão (1 aceita, 0 recusa), e os totais. Papéis: a IA-Python pergunta/ensina (como na maioria das rodadas). Rodar da raiz:
python3 dialogo/rodada51.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

M64 = (1 << 64) - 1


def decisao(dE, T, u):
    if dE <= 0.0:
        return 1.0, 1
    p = exp_(-dE / T)
    return p, 1 if u < p else 0


def main():
    lcg = 51
    aceitos = 0
    soma_p = 0.0
    for k in range(400):
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & M64
        u = (lcg >> 11) / float(1 << 53)
        dE = (k - 200) / 50.0  # de -4 a +4
        T = 0.5 + (k % 20) / 10.0  # de 0,5 a 2,4
        p, ac = decisao(dE, T, u)
        soma_p += p
        aceitos += ac
        print(f"caso {k} dE {dE.hex()} T {T.hex()} u {u.hex()} p {p.hex()} aceita {ac}")
    print(f"totais: aceitos {aceitos} soma_p {soma_p.hex()}")


if __name__ == "__main__":
    main()
