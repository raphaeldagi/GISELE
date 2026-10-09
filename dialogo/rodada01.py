"""Rodada 1 do diálogo Python <-> Java: a IA-Python roda o módulo original (synthai/hexadecimal.py) e imprime no mesmo
formato que Rodada01.java. Rodar da raiz do repositório: python3 dialogo/rodada01.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthai.hexadecimal import efeitos_fatoriais, gray, hamming, walsh_hadamard  # noqa: E402


def lista(v):
    return "[" + ", ".join(float(x).hex() for x in v) + "]"


print("P* = " + (0.1 / (0.9 * 50)).hex())
print("WH [1,2,3,4] = " + lista(walsh_hadamard([1.0, 2.0, 3.0, 4.0])))
print("efeitos [10,12,20,30] = " + lista(efeitos_fatoriais([10.0, 12.0, 20.0, 30.0])))
print("efeitos sqrt = " + lista(efeitos_fatoriais([(i + 1) ** 0.5 / 3.0 for i in range(8)])))
print("gray = " + "".join(f"{gray(i):X}" for i in range(16)))
print(f"hamming(0x3, 0xC) = {hamming(0x3, 0xC)}; hamming(0xB, 0x4) = {hamming(0xB, 0x4)}")
