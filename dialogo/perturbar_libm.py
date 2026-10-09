"""Roda uma rodada do diálogo em Python com CADA resultado de math.exp e math.log deslocado de um ulp (math.nextafter, para
cima ou para baixo, ao acaso, semente 29). Uso: python3 dialogo/perturbar_libm.py RODADA.py [argumentos...]"""
import math
import random
import runpy
import sys

_rng = random.Random(29)


def envolver(f):
    def g(*a):
        v = f(*a)
        return math.nextafter(v, math.inf if _rng.random() < 0.5 else -math.inf)
    return g


_exp, _log = math.exp, math.log
math.exp, math.log = envolver(_exp), envolver(_log)
caminho = sys.argv[1]
sys.argv = [caminho] + sys.argv[2:]
runpy.run_path(caminho, run_name="__main__")
