"""Sonda da Parte 105: mede se sin/cos/tan/atan2 da libm divergem entre Python e Java (a 6ª face da fronteira da Parte 52?).
10 000 argumentos determinísticos x = k/1000, k = 1..10000 (cobrindo [0,001; 10], que cruza π/2, π, 3π/2 — onde tan estoura).
Imprime, por argumento, uma linha por função com o hexadecimal da libm. NÃO é rodada do diálogo (não casa com rodada[0-9]*.py;
o auditor p1722 não a varre): é um experimento de medição. A comparação com o Java é feita por prefixo (sin/cos/tan/atan2),
contando as divergências de cada função. Da raiz: python3 dialogo/sonda_transc_105.py"""

import math

N = 10000


def main():
    linhas = []
    for k in range(1, N + 1):
        x = k / 1000.0
        linhas.append("sin " + math.sin(x).hex())
        linhas.append("cos " + math.cos(x).hex())
        linhas.append("tan " + math.tan(x).hex())
        linhas.append("atan2 " + math.atan2(x, 1.0).hex())
    print("\n".join(linhas))
    print("fim")


if __name__ == "__main__":
    main()
