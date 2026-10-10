"""Testes de unidade da Parte 67: `python3 -m unittest synthai.testes_parte67`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import unittest

import calculos


class DicionarioFalso:
    sinsets = [("n", ["president"], ["n:1", "n:2"], ""), ("n", ["dog"], ["n:3"], ""), ("v", ["run"], ["v:1"], "")]


PREVISOES = [(1, "a", 1.0, 2.0, True), (1, "b", None, None, False), (1, "c", -1.0, 1.0, False), (1, "d", 2.0, 6.0, True)]


class TesteParte67(unittest.TestCase):
    def test_p1451_tendencia_ou_dispersao(self):
        todos, (beta, alfa, ep), (m, dp), (mt, dpt) = calculos.p1451_tendencia_ou_dispersao()
        self.assertEqual(len(todos), 36)
        self.assertEqual(todos[-1][:2], (40, 3755))
        self.assertAlmostEqual(beta, 0.0379, places=4)

    def test_p1452_minhas_previsoes(self):
        prev = calculos.p1452_minhas_previsoes((66,))
        self.assertEqual(len(prev), 9)
        self.assertEqual(prev[0], (66, "a", 0.95, 1.3, True))
        self.assertEqual(prev[2], (66, "c", 0.063, 0.0715, True))

    def test_p1453_engenharia_das_previsoes(self):
        # w = 1/3, 1 e 1/2; mediana 1/2; deixando uma de fora: |1/3 − 3/4|, |1 − 5/12|, |1/2 − 2/3| (média 7/18); ingênuo: (2/3 + 1/2)/2
        r = calculos.p1453_engenharia_das_previsoes(PREVISOES)
        self.assertEqual((r["previsoes"], r["com_faixa"]), (4, 3))
        self.assertAlmostEqual(r["w_mediana"], 0.5, places=12)
        self.assertAlmostEqual(r["erro_loo"], 7 / 18, places=12)
        self.assertAlmostEqual(r["erro_ingenuo"], 7 / 12, places=12)
        self.assertAlmostEqual(r["acerto"], 0.5, places=12)

    def test_p1454_heranca_multipla(self):
        por, ex = calculos.p1454_heranca_multipla(DicionarioFalso())
        self.assertEqual((por, ex), ({"n": (0.5, 2), "v": (0.0, 1)}, ["president"]))

    def test_p1455_automorficos(self):
        achados, conta = calculos.p1455_automorficos(10, 3)
        self.assertEqual(achados, [5, 6, 25, 76, 376, 625])
        self.assertAlmostEqual(conta, 2 * 3 * 0.9, places=12)
        self.assertEqual(calculos.p1455_automorficos(16, 3)[0], [])  # 16 = 2⁴: só os triviais

    def test_p1459_previsoes_sobre_previsoes(self):
        m, mediana, ws = calculos.p1459_previsoes_sobre_previsoes(66, range(53, 66))
        self.assertEqual(m["m2"], 9)
        self.assertEqual(len(ws), 6)
        self.assertAlmostEqual(m["m5"], sum(abs(w - mediana) for w in ws) / 6, places=12)


if __name__ == "__main__":
    unittest.main()
