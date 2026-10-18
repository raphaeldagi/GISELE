"""Rodada 81 do diálogo Python <-> Java (Parte 114): a rede LINEAR profunda (DL lido como ML), treinada por descida do gradiente, bit a bit.
f(x) = W₂(W₁x), d = 3 (x₁, x₂, 1), h = 4, n = 50 pontos e a inicialização tirados de um LCG inteiro; 500 passos de GD com lr 0,02.
Imprime o produto β = W₂W₁ (que converge para o OLS). Só +, −, ×, ÷ em laços sequenciais. Da raiz: python3 dialogo/rodada81.py"""

D, H, N, PASSOS, LR = 3, 4, 50, 500, 0.02


def lcg(x):
    return (x * 1103515245 + 12345) % 2147483648


def dados():
    x = 81
    X, y = [], []
    for _ in range(N):
        x = lcg(x)
        a = float(x % 2001 - 1000) / 1000.0
        x = lcg(x)
        b = float(x % 2001 - 1000) / 1000.0
        x = lcg(x)
        ruido = float(x % 201 - 100) / 1000.0
        X.append([a, b, 1.0])
        y.append(0.7 * a - 0.3 * b + 0.1 + ruido)
    W1, W2 = [], []
    for _ in range(H):
        linha = []
        for _ in range(D):
            x = lcg(x)
            linha.append(float(x % 201 - 100) / 1000.0)
        W1.append(linha)
    for _ in range(H):
        x = lcg(x)
        W2.append(float(x % 201 - 100) / 1000.0)
    return X, y, W1, W2


def treinar():
    X, y, W1, W2 = dados()
    for _ in range(PASSOS):
        g1 = [[0.0] * D for _ in range(H)]
        g2 = [0.0] * H
        for i in range(N):
            a = [0.0] * H
            for k in range(H):
                s = 0.0
                for j in range(D):
                    s = s + W1[k][j] * X[i][j]
                a[k] = s
            r = 0.0
            for k in range(H):
                r = r + W2[k] * a[k]
            r = r - y[i]
            for k in range(H):
                g2[k] = g2[k] + 2.0 * r * a[k] / N
                for j in range(D):
                    g1[k][j] = g1[k][j] + 2.0 * r * W2[k] * X[i][j] / N
        for k in range(H):
            W2[k] = W2[k] - LR * g2[k]
            for j in range(D):
                W1[k][j] = W1[k][j] - LR * g1[k][j]
    beta = []
    for j in range(D):
        s = 0.0
        for k in range(H):
            s = s + W2[k] * W1[k][j]
        beta.append(s)
    return beta


def main():
    print("beta " + " ".join(b.hex() for b in treinar()))
    print("fim")


if __name__ == "__main__":
    main()
