"""Testes de unidade da Parte 56: `python3 -m unittest synthai.testes_parte56`. Cada pNN nova com o seu teste."""

import unittest

import calculos


class LemasFalsos:
    # 'aa' e 'bb' têm os mesmos sinsets {0, 1}; 'cc' tem {1}; 'dd' e 'ee' têm {2}; 'f-g' não é alfabética
    lemas = {"aa": [0, 1], "bb": [1, 0], "cc": [1], "dd": [2], "ee": [2, 2], "f-g": [0, 1]}


class TesteParte56(unittest.TestCase):
    def test_sinonimos_perfeitos(self):
        frac, n, maior = calculos.p1122_sinonimos_perfeitos(LemasFalsos())
        # 4 das 5 palavras alfabéticas têm gêmeo (aa/bb, dd/ee); o maior grupo é o primeiro em tamanho e depois em ordem
        self.assertEqual(n, 5)
        self.assertAlmostEqual(frac, 0.8, places=12)
        self.assertEqual(maior, ["dd", "ee"])

    def test_mesma_soma(self):
        # conferido por código antes: de 1 a 30, só 1..9 têm a mesma soma (9 de 30)
        f, k, conta = calculos.p1123_mesma_soma(30)
        self.assertEqual((k, f), (9, 0.3))
        # a rede: S16 − S10 é sempre múltipla de 3
        def s(n, b):
            t = 0
            while n:
                n, r = divmod(n, b)
                t += r
            return t
        self.assertTrue(all((s(n, 16) - s(n, 10)) % 3 == 0 for n in range(1, 5000)))

    def test_empates(self):
        emp = calculos.p1121_empates()
        self.assertEqual(sorted(emp), ["12", "14", "18", "19", "20", "24"])
        self.assertEqual((emp["12"], emp["14"]), (9, 2))
        self.assertEqual(emp["18"] + emp["19"] + emp["20"] + emp["24"], 0)


if __name__ == "__main__":
    unittest.main()
