"""Testes de unidade do `pensamento_exato` (Parte 24): `python3 -m unittest synthai.testes_pensamento`."""

import unittest

from calculos import _rng

from .mundos import MundoSequencial
from .pensamento_exato import (PensamentoExato, SynthaiPensante, _inversa, ajustar_logistica, dados_do_historico,
                               perda_logistica)
from .testes import acessos_escondidos


class TestePensamentoExato(unittest.TestCase):
    def test_inversa(self):
        m = [[4.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]]
        inv = _inversa(m)
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(sum(m[i][k] * inv[k][j] for k in range(3)), 1.0 if i == j else 0.0)

    def test_newton_recupera_os_pesos(self):
        rng = _rng(31)
        xs, ys = [], []
        for _ in range(30000):
            x = rng.gauss(0, 1)
            xs.append((1.0, x))
            ys.append(1.0 if rng.random() < 1 / (1 + 2.718281828459045 ** (1.0 - 0.8 * x)) else 0.0)
        b, w = ajustar_logistica(xs, ys, firth=False)
        self.assertLess(abs(b + 1.0), 0.05)
        self.assertLess(abs(w - 0.8), 0.05)

    def test_firth_fica_finito_com_separacao(self):
        xs = [(1.0, float(x)) for x in range(-5, 6)]
        ys = [1.0 if x > 0 else 0.0 for x in range(-5, 6)]  # separação perfeita: a máxima verossimilhança diverge
        b, w = ajustar_logistica(xs, ys, firth=True, iteracoes=100)
        self.assertLess(abs(w), 10.0)

    def test_newton_nao_perde_para_o_gradiente_no_treino(self):
        mundo = MundoSequencial(32)
        hist = mundo.historico_auditado(60)
        xs, ys = dados_do_historico(hist)
        p = PensamentoExato(firth=False)
        p.calibrar(hist)
        from .pensamento import Pensamento
        g = Pensamento()
        g.calibrar(hist)
        self.assertLessEqual(perda_logistica(p.w, xs, ys), perda_logistica(g.w, xs, ys) + 1e-12)

    def test_mesmas_variaveis_do_pensamento(self):
        from .pensamento import Pensamento
        ep = MundoSequencial(33).historico_auditado(2)
        xs, _ = dados_do_historico(ep)
        melhor = max(o.comite for o, _, _ in ep[0])
        o, _, s = ep[0][0]
        self.assertEqual(xs[0], Pensamento()._x(o, melhor, s))

    def test_pensante_usa_o_mesmo_pensamento_na_percepcao(self):
        a = SynthaiPensante(1)
        self.assertIs(a.percepcao.pensamento, a.pensamento)

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("pensamento_exato"), [])


if __name__ == "__main__":
    unittest.main()
