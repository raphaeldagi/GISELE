"""Testes de unidade da `autorregulacao` (Parte 27): `python3 -m unittest synthai.testes_autorregulacao`."""

import unittest

from calculos import _rng, p71_valor_da_pergunta

from .autorregulacao import RelacaoAutorregulada, SynthaiAutorregulada
from .mundos import Humano, MundoSequencial, Opcao, Resultado, Situacao
from .testes import acessos_escondidos


def _sit(opcoes, restantes=0, horizonte=1):
    return Situacao(opcoes, restantes, 0.0, Humano(_rng(1)), _rng(2), 1.0, horizonte)


class TesteAutorregulacao(unittest.TestCase):
    def test_relacao_anota_aceita_e_descartada(self):
        r = RelacaoAutorregulada(carga_alvo=-1.0)  # sem orçamento: toda pergunta vira descarte
        o = Opcao(1.0, 0.0, 0.0, False)
        self.assertFalse(r.precisa_perguntar(0.0))
        self.assertEqual(r.aceita_p, 0.0)
        self.assertFalse(r.pode_perguntar(o, _sit([o])))
        self.assertEqual(r.descartadas, [o])

    def test_termos_com_dados_feitos_a_mao(self):
        a = SynthaiAutorregulada(1)
        a.passos_cat = [0]
        a.futuro_soma, a.futuro_n = {0: 30.0}, {0: 2}           # F(0) = 15
        a.f_cat, a.f_p = 4.0, 2.0                               # f = 2
        a.n_r, a.sx, a.sy, a.sxx, a.sxy = 3.0, 6.0, 12.0, 14.0, 28.0  # y = 2x: inclinação 2
        a.n_d, a.d_nota, a.d_plano = 2.0, 1.0, 0.4              # Δd = (2 × 1 + 0,4) / 2 = 1,2
        l_ef, f, dd, b = a.termos()
        self.assertAlmostEqual(l_ef, 65.0)
        self.assertAlmostEqual(f, 2.0)
        self.assertAlmostEqual(b, 2.0)
        self.assertAlmostEqual(dd, 1.2)
        a.recalcular()
        self.assertAlmostEqual(a.mult, 1.2 / (2.0 * 65.0 * p71_valor_da_pergunta()))
        self.assertAlmostEqual(a.relacao.limiar, a.mult * p71_valor_da_pergunta())

    def test_limites_do_multiplicador(self):
        a = SynthaiAutorregulada(1)
        a.passos_cat, a.futuro_soma, a.futuro_n = [0], {0: 0.0}, {0: 1}
        a.n_r, a.sx, a.sy, a.sxx, a.sxy = 2.0, 0.0, 0.0, 2.0, 2.0
        a.n_d, a.d_nota, a.d_plano = 1.0, 1000.0, 0.0
        a.recalcular()
        self.assertEqual(a.mult, a.m_max)

    def test_observar_aprende_a_regressao_e_o_futuro(self):
        a = SynthaiAutorregulada(1)
        o = Opcao(2.0, 0.0, 2.0, False)
        a._pendente = (o, 0.001, 0, 1)
        a._escolha = None
        a.observar(Resultado(o, False, 0.0, 0.0, 2.0))
        self.assertEqual((a.n_r, a.sx, a.sy), (1.0, 2.0, 2.0))
        self.assertEqual(a.futuro_n, {0: 1})
        self.assertAlmostEqual(a.f_p, 0.5 + 0.001)

    def test_roda_e_recalcula(self):
        m = MundoSequencial(13)
        a = SynthaiAutorregulada(13, aquecimento=50, intervalo=25).calibrar(m, 30)
        m.rodar(a, 30)
        self.assertTrue(a.historico_m)

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("autorregulacao"), [])


if __name__ == "__main__":
    unittest.main()
