"""Testes de unidade da Parte 93 (o modelo de mundo que planeja): `python3 -m unittest synthai.testes_parte93`."""

import unittest

import calculos
from synthai import mundo


class TesteParte93(unittest.TestCase):
    def test_p2231_recuperar_modelo(self):
        erro = calculos.p2231_recuperar_modelo()
        # mundo linear determinista: minimos quadrados recuperam A, B ate o epsilon de maquina
        self.assertLess(erro, 1e-10)

    def test_transicao_e_ajuste(self):
        # a dinamica verdadeira e o ajuste batem num caso com TODOS os termos != 0 (regra da Parte 30)
        s = (0.7, -1.3)
        n0, n1 = mundo.transicao(s, 0.5)
        self.assertAlmostEqual(n0, 1.0 * 0.7 + 0.15 * (-1.3) + 0.0 * 0.5)
        self.assertAlmostEqual(n1, 0.0 * 0.7 + 0.9 * (-1.3) + 0.15 * 0.5)
        with self.assertRaises(ValueError):
            mundo.transicao(s, 2.0)  # acao fora de [-1, 1]

    def test_resolver_linear(self):
        x = mundo.resolver_linear([[2.0, 1.0], [1.0, 3.0]], [5.0, 10.0])
        self.assertAlmostEqual(x[0], 1.0)
        self.assertAlmostEqual(x[1], 3.0)

    def test_p2232_painel(self):
        m_mpc, m_re, razao, por = calculos.p2232_mpc_vs_reativo_painel()
        self.assertEqual(len(por), 4)
        # num mundo facil a vantagem media e pequena mas o MPC nao perde feio
        self.assertTrue(0.9 <= razao <= 1.05)

    def test_p2233_regime_velocidade(self):
        cm, cr, rz = calculos.p2233_mpc_regime_velocidade(s0=(-1.0, 1.5), alvo=-0.5, semente=23)
        # no regime cego a velocidade o planejamento vence claramente
        self.assertLess(cm, cr)
        self.assertLess(rz, 1.0)

    def test_p2234_horizonte_nao_monotono(self):
        custos, melhor, mc = calculos.p2234_horizonte_nao_monotono()
        # o melhor horizonte e H=6 (indice 2), nao o maior; mais horizonte nao e sempre melhor
        self.assertEqual((1, 3, 6, 12)[melhor], 6)
        self.assertGreater(custos[3], custos[2])  # H=12 pior que H=6

    def test_p2235_shooting_converge(self):
        custos, mono = calculos.p2235_shooting_converge()
        self.assertTrue(mono)  # custo nao-crescente em K

    def test_p2236_recusa_autoreplicacao(self):
        usa_subprocess, usa_rede = calculos.p2236_recusa_autoreplicacao()
        # os dois mecanismos da auto-operacao autonoma estao presentes no codigo recebido -> recusado
        self.assertTrue(usa_subprocess)
        self.assertTrue(usa_rede)
        # caso de controle limpo: um codigo sem rede nem subprocess nao e acusado
        limpo = "def f(x):\n    return x * x + 1\n"
        self.assertEqual(calculos.p2236_recusa_autoreplicacao(limpo), (False, False))

    def test_p1961_com_parte_93(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93))
        self.assertEqual(por[93], (5, 6))
        self.assertEqual((ok, tot), (58, 71))


if __name__ == "__main__":
    unittest.main()
