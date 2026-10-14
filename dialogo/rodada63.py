"""Rodada 63 do diálogo Python <-> Java (Parte 96): a conexão residual + a normalização de camada (LayerNorm), bit a bit.
Dado x e uma subcamada linear s(x) = W·x + b, calcula o residual y = x + s(x), depois a LayerNorm:
μ = média(y), var = média((y−μ)²), ŷ = (y−μ)/√(var+ε), out = γ·ŷ + β. TUDO é + − × ÷ e √ (exatos no IEEE) —
NENHUM transcendental: a fronteira da Parte 52 (o exp) não aparece aqui. Pesos/entrada fixos. Rodar da raiz: python3 dialogo/rodada63.py"""

import math

D = 4
X = [0.5, -1.2, 0.8, 0.3]
W = [[0.2, -0.1, 0.4, 0.0], [0.3, 0.5, -0.2, 0.1], [-0.4, 0.1, 0.6, -0.3], [0.1, -0.2, 0.0, 0.5]]
B = [0.1, -0.1, 0.2, 0.0]
GAMMA = [1.1, 0.9, 1.0, 1.2]
BETA = [0.0, 0.1, -0.1, 0.05]
EPS = 1e-5


def subcamada(x):
    out = []
    for i in range(D):
        s = 0.0
        for k in range(D):
            s = s + W[i][k] * x[k]
        out.append(s + B[i])
    return out


def layernorm_residual():
    s = subcamada(X)
    y = [X[i] + s[i] for i in range(D)]           # conexão residual
    soma = 0.0
    for v in y:
        soma = soma + v
    mu = soma / D
    sq = 0.0
    for v in y:
        sq = sq + (v - mu) * (v - mu)
    var = sq / D
    inv = 1.0 / math.sqrt(var + EPS)
    return [GAMMA[i] * ((y[i] - mu) * inv) + BETA[i] for i in range(D)]


def main():
    out = layernorm_residual()
    for i in range(D):
        print(f"out {i} {out[i].hex()}")
    print("fim")


if __name__ == "__main__":
    main()
