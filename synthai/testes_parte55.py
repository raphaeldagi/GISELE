"""Testes de unidade da Parte 55: `python3 -m unittest synthai.testes_parte55`. Cada função pNN nova tem o seu teste (regra da Parte 54)."""

import os
import tempfile
import unittest
from unittest import mock

import calculos


class DicionarioCiclo:
    """O mapa: a -> funil -> b -> a (o funil está NO ciclo); c -> a. Tirar o funil de a quebra o ciclo."""

    def __init__(self):
        defs = {"a": "funil b", "funil": "b", "b": "a", "c": "a"}
        self.sinsets = [("n", [w], [], g) for w, g in sorted(defs.items())]
        self.lemas = {w: [i] for i, (_, ls, _, _) in enumerate(self.sinsets) for w in ls}

    @staticmethod
    def palavras_da_definicao(glosa):
        return glosa.split()


class TesteParte55(unittest.TestCase):
    def test_destino_final(self):
        f = {"a": "b", "b": "c", "c": "a", "d": "a", "e": None, "g": "e"}
        self.assertEqual(calculos._destino_final(f, "d"), ("ciclo", "a"))
        self.assertEqual(calculos._destino_final(f, "g"), ("sumidouro", "e"))

    def test_sem_o_funil_quebra_o_ciclo(self):
        # antes: a -> funil -> b -> a; depois: a -> b. O ciclo muda ({a, funil, b} vira {a, b}), mas o menor elemento é 'a' nos dois,
        # então o destino final ('ciclo', 'a') não muda para ninguém: 0 de 4. (A P1093 real muda porque o ciclo de 'act' some.)
        frac, diretas, n = calculos.p1093_sem_o_funil("funil", DicionarioCiclo())
        self.assertEqual((diretas, n), (1, 4))
        self.assertEqual(frac, 0.0)

    def test_ulp_em_hexadecimal(self):
        # conferidos por código antes: 2000 sorteios, semente 7
        self.assertEqual(calculos.p1094_ulp_em_hexadecimal(2000, 7), (1.0325, 16 / 15))
        self.assertEqual(calculos.p1094_ulp_mantissa_uniforme(2000, 7), (1.0635, 16 / 15))

    def test_pnn_sem_teste(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "synthai"))
            open(os.path.join(d, "calculos.py"), "w").write("def p900_a(x):\n    pass\n\ndef p901_b():\n    pass\n\ndef p50_velha():\n    pass\n")
            open(os.path.join(d, "synthai", "testes_parte99.py"), "w").write("calculos.p900_a(1)\n")
            with mock.patch("os.path.abspath", return_value=os.path.join(d, "calculos.py")):
                total, sem = calculos.p1092_pnn_sem_teste(821, 1090)
        self.assertEqual((total, sem), (2, ["p901_b"]))

    def test_o_ulp_que_chega(self):
        r = calculos.p1091_o_ulp_que_chega()
        self.assertTrue(r["14"][2])          # o empate de " sn" e "rld" se desfez
        self.assertGreater(r["26"][1], 1e-12)  # o Gauss-Newton amplifica
        self.assertFalse(r["06"][2])


if __name__ == "__main__":
    unittest.main()
