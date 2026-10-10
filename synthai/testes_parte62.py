"""Testes de unidade da Parte 62: `python3 -m unittest synthai.testes_parte62`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import unittest

import calculos


class DicionarioFalso:
    # animal = animal (n); run / correr (v) não; ideal (a, satélite no português) e similar (a) iguais
    indice = {"n:001": 0, "v:002": 1, "a:003": 2, "a:004": 3}
    sinsets = [("n", ["animal", "beast"], [], ""), ("v", ["run"], [], ""), ("a", ["ideal"], [], ""), ("a", ["similar"], [], "")]


class PortuguesFalso:
    lemas = {"001-n": ["animal"], "002-v": ["correr"], "003-s": ["ideal"], "004-a": ["similar"]}


class TesteParte62(unittest.TestCase):
    def test_p1301_ultimo_digito(self):
        linhas, rho = calculos.p1301_ultimo_digito()
        self.assertEqual(len(linhas), 14)
        self.assertEqual((linhas[5][0], linhas[5][3]), (8, 13))  # base 8: 13 narcisistas sem interruptor
        self.assertAlmostEqual(rho, 0.44175824175824174, places=12)

    def test_p1302_iguais_nas_duas_linguas(self):
        frac, n, por, ex = calculos.p1302_iguais_nas_duas_linguas(DicionarioFalso(), PortuguesFalso())
        self.assertEqual((n, por, ex), (4, {"a": 1.0, "n": 1.0, "v": 0.0}, ["ideal", "similar", "animal"]))
        self.assertAlmostEqual(frac, 0.75, places=12)

    def test_p1303_autonumeros(self):
        # base 10 até 20: 1, 3, 5, 7, 9, 20 (20 não é n + s(n): 19 + 10 = 29, 15 + 6 = 21, 14 + 5 = 19)
        self.assertEqual(calculos.p1303_autonumeros(20, 10), (0.3, 6, [1, 3, 5, 7, 9, 20]))
        self.assertEqual(calculos.p1303_autonumeros(16, 16)[2], [1, 3, 5, 7, 9, 11, 13, 15])

    def test_p1307_terminacoes_iguais(self):
        self.assertEqual(calculos.p1307_terminacoes_iguais(DicionarioFalso(), PortuguesFalso()), (2, [("al", 1), ("ar", 1)]))

    def test_p1308_chance_de_spearman(self):
        # com n = 3 há 6 permutações; só a identidade dá correlação 1: chance ~1/6
        self.assertAlmostEqual(calculos.p1308_chance_de_spearman(0.99, 3, 6000, 7), 1 / 6, delta=0.02)
        self.assertEqual(calculos.p1308_chance_de_spearman(-1.01, 5, 100), 1.0)


if __name__ == "__main__":
    unittest.main()
