"""Testes de unidade da Parte 74 (o que vale testar): `python3 -m unittest synthai.testes_parte74`. Cada pNN nova chamada PELO NOME."""

import unittest

import calculos


class TesteParte74(unittest.TestCase):
    def test_p1661_ganho_de_informacao_contra_voi(self):
        z, mh, mv = calculos.p1661_ganho_de_informacao_contra_voi(2000, 73)
        self.assertEqual(z, 0.51)
        # os 10% de maior VOI têm, por definição, o maior VOI médio possível entre conjuntos de 200
        self.assertLess(mh, mv)
        self.assertAlmostEqual(mv, 0.1695997953157454, places=12)

    def test_p1662_orcamento(self):
        # numa instância só, o guloso por VOI nunca passa do ótimo, e o ótimo é exato (as razões estão em [0; 1])
        a, b, f = calculos.p1662_orcamento(instancias=20, semente=1)
        self.assertTrue(0.0 <= b <= a <= 1.0 + 1e-12)
        self.assertTrue(0.0 <= f <= 1.0)
        self.assertEqual(calculos.p1662_orcamento(semente=75)[2], 0.62)

    def test_p1663_rodada48(self):
        so, s1, s2, ot = calculos.p1663_rodada48()
        self.assertEqual(ot, 172)
        self.assertTrue(s2 < s1 <= so)


if __name__ == "__main__":
    unittest.main()
