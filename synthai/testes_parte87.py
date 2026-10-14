"""Testes de unidade da Parte 87 (compressão, plasticidade e GRPO): `python3 -m unittest synthai.testes_parte87`."""

import unittest

import calculos
from synthai.plasticidade import quantizar, vantagem_grpo, posto_estavel


class TesteParte87(unittest.TestCase):
    def test_p2051_quantizacao(self):
        m8, m4, razao = calculos.p2051_quantizacao_mse()
        self.assertTrue(200 < razao < 320)  # ~4^4 = 256
        # controle: dequantizar um valor na grade e exato
        self.assertAlmostEqual(quantizar(-4.0, 8, -4.0, 4.0), -4.0, places=6)  # o extremo inferior cai exato na grade
        # mais bits, menos erro
        self.assertLess(m8, m4)

    def test_p2052_grpo(self):
        g2, media = calculos.p2052_vantagem_grpo()
        self.assertEqual(g2, [1.0, -1.0])   # G=2, eps=0: sinal contrastivo puro
        self.assertEqual(media, 0.0)        # a media das vantagens e 0 para qualquer G
        # controle: todos iguais -> vantagens ~0 (desvio 0, eps protege)
        self.assertTrue(all(abs(a) < 1e-6 for a in vantagem_grpo([3.0, 3.0, 3.0])))

    def test_p2053_plasticidade_nao_colapsa(self):
        (pp, pn), (sp_p, sp_n) = calculos.p2053_plasticidade(tarefas=5)
        # a patologia NAO aparece nesta escala: posto nao colapsa (razao proxima de 1 ou acima)
        self.assertGreater(pp, 0.8)
        # o S&P contem mais a norma que o SGD puro
        self.assertLess(sp_n, pn)

    def test_p2054_conflito(self):
        posto, norma, dorm = calculos.p2054_plasticidade_conflito(tarefas=10)
        self.assertGreater(posto, 0.8)   # tambem nao colapsa com conflito nesta escala
        self.assertEqual(dorm, 0.0)

    def test_posto_estavel_controle(self):
        # uma matriz posto-1 tem posto estavel ~1; identidade 3x3 tem posto estavel 3
        self.assertAlmostEqual(posto_estavel([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]]), 1.0, places=4)
        self.assertAlmostEqual(posto_estavel([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]), 3.0, places=4)

    def test_p1961_com_parte_87(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87))
        self.assertEqual(por[87], (2, 5))  # a (e) descartada; a,b ✅, c,d,f ❌
        self.assertEqual((ok, tot), (34, 46))

    def test_p2055_rodada54(self):
        vs = calculos.p2055_rodada54()
        self.assertEqual(len(vs), 18)
        self.assertAlmostEqual(vs[0], 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
