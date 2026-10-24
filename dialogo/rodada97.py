"""Rodada 97 do diálogo Python <-> Java (Parte 149): o quantil t de Student de calculos.p3200_t_student_quantil bit a bit. A densidade é
c · exp(−(ν+1)/2 · log(1 + s²/ν)) com o exp e o log PRÓPRIOS da rodada 26 (a libm e a pow são fronteira, Parte 52); a constante
c = R(ν)/√(νπ), com R(ν) = Γ((ν+1)/2)/Γ(ν/2) pela recorrência R(ν + 2) = R(ν)·(ν + 1)/ν, R(1) = 1/√π, R(2) = √π/2 (sem lgamma). CDF por Simpson
com 2.000 intervalos (soma em laço, Parte 34), quantil 0,95 por 80 bissecções em [0, 50]. Antes de imprimir, confere que o quantil desta tradução
fica a menos de 1e-9 do da função medida (que usa lgamma e pow). Da raiz: python3 dialogo/rodada97.py"""
import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
_spec = importlib.util.spec_from_file_location("rodada26", os.path.join(AQUI, "rodada26.py"))
r26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r26)
exp_, log_ = r26.exp_, r26.log_


def razao_gama(nu):
    r = 1.0 / math.sqrt(math.pi) if nu % 2 == 1 else math.sqrt(math.pi) / 2.0
    k = 1 if nu % 2 == 1 else 2
    while k < nu:
        r = r * (k + 1.0) / k
        k += 2
    return r


def cdf(x, nu, c, n=2000):
    e = -((nu + 1.0) / 2.0)

    def f(s):
        return c * exp_(e * log_(1.0 + s * s / nu))
    h = x / n
    acc = f(0.0) + f(x)
    for i in range(1, n):
        acc += (4.0 if i % 2 == 1 else 2.0) * f(i * h)
    return 0.5 + acc * h / 3.0


def quantil(nu, q=0.95):
    c = razao_gama(nu) / math.sqrt(nu * math.pi)
    lo, hi = 0.0, 50.0
    for _ in range(80):
        m = (lo + hi) / 2.0
        if cdf(m, nu, c) < q:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2.0, c


def main():
    import calculos
    for nu in (2, 7, 19, 27):
        t, c = quantil(nu)
        assert abs(t - calculos.p3200_t_student_quantil(nu)) < 1e-9
        print("nu" + str(nu) + " c " + c.hex() + " t " + t.hex())
    print("conferido True")
    print("fim")


if __name__ == "__main__":
    main()
