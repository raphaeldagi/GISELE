"""Rodada 75 do diálogo Python <-> Java (Parte 108): o minimax de um jogo de soma zero, bit a bit.
Forma fechada do valor/estratégias do jogo 2×2 e o jogo fictício (melhor-resposta por argmax + média corrente). Só +, −, ×, ÷,
argmax e comparações — nenhuma transcendental, portável por construção (Parte 52). Da raiz: python3 dialogo/rodada75.py"""

A = [[1.0, -1.0], [-2.0, 3.0]]
ITER = 500


def valor_fechado():
    (a, b), (c, d) = A
    den = a + d - b - c
    return (a * d - b * c) / den, (d - c) / den, (d - b) / den


def ficticio(iteracoes):
    m, n = 2, 2
    cl = [0, 0]
    cc = [0, 0]
    gcol = [0.0, 0.0]
    glin = [0.0, 0.0]
    cl[0] += 1
    for j in range(n):
        gcol[j] += A[0][j]
    vs = vi = 0.0
    for _ in range(iteracoes):
        jc = 0
        for j in range(1, n):
            if gcol[j] < gcol[jc]:
                jc = j
        cc[jc] += 1
        for i in range(m):
            glin[i] += A[i][jc]
        il = 0
        for i in range(1, m):
            if glin[i] > glin[il]:
                il = i
        cl[il] += 1
        for j in range(n):
            gcol[j] += A[il][j]
        tl = cl[0] + cl[1]
        tc = cc[0] + cc[1]
        vs = max(glin) / tc
        vi = min(gcol) / tl
    return (vs + vi) / 2.0


def main():
    v, p, q = valor_fechado()
    print("valor " + v.hex())
    print("p " + p.hex())
    print("q " + q.hex())
    print("ficticio " + ficticio(ITER).hex())
    print("fim")


if __name__ == "__main__":
    main()
