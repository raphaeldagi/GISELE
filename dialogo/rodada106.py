"""Rodada 106 do diálogo Python <-> Java (Parte 158): o α de máxima verossimilhança da lei de potência das frequências de synthai.zipf_frequencias, bit a bit.
Frequências fixas x_i = ⌊1000/i⌋ (i = 1..60), as ≥ x_min = 2; ζ(a, x_min) e Σ k^−a ln k por soma direta até x_min + K − 1 (K = 200) e o resto de Euler–Maclaurin;
k^−a = e^(−a ln k) com o exp e o log PRÓPRIOS da rodada 26; bisseção em [1,05; 6] com 60 passos fixos. Confere contra o módulo (1e-7) antes de imprimir.
Da raiz: python3 dialogo/rodada106.py"""
import importlib.util
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
_spec = importlib.util.spec_from_file_location("rodada26", os.path.join(AQUI, "rodada26.py"))
r26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r26)
exp_, log_ = r26.exp_, r26.log_
from synthai import zipf_frequencias  # noqa: E402

XMIN, K = 2, 200


def media(a):
    z = d = 0.0
    for k in range(XMIN, XMIN + K):
        lk = log_(float(k))
        w = exp_(-a * lk)
        z += w
        d += w * lk
    N = XMIN + K
    lN = log_(float(N))
    wN = exp_(-a * lN)
    w1 = exp_((1.0 - a) * lN)
    w2 = exp_((-a - 1.0) * lN)
    z += w1 / (a - 1.0) + wN / 2.0 + a * w2 / 12.0
    d += w1 * (lN / (a - 1.0) + 1.0 / ((a - 1.0) * (a - 1.0))) + wN * lN / 2.0 - w2 * (1.0 - a * lN) / 12.0
    return d / z


def main():
    xs = [1000 // i for i in range(1, 61)]
    xs = [x for x in xs if x >= XMIN]
    soma = 0.0
    for x in xs:
        soma += log_(float(x))
    alvo = soma / len(xs)
    lo, hi = 1.05, 6.0
    for _ in range(60):
        m = (lo + hi) / 2
        if media(m) > alvo:
            lo = m
        else:
            hi = m
    a = (lo + hi) / 2
    assert abs(a - zipf_frequencias.alfa_mle(xs, XMIN)) < 1e-7
    print("alvo " + alvo.hex())
    print("alfa " + a.hex())
    print("conferido True")
    print("fim")


if __name__ == "__main__":
    main()
