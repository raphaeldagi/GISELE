"""Testes de unidade da Parte 73 (o que refuta): `python3 -m unittest synthai.testes_parte73`. Cada pNN nova chamada PELO NOME."""

import unittest

import calculos


class Mini:
    # raiz 0 (organism) com filhos 1 (animal) e 2 (parasite); 3 é filho de 1 e de 2 (viola a disjunção); 4 é filho de 1 com glosa "flightless"
    indice = {f"n:{i}": i for i in range(5)}
    lemas = {"organism": [0], "animal": [1], "parasite": [2], "bird": [1]}
    sinsets = [("n", ["organism"], [], "g0"), ("n", ["animal", "fauna"], ["n:0"], "g1"), ("n", ["parasite"], ["n:0"], "g2"),
               ("n", ["flea", "animal"], ["n:1", "n:2"], "g3"), ("n", ["kiwi"], ["n:1"], "g4")]
    _defs = {"g0": "a living thing", "g1": "a living organism", "g2": "an organism that lives on another", "g3": "a small insect",
             "g4": "a nocturnal flightless bird"}

    def definicao(self, g):
        return self._defs[g]


class TesteParte73(unittest.TestCase):
    def test_p1631_comparar_reenvio(self):
        self.assertEqual(calculos.p1631_comparar_reenvio(), [(0, 1, 135)])

    def test_p1632_prioridade_contra_voi(self):
        z, zt, rho, pares = calculos.p1632_prioridade_contra_voi(2000, 73)
        self.assertEqual((z, zt), (0.479, 0.51))
        # VOI nunca é negativo, e S = H + I + 1 fica em [1; 3]
        self.assertTrue(all(v >= 0.0 and 1.0 <= s <= 3.0 for s, v in pares))

    def test_p1633_disjuncoes_e_p1634_irmaos(self):
        m = Mini()
        regras = calculos.p1611_regras_de_animal(m)[1]
        self.assertEqual(calculos.p1634_irmaos(0, m), [1, 2])
        self.assertEqual(calculos.p1633_disjuncoes([1, 2], m, regras), {(1, 2): [3]})

    def test_p1635_contradicoes_de_animal(self):
        n, pares = calculos.p1635_contradicoes_de_animal(Mini())
        self.assertEqual((n, pares), (1, [(2, [3])]))

    def test_p1636_contraexemplos(self):
        self.assertEqual(calculos.p1636_contraexemplos("bird", "flightless", Mini()), (3, ["kiwi"]))

    def test_p1637_polissemia(self):
        # lemas de substantivo: organism, animal (2 sinsets), fauna, parasite, flea, kiwi: 6 lemas, 1 polissêmico
        self.assertEqual(calculos.p1637_polissemia(Mini())[:2], (6, 1))

    def test_p1638_rodadas_com_libm(self):
        total, com = calculos.p1638_rodadas_com_libm()
        self.assertGreaterEqual(total, 47)
        for r in ("rodada21", "rodada22", "rodada23", "rodada25", "rodada26", "rodada47"):
            self.assertNotIn(r, com)

    def test_p1639_rodada47(self):
        n, z0, sv, ss, zt, mtv, mts = calculos.p1639_rodada47()
        self.assertEqual((n, z0, zt), (2000, 958, 102))
        self.assertLess(mts, mtv)


    def test_p1642_heranca_multipla(self):
        # no Mini, só a pulga (3) tem dois hiperônimos: 1 de 5
        self.assertEqual(calculos.p1642_heranca_multipla(Mini()), (1, 5, 0.2))


if __name__ == "__main__":
    unittest.main()
