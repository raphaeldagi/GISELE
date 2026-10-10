"""Testes de unidade da Parte 68: `python3 -m unittest synthai.testes_parte68`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import unittest

import calculos


class DicionarioFalso:
    # a é pai de b e de c; c é pai de d: folhas b e d entre os substantivos; o verbo é folha
    indice = {"n:a": 0, "n:b": 1, "n:c": 2, "n:d": 3, "v:e": 4}
    sinsets = [("n", ["a"], [], ""), ("n", ["b"], ["n:a"], ""), ("n", ["c"], ["n:a"], ""), ("n", ["d"], ["n:c"], ""), ("v", ["e"], [], "")]


PREVISOES = [(1, "a", 0.1, 0.3, True, "fracao"), (1, "b", 0.2, 0.25, False, "fracao"), (1, "c", 0.1, 0.9, True, "fracao"),
             (1, "d", -1.0, 1.0, False, "zero"), (1, "e", None, None, True, None)]


def digitos(n, b):
    r = []
    while n:
        n, x = divmod(n, b)
        r.append(x)
    return r


class TesteParte68(unittest.TestCase):
    def test_p1481_minhas_previsoes_v2(self):
        prev = calculos.p1481_minhas_previsoes_v2((60, 67))
        self.assertEqual(prev[0], (60, "a", 0.03, 0.12, True, "fracao"))  # "[3%; 12%]" vira fração
        p67 = [x for x in prev if x[0] == 67]
        self.assertEqual([x[5] for x in p67], ["fracao", "contagem", "outra", "zero", None, "zero"])  # (c) e (f) na linha seguinte

    def test_p1482_engenharia_por_tipo(self):
        # frações: w = 0,5 (✅), 0,111 (❌), 0,8 (✅): mediana 0,5; a estreita erra, a larga acerta
        r = calculos.p1482_engenharia_por_tipo(PREVISOES)
        n, acerto, med, est, lar = r["fracao"]
        self.assertEqual((n, est, lar), (3, 0.0, 1.0))
        self.assertAlmostEqual(med, 0.5, places=12)
        self.assertEqual(r["zero"][:2], (1, 0.0))

    def test_p1491_densidade_da_conta(self):
        linhas, antes, depois, maior = calculos.p1491_densidade_da_conta()
        self.assertEqual(linhas[5][:2], (10, 9592))  # π(10⁵) = 9.592
        self.assertAlmostEqual(antes, 0.0379, places=4)
        self.assertLess(abs(depois - antes), 0.005)

    def test_p1492_folhas(self):
        self.assertEqual(calculos.p1492_folhas(DicionarioFalso()), {"n": (0.5, 4), "v": (1.0, 1)})

    def test_p1493_palindromos_duplos(self):
        achados, conta = calculos.p1493_palindromos_duplos(100, 16, 10)
        self.assertEqual(achados, [1, 2, 3, 4, 5, 6, 7, 8, 9, 11])
        outra = sum(16 ** (-(len(digitos(n, 16)) // 2)) * 10 ** (-(len(digitos(n, 10)) // 2)) for n in range(1, 100))
        self.assertAlmostEqual(conta, outra, places=12)

    def test_p1499_previsoes_sobre_previsoes_v2(self):
        m, ws = calculos.p1499_previsoes_sobre_previsoes_v2(67)
        self.assertEqual((m["m1"], m["m2"], m["m5"]), (6, 2, 1))
        self.assertAlmostEqual(m["m3"], ws[1], places=12)


if __name__ == "__main__":
    unittest.main()
