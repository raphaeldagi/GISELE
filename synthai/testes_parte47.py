"""Testes de unidade da Parte 47: `python3 -m unittest synthai.testes_parte47`."""

import unittest

import calculos
from .dicionario import Dicionario


class DicionarioFalso:
    definicao = staticmethod(Dicionario.definicao)

    def __init__(self):
        # cão -> canino (a definição de cão cita o gênero no plural); gato -> felino (não cita); canino cita "dog"
        self.sinsets = [("n", ["canine"], [], "a carnivore; of the dog family"),
                        ("n", ["dog"], ["n:1"], "one of the domestic canines \"my dog\""),
                        ("n", ["feline"], [], "a cat-like animal"),
                        ("n", ["cat"], ["n:3"], "a small pet")]
        self.indice = {"n:1": 0, "n:2": 1, "n:3": 2, "n:4": 3}


class TesteParte47(unittest.TestCase):
    def test_cadeia_hexadecimal_ate_20(self):
        # de 1 a 20 sem letra: 1-9 e 16-20 (0x10-0x14) = 14; passos de 10 a 20: 16,17,18,19,20 dão 1 cada (20 = 0x14 -> 14 = 0xe)
        sem, media, _ = calculos.p852_cadeia_hexadecimal(20)
        self.assertEqual(sem, 14)
        self.assertAlmostEqual(media, 5 / 11, places=12)

    def test_cadeia_desce(self):
        # f diminui o número: 0x100 = 256 -> 100 -> 0x64 -> 64 -> 0x40 -> 40 -> 0x28 -> 28 -> 0x1c (letra): 4 passos
        n, k = 256, 0
        while format(n, "x").isdigit():
            n, k = int(format(n, "x")), k + 1
        self.assertEqual(k, 4)

    def test_genero_e_diferenca(self):
        direto, inverso, pares, n = calculos.p851_genero_e_diferenca(DicionarioFalso())
        # direto: "canines" contém canine (+s): 1 de 2; inverso: a de canine cita "dog": 1 de 2 pares
        self.assertEqual((direto, inverso, pares, n), (0.5, 0.5, 2, 2))


if __name__ == "__main__":
    unittest.main()
