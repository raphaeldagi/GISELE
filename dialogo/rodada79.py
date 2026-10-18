"""Rodada 79 do diálogo Python <-> Java (Parte 112): o simplex próprio (regra de Bland) resolvendo um jogo de soma zero 4×5, bit a bit.
A matriz é a fixture da Parte 112: entradas (x mod 11) − 5, x pelo LCG a partir de 112. O jogo é deslocado para valor positivo, e a coluna
resolve max Σw s.a. A·w ≤ 1; a linha sai dos preços duais. Só +, −, ×, ÷ e comparações. Da raiz: python3 dialogo/rodada79.py"""

N, M = 4, 5


def jogo():
    x, A = 112, []
    for _ in range(N):
        linha = []
        for _ in range(M):
            x = (1103515245 * x + 12345) % 2147483648
            linha.append(float(x % 11 - 5))
        A.append(linha)
    return A


def resolver(A):
    menor = A[0][0]
    for linha in A:
        for v in linha:
            if v < menor:
                menor = v
    desloc = 1.0 - menor if menor <= 0.0 else 0.0
    T = []
    for i in range(N):
        T.append([A[i][j] + desloc for j in range(M)] + [1.0 if k == i else 0.0 for k in range(N)] + [1.0])
    obj = [-1.0] * M + [0.0] * N + [0.0]
    base = [M + i for i in range(N)]
    pivos = 0
    while True:
        entra = -1
        for j in range(M + N):
            if obj[j] < 0.0:
                entra = j
                break
        if entra < 0:
            break
        sai = -1
        melhor = 0.0
        for i in range(N):
            if T[i][entra] > 0.0:
                razao = T[i][M + N] / T[i][entra]
                if sai < 0 or razao < melhor or (razao == melhor and base[i] < base[sai]):
                    sai = i
                    melhor = razao
        p = T[sai][entra]
        T[sai] = [v / p for v in T[sai]]
        for i in range(N):
            if i != sai and T[i][entra] != 0.0:
                f = T[i][entra]
                T[i] = [a - f * b for a, b in zip(T[i], T[sai])]
        f = obj[entra]
        obj = [a - f * b for a, b in zip(obj, T[sai])]
        base[sai] = entra
        pivos += 1
    w = [0.0] * M
    for i in range(N):
        if base[i] < M:
            w[base[i]] = T[i][M + N]
    vd = 1.0 / obj[M + N]
    return vd - desloc, [obj[M + i] * vd for i in range(N)], [wj * vd for wj in w], pivos


def main():
    v, p, q, k = resolver(jogo())
    print("valor " + v.hex())
    print("p " + " ".join(x.hex() for x in p))
    print("q " + " ".join(x.hex() for x in q))
    print("pivos " + str(k))
    print("fim")


if __name__ == "__main__":
    main()
