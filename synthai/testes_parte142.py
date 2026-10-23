"""Testes da Parte 142: a enantiodromia do heavy-ball e a compensação da GRPO (P3193, P3194 pelo nome) e o descer com guardar=."""
import unittest

import calculos as c
from synthai import passos as p


class TestesParte142(unittest.TestCase):
    def test_descer_guardar(self):
        A, _, _ = p.quadratica_anisotropica(3, 2.0, 1)
        xs = []
        cs = p.descer(A, [1.0, 0.0, 0.0], [0.0] * 3, 5, guardar=xs)
        self.assertEqual(len(xs), 6)
        self.assertAlmostEqual(cs[-1], p.custo(A, xs[-1], [0.0] * 3))

    def test_p3193_enantiodromia(self):
        r = c.p3193_enantiodromia()
        self.assertEqual([t for _, t, _ in r], [0, 0, 0, 1, 3, 4, 5, 7])
        for l, t, prev in r:
            if prev is not None:
                self.assertLessEqual(abs(t - prev), 1.0)

    def test_p3194_compensacao(self):
        self.assertLess(c.p3194_compensacao(grupos=500), 1e-12)


if __name__ == "__main__":
    unittest.main()
