"""Testes de unidade da Parte 112 (o simplex próprio, o Kuhn completo, o leitor v3 e a hipótese do repertório):
`python3 -m unittest synthai.testes_parte112`. Casos com todos os termos diferentes de zero (regra da Parte 30) e controles dos dois lados (Parte 75)."""

import unittest
from fractions import Fraction as F

import calculos
from synthai import minimax, simplex


class TesteSimplex(unittest.TestCase):
    def test_reproduz_a_parte_108(self):
        v, p, q, _ = simplex.resolver_jogo(minimax.JOGO_TESTE)
        self.assertEqual((v, p, q), (F(1, 7), [F(5, 7), F(2, 7)], [F(4, 7), F(3, 7)]))
        v, p, q, _ = simplex.resolver_jogo(minimax.JOGO_SELA)
        self.assertEqual((v, p), (1, [1, 0]))

    def test_pedra_papel_tesoura(self):
        v, p, q, _ = simplex.resolver_jogo([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
        self.assertEqual(v, 0)
        self.assertEqual(p, [F(1, 3)] * 3)

    def test_problema_lp_direto(self):
        # max 3x + 2y s.a. x + y <= 4, x + 3y <= 6: ótimo em (4, 0), valor 12
        val, x, y, _ = simplex.simplex_max([[F(1), F(1)], [F(1), F(3)]], [F(4), F(6)], [F(3), F(2)], zero=F(0))
        self.assertEqual((val, x), (12, [4, 0]))
        self.assertEqual(sum(yi * bi for yi, bi in zip(y, [4, 6])), 12)   # dualidade forte

    def test_regras_do_kuhn_a_mao(self):
        # o caso conferido à mão no registro: P1 com o rei aposta, P2 com o valete desiste: +1
        self.assertEqual(simplex._payoff_kuhn(3, 1, "aposta", ("desiste", "passa")), 1)
        self.assertEqual(simplex._payoff_kuhn(1, 3, "passa-paga", ("paga", "aposta")), -2)
        self.assertEqual(simplex._payoff_kuhn(2, 1, "passa-desiste", ("desiste", "passa")), 1)


class TesteParte112(unittest.TestCase):
    def test_p2801_kuhn_completo(self):
        v, k, (lo, hi) = calculos.p2801_kuhn_completo()
        self.assertEqual(v, F(-1, 18))
        self.assertEqual((lo, hi), (F(-1, 18), F(-1, 18)))

    def test_p2802_jogador2(self):
        self.assertEqual(calculos.p2802_jogador2_de_kuhn(), (F(1, 3), F(1, 3)))

    def test_p2803_familia_do_jogador1(self):
        al, d1, bq, d2 = calculos.p2803_familia_do_jogador1()
        self.assertTrue(0 <= al <= F(1, 3))
        self.assertEqual((d1, bq, d2), (0, 0, 0))

    def test_p2804_float_exato_e_dualidade(self):
        ve, ef, lac, ke = calculos.p2804_float_exato_e_dualidade()
        self.assertEqual(ve, F(-5, 12))
        self.assertLessEqual(ef, 1e-12)
        self.assertEqual(lac, 0)

    def test_p2805_rodada79(self):
        v, p, q, k = calculos.p2805_rodada79()
        self.assertEqual(v.hex(), "-0x1.aaaaaaaaaaaa0p-2")
        self.assertEqual(k, 3)

    def test_p2806_p2807_leitor_v3(self):
        rec, per, tro, tot = calculos.p2807_v2_contra_v3(range(53, 112))
        self.assertEqual(len(rec), 7)
        self.assertIn((110, "a"), rec)
        self.assertEqual(per, [(110, "h")])          # a faixa roubada da (a); a certa tem expoentes sobrescritos
        self.assertEqual(sorted(tro), [(74, "a"), (84, "e")])
        v3 = {(x[0], x[1]): (x[2], x[3]) for x in calculos.p2806_minhas_previsoes_v3(range(84, 85))}
        self.assertEqual(v3[(84, "e")], (0.81, 0.99))   # a v2 lia [0; 3,33] de outro item

    def test_p2808_placar_m_v3(self):
        # pelo NOME (regra da Parte 58; a P1092 da Parte 112 acusou que a P2808 só era testada por dentro da P2809)
        m, ws = calculos.p2808_previsoes_sobre_previsoes_v3(112)
        self.assertEqual((m["m1"], m["m2"], m["m5"]), (14, 6, 0))
        self.assertEqual(m["m4"], 1.0)
        m2, _ = calculos.p1499_previsoes_sobre_previsoes_v2(112)
        self.assertEqual(m2["m2"], 5)   # a régua velha perde a (d) na própria parte que a corrige

    def test_p2809_auditoria_do_placar(self):
        linhas, mudam = calculos.p2809_auditoria_do_placar_m()
        self.assertEqual(mudam, 0)
        self.assertEqual(sum(1 for l in linhas if l[3] != l[4]), 5)

    def test_p2810_repertorio(self):
        rc, rl, n, k = calculos.p2810_hipotese_do_repertorio()
        self.assertTrue(1.039 <= rc <= 1.063)
        self.assertTrue(1.081 <= rl <= 1.121)

    def test_p1961_com_parte_112(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[112], (14, 14))
        self.assertEqual((ok, tot), (184, 205))


if __name__ == "__main__":
    unittest.main()
