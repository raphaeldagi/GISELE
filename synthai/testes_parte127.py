"""Testes da Parte 127: a ignição biestável, o atraso de Airy, a compressão condicional e o tipo 2 (P3161–P3169), pelo nome."""

import math
import unittest

import calculos as c


class TestesParte127(unittest.TestCase):
    def test_p3161_ignicao_dobras(self):
        s_sobe, s_desce, xa, xb, a = c.p3161_ignicao_dobras(2.0, 4.0, 1.0)
        f = lambda x: x - 2.0 / (1 + math.exp(-4.0 * (x - 1.0)))
        h = 1e-6
        self.assertAlmostEqual((f(xa + h) - f(xa - h)) / (2 * h), 0.0, places=6)     # f'(x_a) = 0
        self.assertAlmostEqual(s_sobe, -s_desce, places=12)                         # simetria θ = w/2
        self.assertAlmostEqual(a, math.sqrt(2), places=12)
        self.assertIsNone(c.p3161_ignicao_dobras(1.0, 3.0, 1.0))                    # w·g/4 < 1: sem biestabilidade

    def test_p3161_assimetrico(self):
        # θ ≠ w/2: todos os termos diferentes de zero; a dobra satisfaz s = f(x) e f' = 0
        s_sobe, s_desce, xa, xb, a = c.p3161_ignicao_dobras(3.0, 2.0, 0.7)
        sig = lambda z: 1 / (1 + math.exp(-z))
        self.assertAlmostEqual(s_sobe, xa - 3.0 * sig(2.0 * (xa - 0.7)), places=12)
        self.assertAlmostEqual(1 - 6.0 * sig(2.0 * (xb - 0.7)) * (1 - sig(2.0 * (xb - 0.7))), 0.0, places=12)
        self.assertGreater(s_sobe, s_desce)

    def test_p3162_ignicao_rampa(self):
        sobe, desce = c.p3162_ignicao_rampa(0.01)
        self.assertGreater(sobe, c.p3161_ignicao_dobras()[0])   # a rampa atrasa a ignição
        self.assertLess(desce, c.p3161_ignicao_dobras()[1])

    def test_p3163_atraso_airy(self):
        d1, _ = c.p3163_atraso_airy(0.002)
        d2, _ = c.p3163_atraso_airy(0.00025)
        self.assertAlmostEqual(d1 / d2, 4.0, places=9)        # 8^(2/3)

    def test_p3168_cruzamento_riccati(self):
        tau, s = c.p3168_cruzamento_riccati(0.002)
        self.assertLess(tau, 2.338107410459767)                # o cruzamento vem antes da explosão
        self.assertGreater(s, c.p3161_ignicao_dobras()[0])

    def test_p3164_k_condicional(self):
        a = "o degrau quebrado na calçada " * 5
        k, cb, eco = c.p3164_k_condicional(a, a)
        self.assertGreater(eco, 0.5)                           # um texto dado ele mesmo custa quase nada

    def test_p3165_ncd(self):
        self.assertLess(c.p3165_ncd("abc " * 50, "abc " * 50), c.p3165_ncd("abc " * 50, "xyz q " * 40))

    def test_p3166_atribuir(self):
        pais = ["gato preto no telhado " * 6, "chuva fria sobre o rio " * 6, "relógio parado na sala " * 6]
        filhos = ["chuva fria sobre o rio e mais nada " * 3, "relógio parado na sala vazia " * 3, "gato preto no telhado alto " * 3]
        self.assertEqual(c.p3166_atribuir(pais, filhos, [1, 2, 0])[:2], (3, 3))

    def test_p3167_tipo2(self):
        reg = [(0, "a", "conta", True)] * 9 + [(0, "b", "conta", False)] + [(0, "c", "mecanismo", True)] * 5 + [(0, "d", "mecanismo", False)] * 5
        pa, pb, h2, f2, d2, n = c.p3167_tipo2(reg)
        self.assertAlmostEqual(pa, 0.9)
        self.assertAlmostEqual(pb, 0.5)
        self.assertAlmostEqual(h2, 9.5 / 15)
        self.assertAlmostEqual(f2, 1.5 / 7)
        self.assertGreater(d2, 0)
        self.assertEqual(len(c.PREVISOES_P124_P126), 40)

    def test_p3169_informacao_par(self):
        pais = ["gato preto no telhado " * 6, "chuva fria sobre o rio " * 6, "relógio parado na sala " * 6]
        filhos = ["chuva fria sobre o rio " * 4, "relógio parado na sala " * 4, "gato preto no telhado " * 4]
        mc, me, z, assim = c.p3169_informacao_par(pais, filhos, [1, 2, 0])
        self.assertGreater(mc, me)


if __name__ == "__main__":
    unittest.main()
