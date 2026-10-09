"""Compara a saída de uma rodada em Python com a da mesma rodada em Java, BIT A BIT: cada número em hexadecimal das duas
saídas é lido de volta com float.fromhex (que aceita a grafia do Java e a do Python) e comparado por igualdade exata; o
resto do texto tem de ser idêntico. Uso: python3 dialogo/comparar.py saida_python.txt saida_java.txt"""

import re
import sys

HEX = re.compile(r"-?0x[0-9a-fA-F]+(?:\.[0-9a-fA-F]*)?p[+-]?\d+")


def normalizar(linha):
    numeros = [float.fromhex(x) for x in HEX.findall(linha)]
    return HEX.sub("#", linha), numeros


def comparar(a, b):
    la, lb = open(a).read().splitlines(), open(b).read().splitlines()
    if len(la) != len(lb):
        return False, f"número de linhas: {len(la)} contra {len(lb)}"
    numeros = 0
    for x, y in zip(la, lb):
        (tx, nx), (ty, ny) = normalizar(x), normalizar(y)
        if tx != ty or nx != ny:
            return False, f"diferem: {x!r} / {y!r}"
        numeros += len(nx)
    return True, f"{len(la)} linhas e {numeros} números idênticos bit a bit"


if __name__ == "__main__":
    ok, msg = comparar(sys.argv[1], sys.argv[2])
    print(("IGUAIS: " if ok else "DIFERENTES: ") + msg)
    sys.exit(0 if ok else 1)
