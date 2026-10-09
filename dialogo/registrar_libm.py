"""Registra os argumentos DISTINTOS de math.exp e math.log de uma rodada do diálogo em Python (com o valor da glibc).
Uso: python3 dialogo/registrar_libm.py SAIDA RODADA.py [argumentos...]; escreve SAIDA.exp e SAIDA.log, uma linha por
argumento: "argumento_hex valor_hex"."""
import math
import runpy
import sys

ARGS = {"exp": {}, "log": {}}


def envolver(nome, f):
    def g(*a):
        v = f(*a)
        if len(a) == 1:
            ARGS[nome][float(a[0])] = v
        return v
    return g


for nome in ("exp", "log"):
    setattr(math, nome, envolver(nome, getattr(math, nome)))
saida, caminho = sys.argv[1], sys.argv[2]
sys.argv = [caminho] + sys.argv[3:]
try:
    runpy.run_path(caminho, run_name="__main__")
finally:
    for nome in ("exp", "log"):
        with open(f"{saida}.{nome}", "w") as f:
            for x in sorted(ARGS[nome]):
                f.write(f"{x.hex()} {ARGS[nome][x].hex()}\n")
