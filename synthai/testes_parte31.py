"""Testes de unidade dos métodos da Parte 31 (dicionário e hexadecimal): `python3 -m unittest synthai.testes_parte31`."""

import unittest

from .dicionario import fecho_parcial, minset_reduzido, spearman
from .hexadecimal import gray, hamming, subida_de_encosta, ulps_entre

BRINQUEDO = {"a": {"b"}, "b": {"a"}, "c": {"a"}, "d": {"c", "b"}, "e": {"d"}}


class TesteParte31(unittest.TestCase):
    def test_fecho_parcial(self):
        self.assertEqual(fecho_parcial({"a"}, BRINQUEDO, 1.0), set(BRINQUEDO))
        self.assertEqual(fecho_parcial({"c"}, BRINQUEDO, 0.5), {"c", "d", "e"})  # d: 1 de 2 basta; a e b só se definem entre si
        self.assertEqual(fecho_parcial({"c"}, BRINQUEDO, 1.0), {"c"})

    def test_minset_reduzido_tira_o_redundante_e_continua_aciclico(self):
        self.assertEqual(minset_reduzido(set(BRINQUEDO), BRINQUEDO, ["a", "b"]), {"a"})
        tri = {"x": {"y"}, "y": {"z"}, "z": {"x"}}
        self.assertEqual(len(minset_reduzido(set(tri), tri, ["x", "y", "z"])), 1)

    def test_gray_muda_um_bit(self):
        for n in range(15):
            self.assertEqual(hamming(gray(n), gray(n + 1)), 1)
        self.assertEqual(sorted(gray(n) for n in range(16)), list(range(16)))

    def test_subida_de_encosta(self):
        self.assertEqual(subida_de_encosta({0: 1, 1: 2, 2: 0, 3: 5}), [0, 1, 3])

    def test_spearman_e_ulps(self):
        self.assertAlmostEqual(spearman([1, 2, 3, 4], [10, 20, 30, 25]), 0.8)
        self.assertEqual(ulps_entre(0.1 + 0.2, 0.3), 1.0)


if __name__ == "__main__":
    unittest.main()
