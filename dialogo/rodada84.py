"""Rodada 84 do diálogo Python <-> Java (Parte 117): as camadas contrapostas com MATRIZES. W (4×4, de um LCG inteiro) e W⁻¹ (Gauss-Jordan com
pivô parcial) alternadas em 10 camadas; o produto J = W⁻¹W⋯W⁻¹W e o seu desvio da identidade. Só +, −, ×, ÷ na mesma ordem. Bit a bit.
Da raiz: python3 dialogo/rodada84.py"""

D, L = 4, 10


def matriz():
    x = 117
    W = []
    for i in range(D):
        linha = []
        for j in range(D):
            x = (1103515245 * x + 12345) % 2147483648
            linha.append((x % 2001 - 1000) / 500.0)
        W.append(linha)
    return W


def inversa(A):
    d = len(A)
    M = [[A[i][j] for j in range(d)] + [1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for c in range(d):
        p = c
        for r in range(c + 1, d):
            if abs(M[r][c]) > abs(M[p][c]):
                p = r
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [v / piv for v in M[c]]
        for r in range(d):
            if r != c:
                f = M[r][c]
                if f != 0.0:
                    M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [linha[d:] for linha in M]


def matmul(A, B):
    C = [[0.0] * D for _ in range(D)]
    for i in range(D):
        for k in range(D):
            a = A[i][k]
            if a != 0.0:
                for j in range(D):
                    C[i][j] += a * B[k][j]
    return C


def cadeia():
    W = matriz()
    Wi = inversa(W)
    J = [[1.0 if i == j else 0.0 for j in range(D)] for i in range(D)]
    for k in range(L):
        J = matmul(W if k % 2 == 0 else Wi, J)
    desvio = 0.0
    for i in range(D):
        for j in range(D):
            e = abs(J[i][j] - (1.0 if i == j else 0.0))
            if e > desvio:
                desvio = e
    return Wi, J, desvio


def main():
    Wi, J, desvio = cadeia()
    print("Winv " + " ".join(v.hex() for l in Wi for v in l))
    print("J " + " ".join(v.hex() for l in J for v in l))
    print("desvio " + desvio.hex())
    print("fim")


if __name__ == "__main__":
    main()
