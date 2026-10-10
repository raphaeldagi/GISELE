"""Testes de unidade da Parte 60: `python3 -m unittest synthai.testes_parte60`. Cada pNN nova com o seu teste, chamada PELO NOME."""

import os
import sys
import unittest

import calculos

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dialogo"))
import rodada34  # noqa: E402


class DicionarioFalso:
    # walk se define por si; run/jog não; big_cat só tem lema composto e fica fora
    sinsets = [("n", ["walk"], [], "the walk"), ("v", ["run", "jog"], [], "move fast"), ("n", ["big_cat"], [], "cat")]

    @staticmethod
    def palavras_da_definicao(glosa):
        return [w for w in glosa.split() if w != "the"]


TEXTO = """## Rodada 12 — fora
(a) ✅ IA-Python
## Rodada 13 — dentro
(a) ✅ (IA-Python), (b) ❌
**IA-Java**. Previsão (c), das duas vozes. Resultado (c) ✅. Controle (d) ❌. De novo (a) ❌ IA-Java.
## Rodada 14 — dentro
(e) ✅ (a da IA-Java). (f) ✅
---
## Refazer
(g) ✅ IA-Python
"""


class TesteParte60(unittest.TestCase):
    def test_regra_da_rodada34(self):
        # rodada 13: dono (a, Python) ✅, (b, Java) ❌, (a, Java) ❌ [a letra já vista, mas o dono é outro]; conjunta c ✅; sem dono d ❌
        # rodada 14: dono (e, Java) ✅; sem dono f ✅
        tot, linhas = rodada34.placar(TEXTO)
        self.assertEqual(tot["IA-Python"], [2, 2, 4, 3])
        self.assertEqual(tot["IA-Java"], [4, 2, 6, 3])
        self.assertEqual(len(linhas), 2)

    def test_p1241_placar_por_voz(self):
        tot, linhas = calculos.p1241_placar_por_voz(33)
        self.assertEqual(len(linhas), 21)
        self.assertEqual(tot["IA-Python"], [27, 15, 44, 31])
        self.assertEqual(tot["IA-Java"], [27, 13, 44, 29])

    def test_p1242_definicao_propria(self):
        frac, n, por, ex = calculos.p1242_definicao_propria(DicionarioFalso())
        self.assertEqual((n, por), (2, {"n": 1.0, "v": 0.0}))
        self.assertAlmostEqual(frac, 0.5, places=12)
        self.assertEqual(ex, [("walk", "the walk")])

    def test_p1243_narcisistas_hex(self):
        self.assertEqual(calculos.p1243_narcisistas_hex(3, 10), list(range(1, 10)) + [153, 370, 371, 407])
        self.assertIn(0x156, calculos.p1243_narcisistas_hex(3))  # 1³ + 5³ + 6³ = 342 = 0x156

    def test_p1247_interruptores(self):
        self.assertEqual(calculos.p1247_interruptores(5), [(1, 0), (2, 1), (4, 2), (8, 3)])
        self.assertEqual(calculos.p1247_interruptores(4), [(1, 0)])

    def test_p1248_por_comprimento(self):
        self.assertEqual(calculos.p1248_por_comprimento([0x156, 0xB8D2, 5]), {1: 1, 3: 1, 4: 1})

    def test_p1249_fator_de_congruencia(self):
        self.assertEqual([calculos.p1249_fator_de_congruencia(k) for k in (3, 4, 5)], [3, 1, 15])
        self.assertEqual(calculos.p1249_fator_de_congruencia(3, 10), 3)  # 9 não é livre de quadrados: 3³ ≢ 3 (mod 9)

    def test_p1250_esperado_narcisistas(self):
        # base 3, k = 2: somas 4 (0,2: 1 número sem zero à esquerda), 5 (1,2: 2 números), 8 (2,2: 1) caem em [3; 8]: 4/(2·3) = 2/3; g = 2
        e0, e1 = calculos.p1250_esperado_narcisistas(2, 3)
        self.assertAlmostEqual(e0, 2 / 3, places=12)
        self.assertAlmostEqual(e1, 4 / 3, places=12)

    def test_p1251_conta_contra_medida(self):
        # base 3: 5 = 12, 8 = 22 (2 dígitos), 17 = 122 (3 dígitos), conferidos à mão: 1 + 4, 4 + 4, 1 + 8 + 8
        self.assertEqual(calculos.p1243_narcisistas_hex(3, 3), [1, 2, 5, 8, 17])
        linhas, l0, l1 = calculos.p1251_conta_contra_medida(((3, 3),))
        self.assertEqual([x[:3] for x in linhas], [(3, 2, 2), (3, 3, 1)])
        self.assertGreater(l1, l0)


if __name__ == "__main__":
    unittest.main()
