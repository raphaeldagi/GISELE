"""Conta as chamadas de math.exp, math.log e math.pow (e do pow embutido com expoente float) de uma rodada do diálogo em
Python. Uso: python3 dialogo/contar_libm.py RODADA.py [argumentos...]; imprime "exp N log N pow N" na saída de erro."""
import builtins
import math
import runpy
import sys

CONT = {"exp": 0, "log": 0, "pow": 0}


def envolver(nome, f):
    def g(*a):
        CONT[nome] += 1
        return f(*a)
    return g


for nome in ("exp", "log", "pow"):
    setattr(math, nome, envolver(nome, getattr(math, nome)))
_pow = builtins.pow


def pow_contado(*a):
    if len(a) == 2 and isinstance(a[1], float):
        CONT["pow"] += 1
    return _pow(*a)


builtins.pow = pow_contado
caminho = sys.argv[1]
sys.argv = [caminho] + sys.argv[2:]
try:
    runpy.run_path(caminho, run_name="__main__")
finally:
    print(f"exp {CONT['exp']} log {CONT['log']} pow {CONT['pow']}", file=sys.stderr)
