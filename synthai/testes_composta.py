"""Testes de unidade da `composta` e do `pensamento_rico` (Parte 29): `python3 -m unittest synthai.testes_composta`."""

import unittest

from calculos import _rng

from .ancora import SynthaiComAncora
from .composta import SynthaiComposta, composta_rica
from .mundos import MundoBandido, MundoSequencial
from .pensamento_exato import ajustar_logistica
from .pensamento_rico import PensamentoRico
from .reconhecimento import SynthaiExploradora
from .testes import acessos_escondidos


class TesteComposta(unittest.TestCase):
    def test_fora_do_bandido_decide_como_a_ancorada(self):
        m = MundoSequencial(21)
        a = m.rodar(SynthaiComposta(21).calibrar(m, 40), 15)
        m = MundoSequencial(21)
        b = m.rodar(SynthaiComAncora(21, z=0.8416, auditoria=True).calibrar(m, 40), 15)
        self.assertEqual(a, b)

    def test_no_bandido_decide_como_a_principal(self):
        m = MundoBandido(22)
        a = m.rodar(SynthaiComposta(22).calibrar(m, 40), 1)
        m = MundoBandido(22)
        b = m.rodar(SynthaiExploradora(22).calibrar(m, 40), 1)
        self.assertEqual(a, b)

    def test_troca_de_modulo_de_fora(self):
        c = composta_rica(1)
        self.assertIsInstance(c.fora.pensamento, PensamentoRico)
        self.assertIs(c.fora.percepcao.pensamento, c.fora.pensamento)


class TestePensamentoRico(unittest.TestCase):
    def test_dez_pesos(self):
        p = PensamentoRico()
        self.assertEqual(len(p.w), 10)
        hist = MundoSequencial(23).historico_auditado(1)
        o, _, s = hist[0][0]
        self.assertEqual(len(p._x(o, 0.0, s)), 10)

    def test_ridge_zero_e_o_ajuste_antigo(self):
        rng = _rng(24)
        xs = [(1.0, rng.gauss(0, 1)) for _ in range(3000)]
        ys = [1.0 if rng.random() < 1 / (1 + 2.718281828459045 ** (2 - 1.2 * x[1])) else 0.0 for x in xs]
        self.assertEqual(ajustar_logistica(xs, ys, firth=False), ajustar_logistica(xs, ys, firth=False, ridge=0.0))
        w0 = ajustar_logistica(xs, ys, firth=False)
        w1 = ajustar_logistica(xs, ys, firth=False, ridge=50.0)
        self.assertLess(abs(w1[1]), abs(w0[1]))  # a penalidade encolhe a inclinação

    def test_recupera_uma_logistica_quadratica(self):
        rng = _rng(25)
        xs, ys = [], []
        for _ in range(40000):
            a = rng.gauss(0, 1)
            x = (1.0, a, 0.0, 0.0, a * a, 0.0, 0.0, 0.0, 0.0, 0.0)
            xs.append(x)
            ys.append(1.0 if rng.random() < 1 / (1 + 2.718281828459045 ** (2.0 - 0.5 * a - 0.8 * a * a)) else 0.0)
        w = ajustar_logistica(xs, ys, firth=False, ridge=1.0, iteracoes=40)
        self.assertLess(abs(w[4] - 0.8), 0.06)

    def test_nao_le_o_escondido(self):
        for nome in ("composta", "pensamento_rico"):
            self.assertEqual(acessos_escondidos(nome), [], nome)


if __name__ == "__main__":
    unittest.main()
