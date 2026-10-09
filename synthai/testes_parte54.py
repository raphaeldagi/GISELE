"""Testes de unidade da Parte 54: `python3 -m unittest synthai.testes_parte54`."""

import unittest

import calculos
from .testes_parte53 import DicionarioFalso


class TesteParte54(unittest.TestCase):
    def test_autodescritivos(self):
        # conferido por código antes (regra da Parte 53): C210000000001000 tem doze 0, dois 1, um 2 e um C
        self.assertEqual(calculos.p1063_autodescritivos(16), ["C210000000001000"])
        self.assertEqual(calculos.p1063_autodescritivos(10), ["6210001000"])
        self.assertEqual(calculos.p1063_autodescritivos(4), ["1210", "2020"])

    def test_folhas(self):
        # raiz -> filho -> neto (cadeia): só o neto é folha; os dois internos têm 1 filho cada
        frac, media, n = calculos.p1062_folhas(DicionarioFalso())
        self.assertEqual(n, 3)
        self.assertAlmostEqual(frac, 1 / 3, places=12)
        self.assertAlmostEqual(media, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()


class TesteExatidaoOuSorte(unittest.TestCase):
    """Acrescentado DEPOIS da medida da Parte 54 (que achou p1061 sem teste); a medida não foi refeita."""

    def test_chance_e_tabela(self):
        import math
        chances, dif = calculos.p1061_exatidao_ou_sorte()
        # nenhuma chamada: chance 1; a rodada 17 não chama exp nem log
        self.assertEqual(chances["rodada17"], 1.0)
        # a fórmula, conferida por uma linha de código antes: (1 − 0,0029)^1000 = 0,05479...
        import importlib.util
        import os
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        spec = importlib.util.spec_from_file_location("rodada28", os.path.join(raiz, "dialogo", "rodada28.py"))
        r28 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(r28)
        self.assertAlmostEqual(r28.chance(1000, 0), (1 - 0.0029) ** 1000, places=14)
        self.assertEqual(dif["rodada25"], (1440, 3, 39059, 5))
        self.assertEqual(dif["rodada06"][2:], (687, 0))
