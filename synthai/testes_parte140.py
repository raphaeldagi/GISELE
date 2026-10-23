"""Testes da Parte 140: o leitor v5 (tabelas), o dicionário como fluxo, o hexadecimal como vértices, e as funções P3187–P3192 pelo nome."""
import unittest

import calculos as c


class TestesParte140(unittest.TestCase):
    def test_p3187_minhas_previsoes_v5_le_tabela(self):
        v = c.p3187_minhas_previsoes_v5(range(137, 138))
        rot = {x[1]: x for x in v}
        self.assertIn("a", rot)
        self.assertIn("b2", rot)
        self.assertFalse(rot["b2"][4])  # (b2) errou na Parte 137
        self.assertEqual(len(v), 11)

    def test_p3187_igual_v4_onde_a_v4_le(self):
        self.assertEqual(set(c.p3187_minhas_previsoes_v5(range(120, 124))), set(c.p2833_minhas_previsoes_v4(range(120, 124))))

    def test_p3188_auditoria_do_leitor_v5(self):
        n, ac, mudam, por = c.p3188_auditoria_do_leitor_v5()
        self.assertEqual((n, ac, mudam), (91, 84, 0))  # (83, 76) até a Parte 135 ganhar 8 vereditos (Parte 144)

    def test_p3189_dicionario_como_fluxo(self):
        r, z, met, N, mu = c.p3189_dicionario_como_fluxo(k=200, reservatorios=20)
        self.assertEqual(N, 117659)
        self.assertLess(abs(r - 1), 0.5)
        self.assertLess(abs(met - 0.5), 0.02)

    def test_p3190_hexadecimal_vertices(self):
        p16, e10, eb, pn = c.p3190_hexadecimal_vertices(n=2000)
        self.assertAlmostEqual(p16, 4.0, places=9)
        self.assertLess(e10, 1e-9)
        self.assertLess(eb, 0.02)

    def test_p3191_calibracao_v4_v5(self):
        (n4, a4), (n5, a5) = c.p3191_calibracao_v4_v5(range(80, 124))
        self.assertGreaterEqual(n5, n4)

    def test_p3192_partes_invisiveis(self):
        self.assertNotIn(137, c.p3192_partes_invisiveis(range(130, 139)))


if __name__ == "__main__":
    unittest.main()
