"""Testes de unidade da Parte 63: `python3 -m unittest synthai.testes_parte63`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import math
import unittest

import calculos


class DicionarioFalso:
    indice = {"n:001": 0, "v:002": 1}
    sinsets = [("n", ["animal"], [], 'a living organism; "the dog"'), ("v", ["run"], [], "move fast")]

    @staticmethod
    def definicao(glosa):
        return glosa.split(";")[0]


class PortuguesFalso:
    # 5 palavras contra 3 (1,667) e 1 contra 2 (0,5): mediana 1,0833; metade mais longa
    glosas = {"001-n": "organismo vivo que se move", "002-v": "correr"}


class TesteParte63(unittest.TestCase):
    def test_p1331_fator_efetivo(self):
        linhas, com, longe = calculos.p1331_fator_efetivo()
        self.assertEqual((com, longe), (84, 42))
        self.assertEqual(linhas[5][:2], (8, 13))
        self.assertAlmostEqual(13 / linhas[5][3], 3.4553, places=3)

    def test_p1332_glosa_pt_e_en(self):
        med, mais, n, media = calculos.p1332_glosa_pt_e_en(DicionarioFalso(), PortuguesFalso())
        self.assertEqual((n, mais), (2, 0.5))
        self.assertAlmostEqual(med, (5 / 3 + 0.5) / 2, places=12)
        self.assertAlmostEqual(media, med, places=12)

    def test_p1333_primos_palindromos(self):
        # base 10 até 1000: 2, 3, 5, 7, 11 e 15 de 3 dígitos (101, 131, 151, 181, 191, 313, ...)
        k, conta, por = calculos.p1333_primos_palindromos(1000, 10)
        self.assertEqual((k, por), (20, {1: 4, 2: 1, 3: 15}))
        self.assertEqual(calculos.p1333_primos_palindromos(10 ** 7, 10)[0], 781)  # OEIS A050251

    def test_p1337_conta_palindromos(self):
        # base 10 até 200: 4 primos de 1 dígito, o 11, e 2/ln n nos dez palíndromos 1m1
        esperado = 4 + 1 + sum(2 / math.log(100 + 10 * m + 1) for m in range(10))
        self.assertAlmostEqual(calculos.p1337_conta_palindromos(200, 10), esperado, places=12)
        self.assertAlmostEqual(calculos.p1337_conta_palindromos(16 ** 5, 16), calculos.p1333_primos_palindromos()[1], places=9)

    def test_p1338_contas_da_parte63(self):
        cauda, desvio, ingenuo, npal, media = calculos.p1338_contas_da_parte63(1.0)
        # Poisson(1) >= 13: 1 - sum e^-1/j! (j < 13), conferido por outra conta
        self.assertAlmostEqual(cauda, 1 - sum(math.exp(-1) / math.factorial(j) for j in range(13)), places=12)
        self.assertEqual((npal, media), (4350, 1.0))
        self.assertTrue(0 < desvio < 0.2 and 200 < ingenuo < 500)


if __name__ == "__main__":
    unittest.main()
