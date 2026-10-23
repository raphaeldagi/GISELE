"""Rodada 95 do diálogo Python <-> Java (Parte 145): o hexadecimal de Benford. O primeiro dígito hexadecimal de 3ⁿ, n = 1..500, por inteiros
grandes (exatos nos dois lados), e o posto efetivo dos 4 bits desses dígitos (centrar, ZᵀZ, Jacobi cíclico, exp(−Σp ln p) com o exp e o log
PRÓPRIOS da rodada 26). Imprime as contagens dos 15 dígitos e o posto em hexadecimal. Da raiz: python3 dialogo/rodada95.py"""
import importlib.util
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("rodada93", os.path.join(AQUI, "rodada93.py"))
r93 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r93)


def main():
    dig = [int(format(3 ** m, "x")[0], 16) for m in range(1, 501)]
    cont = [0] * 16
    for d in dig:
        cont[d] += 1
    print("contagens " + " ".join(str(c) for c in cont[1:]))
    H = [[float((d >> j) & 1) for j in (3, 2, 1, 0)] for d in dig]
    print("posto " + r93.posto(H).hex())
    print("fim")


if __name__ == "__main__":
    main()
