"""Testes da Parte 145: os grupos úteis da GRPO num segundo mundo (P3197 pelo nome)."""
import unittest

import calculos as c


class TestesParte145(unittest.TestCase):
    def test_p3197_grupos_uteis_mundo_novo(self):
        out, desvio, ordem = c.p3197_grupos_uteis_mundo_novo()
        self.assertEqual(round(out[2][1], 1), 362.0)
        self.assertEqual(round(out[16][1], 1), 175.3)
        self.assertFalse(ordem)  # G = 4 acima de G = 2: a diferença esperada (0,0022) está abaixo do ruído (0,0076)
        for d in desvio.values():
            self.assertLess(abs(d), 0.017)


if __name__ == "__main__":
    unittest.main()
