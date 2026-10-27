"""Rodada 105 do diálogo Python <-> Java (Parte 157): o expoente de Zipf por máxima verossimilhança de synthai.zipf_mle.mle, bit a bit. Contagens fixas
c_r = ⌊1000/r⌋ em N = 50 postos; o alvo (1/n) Σ c_r ln r; a bisseção em [0,01; 5] com 60 passos fixos sobre E_s[ln r] = Σ w_r ln r / Σ w_r, w_r = e^(−s ln r),
com o exp e o log PRÓPRIOS da rodada 26 (r^−s pela pow da libm seria a fronteira da Parte 52) e somas em laço. Confere contra o módulo (1e-9) antes de
imprimir. Da raiz: python3 dialogo/rodada105.py"""
import importlib.util
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
_spec = importlib.util.spec_from_file_location("rodada26", os.path.join(AQUI, "rodada26.py"))
r26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r26)
exp_, log_ = r26.exp_, r26.log_
from synthai import zipf_mle  # noqa: E402

N = 50


def main():
    c = [1000 // r for r in range(1, N + 1)]
    lr = [log_(float(r)) for r in range(1, N + 1)]
    n = 0
    soma = 0.0
    for k in range(N):
        n += c[k]
        soma += c[k] * lr[k]
    alvo = soma / n
    lo, hi = 0.01, 5.0
    for _ in range(60):
        m = (lo + hi) / 2
        num = den = 0.0
        for k in range(N):
            w = exp_(-m * lr[k])
            num += w * lr[k]
            den += w
        if num / den > alvo:
            lo = m
        else:
            hi = m
    s = (lo + hi) / 2
    assert abs(s - zipf_mle.mle(c)) < 1e-9
    print("alvo " + alvo.hex())
    print("s " + s.hex())
    print("conferido True")
    print("fim")


if __name__ == "__main__":
    main()
