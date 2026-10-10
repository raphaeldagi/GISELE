"""Testes de unidade da Parte 72 (o que está disfuncional): `python3 -m unittest synthai.testes_parte72`. Cada pNN nova chamada PELO NOME."""

import math
import unittest

import calculos


class Mini:
    # três sinsets: "knowledge" definido com "information", "information" sem "knowledge"; sinônimos a/b
    sinsets = [("n", ["knowledge"], [], "g0"), ("n", ["information", "info"], [], "g1"), ("n", ["a", "b"], [], "g2")]
    _defs = {"g0": "information acquired by study", "g1": "a message received", "g2": "letters"}

    def definicao(self, g):
        return self._defs[g]


class TesteParte72(unittest.TestCase):
    def test_p1601_auditoria_do_repositorio(self):
        defeitos = calculos.p1601_auditoria_do_repositorio(71)
        self.assertEqual(set(defeitos), {"docs", "sem_teste", "testes_fora_da_lista", "rodadas_sem_java", "partes_fora_do_resultados", "constantes"})
        self.assertEqual(defeitos["rodadas_sem_java"], [])
        self.assertEqual(defeitos["constantes"], [])

    def test_p1602_entropia_de_unigrama(self):
        # "aab": p = 2/3, 1/3; H = −(2/3)log₂(2/3) − (1/3)log₂(1/3) = 0,9183; 2 símbolos: redundância 1 − H/1; contra 8 bits: 1 − H/8
        h, n, r, r8 = calculos.p1602_entropia_de_unigrama("aab")
        hh = -(2 / 3) * math.log2(2 / 3) - (1 / 3) * math.log2(1 / 3)
        self.assertAlmostEqual(h, hh, places=12)
        self.assertEqual(n, 2)
        self.assertAlmostEqual(r, 1 - hh, places=12)
        self.assertAlmostEqual(r8, 1 - hh / 8, places=12)

    def test_p1603_ciclos_de_glosas(self):
        r = calculos.p1603_ciclos_de_glosas((("information", "knowledge"),), Mini())
        self.assertEqual(r, [("information", "knowledge", True, False)])

    def test_p1604_hash_como_peso(self):
        ms, mr, z = calculos.p1604_hash_como_peso(50, 1, Mini())
        self.assertAlmostEqual(z, (ms - mr) / math.sqrt(2 / 18 / 50), places=12)
        self.assertTrue(0 <= ms <= 1 and 0 <= mr <= 1)


if __name__ == "__main__":
    unittest.main()
