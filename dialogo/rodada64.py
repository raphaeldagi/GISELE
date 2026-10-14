"""Rodada 64 do diálogo Python <-> Java (Parte 97): um BLOCO TRANSFORMER completo de 2 camadas, bit a bit.
Cada camada: h = LayerNorm(x + atenção_causal(x)); y = LayerNorm(h + MLP(h)), com o MLP usando ReLU (sem transcendental).
O ÚNICO transcendental do bloco é o exp do softmax da atenção (o exp próprio; a fronteira da Parte 52). Tudo o mais —
produto interno, ReLU, residual, LayerNorm (média/variância/√) — é +−×÷ e √, exatos no IEEE. Pesos e entrada gerados por um
LCG INTEIRO (idêntico nas duas línguas, sem usar nenhuma transcendental para gerá-los). Rodar da raiz: python3 dialogo/rodada64.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

T, D, H, EPS = 3, 4, 4, 1e-5
_M = 2147483648  # 2^31
_estado = [12345]


def _lcg():
    _estado[0] = (1103515245 * _estado[0] + 12345) % _M
    return _estado[0] / _M - 0.5   # em [-0.5, 0.5), divisão idêntica nas duas línguas


def _mat(linhas, colunas):
    return [[_lcg() for _ in range(colunas)] for _ in range(linhas)]


def _vec(n):
    return [_lcg() for _ in range(n)]


def matvec(W, x, b):
    out = []
    for o in range(len(W)):
        s = 0.0
        for k in range(len(x)):
            s = s + W[o][k] * x[k]
        out.append(s + b[o])
    return out


def layernorm(v, gamma, beta):
    soma = 0.0
    for z in v:
        soma = soma + z
    mu = soma / len(v)
    sq = 0.0
    for z in v:
        sq = sq + (z - mu) * (z - mu)
    var = sq / len(v)
    import math
    inv = 1.0 / math.sqrt(var + EPS)
    return [gamma[i] * ((v[i] - mu) * inv) + beta[i] for i in range(len(v))]


def atencao(seq, Wq, Wk, Wv):
    import math
    zero = [0.0] * D
    Q = [matvec(Wq, seq[i], zero) for i in range(T)]
    K = [matvec(Wk, seq[i], zero) for i in range(T)]
    V = [matvec(Wv, seq[i], zero) for i in range(T)]
    escala = math.sqrt(float(D))
    saidas = []
    for i in range(T):
        e = []
        for j in range(i + 1):
            dot = 0.0
            for k in range(D):
                dot = dot + Q[i][k] * K[j][k]
            e.append(dot / escala)
        m = e[0]
        for x in e:
            if x > m:
                m = x
        ex = [exp_(x - m) for x in e]
        s = 0.0
        for x in ex:
            s = s + x
        p = [x / s for x in ex]
        o = [0.0] * D
        for j in range(i + 1):
            for k in range(D):
                o[k] = o[k] + p[j] * V[j][k]
        saidas.append(o)
    return saidas


def relu(x):
    return x if x > 0.0 else 0.0


def camada(seq, P):
    Wq, Wk, Wv, W1, b1, W2, b2, g1, be1, g2, be2 = P
    attn = atencao(seq, Wq, Wk, Wv)
    h = [layernorm([seq[i][k] + attn[i][k] for k in range(D)], g1, be1) for i in range(T)]
    saida = []
    for i in range(T):
        oculto = [relu(v) for v in matvec(W1, h[i], b1)]
        mlp = matvec(W2, oculto, b2)
        saida.append(layernorm([h[i][k] + mlp[k] for k in range(D)], g2, be2))
    return saida


def _params():
    return [_mat(D, D), _mat(D, D), _mat(D, D), _mat(H, D), _vec(H), _mat(D, H), _vec(D), _vec(D), _vec(D), _vec(D), _vec(D)]


def rodar():
    _estado[0] = 12345
    seq = [_vec(D) for _ in range(T)]
    P1 = _params()
    P2 = _params()
    Wo = _mat(2, D)
    bo = _vec(2)
    seq = camada(seq, P1)
    seq = camada(seq, P2)
    logits = matvec(Wo, seq[T - 1], bo)
    arg = 0 if logits[0] >= logits[1] else 1
    return seq, logits, arg


def main():
    seq, logits, arg = rodar()
    for i in range(T):
        for k in range(D):
            print(f"pos {i} dim {k} {seq[i][k].hex()}")
    for k in range(2):
        print(f"logit {k} {logits[k].hex()}")
    print(f"decisao {arg}")
    print("fim")


if __name__ == "__main__":
    main()
