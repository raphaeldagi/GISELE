"""Rodada 13 do diálogo Python <-> Java: uma fronteira atacada de propósito, o arquivo binário. A crença de um
ThompsonDescontado (synthai/decisao.py, γ = 0,99; 10 braços em rodízio, 500 recompensas do gerador da rodada 5, semente
1313) é gravada como 'SYN1' + k (int32) + a[0..k) + b[0..k) (float64), tudo little-endian. Com `--preparar PASTA`,
grava PASTA/pesos_py.bin; o Java lê esse arquivo, confere e grava PASTA/pesos_java.bin; depois `rodada13.py PASTA` lê o
do Java. Rodar da raiz do repositório: python3 dialogo/rodada13.py PASTA"""

import hashlib
import os
import random
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rodada05 import LCG  # noqa: E402
from synthai.decisao import ThompsonDescontado  # noqa: E402

K = 10


def crenca():
    g = LCG(1313)
    t = ThompsonDescontado(K, random.Random(0), gama=0.99)
    for passo in range(500):
        i = passo % K
        t.atualizar(i, 1 if g.uniforme() < (i + 1) / 11 else 0)
    return t.a, t.b


def gravar(caminho, a, b):
    with open(caminho, "wb") as f:
        f.write(b"SYN1" + struct.pack("<i", len(a)) + struct.pack(f"<{2 * len(a)}d", *a, *b))


def ler(caminho):
    dados = open(caminho, "rb").read()
    assert dados[:4] == b"SYN1"
    (k,) = struct.unpack("<i", dados[4:8])
    nums = struct.unpack(f"<{2 * k}d", dados[8:8 + 16 * k])
    return dados, list(nums[:k]), list(nums[k:])


def main():
    a, b = crenca()
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        gravar(os.path.join(sys.argv[2], "pesos_py.bin"), a, b)
        return
    pasta = sys.argv[1] if len(sys.argv) > 1 else "."
    gravar(os.path.join(pasta, "pesos_py.bin"), a, b)
    dpy, _, _ = ler(os.path.join(pasta, "pesos_py.bin"))
    print(f"arquivo do Python: {len(dpy)} bytes; sha = {hashlib.sha256(dpy).hexdigest()}")
    dj, aj, bj = ler(os.path.join(pasta, "pesos_java.bin"))
    print(f"arquivo do Java: {len(dj)} bytes; sha = {hashlib.sha256(dj).hexdigest()}")
    print("a = " + " ".join(x.hex() for x in aj))
    print("b = " + " ".join(x.hex() for x in bj))
    print(f"os dois arquivos sao iguais byte a byte: {dpy == dj}")


if __name__ == "__main__":
    main()
