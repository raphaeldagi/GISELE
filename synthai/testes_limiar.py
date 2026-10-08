"""Testes de unidade do `limiar` (Parte 25): `python3 -m unittest synthai.testes_limiar`."""

import unittest

from calculos import p71_valor_da_pergunta

from .limiar import PensamentoLocal, SynthaiAjustada, dados_do_topo
from .mundos import MundoSequencial
from .pensamento_exato import dados_do_historico
from .testes import acessos_escondidos


class TesteLimiar(unittest.TestCase):
    def test_topo_usa_a_melhor_nota_do_episodio_inteiro(self):
        hist = MundoSequencial(41, passos=1, n_acoes=200).historico_auditado(3)
        xs, _ = dados_do_topo(hist, 0.1)
        todos, _ = dados_do_historico(hist)
        self.assertEqual(len(xs), 3 * 20)
        self.assertTrue(set(xs) <= set(todos))  # as mesmas variáveis, só um recorte

    def test_multiplicador_do_limiar(self):
        for m in (0.5, 2.0, 8.0):
            self.assertAlmostEqual(SynthaiAjustada(1, mult=m).relacao.limiar, m * p71_valor_da_pergunta())

    def test_local_troca_o_pensamento_na_percepcao_tambem(self):
        a = SynthaiAjustada(1, local=True)
        self.assertIsInstance(a.pensamento, PensamentoLocal)
        self.assertIs(a.percepcao.pensamento, a.pensamento)

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("limiar"), [])


if __name__ == "__main__":
    unittest.main()
