"""Testes de unidade da Parte 66: `python3 -m unittest synthai.testes_parte66`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import unittest

import calculos


class DicionarioFalso:
    sinsets = [("n", ["dog", "domestic_dog"], [], ""), ("n", ["cat"], [], ""), ("v", ["run", "go", "move"], [], "")]


def soma(n, b):
    t = 0
    while n:
        n, r = divmod(n, b)
        t += r
    return t


class TesteParte66(unittest.TestCase):
    def test_p1421_endereco_da_falta(self):
        quis, k, bases = calculos.p1421_endereco_da_falta()
        self.assertEqual((quis["d0"][1], quis["d2"][1]), (11, 9))  # 12 primeiros dígitos coprimos a 21; 10 dígitos do meio ímpares
        self.assertEqual([x[0] for x in bases], list(range(23, 29)))
        self.assertEqual(bases[0][1], 874)
        self.assertLess(k, 1.0)

    def test_p1422_sinonimos_por_classe(self):
        self.assertEqual(calculos.p1422_sinonimos_por_classe(DicionarioFalso()), {"n": (1.5, 0.5, 2), "v": (3.0, 0.0, 1)})

    def test_p1423_mesma_soma_10_16(self):
        # n < 20: iguais só de 1 a 9 (9 de 19); a conta: 3 vezes Σ_k P(s10 = k) P(s16 = k) nos n de 0 a 19, por outra conta
        frac, conta = calculos.p1423_mesma_soma_10_16(20)
        self.assertAlmostEqual(frac, 9 / 19, places=12)
        d10 = [soma(n, 10) for n in range(20)]
        d16 = [soma(n, 16) for n in range(20)]
        ind = sum(d10.count(k) * d16.count(k) for k in set(d10)) / 400
        self.assertAlmostEqual(conta, 3 * ind, places=12)

    def test_p1427_bases_29_a_34(self):
        b, m, C, sg, z = calculos.p1427_bases_29_a_34((29,))[0]
        self.assertEqual((b, m), (29, 1610))
        self.assertAlmostEqual(z, (m - C) / sg, places=12)


if __name__ == "__main__":
    unittest.main()
