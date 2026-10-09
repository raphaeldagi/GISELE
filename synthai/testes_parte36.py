"""Testes de unidade da Parte 36: `python3 -m unittest synthai.testes_parte36`."""

import random
import unittest

from .decisao import ThompsonSurpresaExposta
from .hexadecimal import de_gray, ea_um_mais_um, gray


class TesteParte36(unittest.TestCase):
    def test_de_gray_inverte_gray(self):
        for n in range(1024):
            self.assertEqual(de_gray(gray(n)), n)

    def test_vizinhos_inteiros_diferem_em_um_bit_de_gray(self):
        for n in range(255):
            self.assertEqual(bin(gray(n) ^ gray(n + 1)).count("1"), 1)

    def test_exposicao_puxa_o_mais_antigo(self):
        t = ThompsonSurpresaExposta(3, random.Random(1), periodo=2)
        t.ultimo = [5, 1, 3]
        t.passo = 1
        self.assertEqual(t.escolher(), 1)  # passo 2: forçado, o puxado há mais tempo

    def test_ea_gray_resolve_o_penhasco(self):
        apt = lambda vs: -sum((v - 128) ** 2 for v in vs)
        fx, _ = ea_um_mais_um(apt, 8, gray(127), random.Random(2), 2000, "gray")
        self.assertEqual(fx, 0)
        fb, _ = ea_um_mais_um(apt, 8, 127, random.Random(2), 2000, "binario")
        self.assertEqual(fb, -1)  # preso em 0x7F: o vizinho 0x80 está a 8 bits


if __name__ == "__main__":
    unittest.main()
