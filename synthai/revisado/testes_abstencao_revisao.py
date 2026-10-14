"""(Integrado na Parte 82, do pacote SYNTHAI_consolidado.py recebido do usuário; caminhos ajustados para synthai.revisado.)"""
"""Ausência de ação, custos preservados e feedback somente de ações executadas."""

import math
import unittest
from unittest.mock import Mock, patch

import calculos
from calculos import _rng

from .agente import Synthai
from .ancora import SynthaiComAncora
from .autorregulacao import SynthaiAutorregulada
from .composta import SynthaiComposta
from .mundos import CUSTO_LEITURA, Humano, MundoBandido, MundoSequencial, Opcao, Resultado, Situacao
from .reconhecimento import SynthaiReconhecida


def situacao(opcoes, restantes=0, horizonte=1, explorar=False):
    sit = Situacao(opcoes, restantes, 0.0, Humano(_rng(1), eps0=0, fadiga=0), _rng(2), 1.0, horizonte)
    sit.explorar = explorar
    return sit


def pensamento_fixo(agente, p):
    pensamento = Mock(w=[0.0] * 4)
    pensamento.p_catastrofe.return_value = p
    agente.pensamento = pensamento
    if hasattr(agente.percepcao, "pensamento"):
        agente.percepcao.pensamento = pensamento
    return pensamento


class TesteDecisaoAdmissivel(unittest.TestCase):
    def test_risco_excessivo_nao_vira_fallback(self):
        a = Synthai()
        pensamento_fixo(a, 0.99)
        self.assertIsNone(a.decidir(situacao([Opcao(1, 0, 1000, True)])))
        self.assertIsNone(a._escolha)

    def test_veto_nao_vira_fallback(self):
        a = Synthai()
        pensamento_fixo(a, 0.1)
        o = Opcao(1, 0, 1000, True)
        sit = situacao([o])
        self.assertIsNone(a.decidir(sit))
        self.assertEqual(a.vetados_agora, [o])
        self.assertEqual(sit.perguntas, 1)

    def test_falta_de_orcamento_nao_autoriza_acao(self):
        a = Synthai(carga_alvo=-1)
        pensamento_fixo(a, 0.1)
        sit = situacao([Opcao(1, 0, 1, False)])
        self.assertIsNone(a.decidir(sit))
        self.assertEqual(sit.perguntas, 0)

    def test_procura_alternativa_apos_veto(self):
        a = Synthai()
        p = pensamento_fixo(a, 0)
        vetada, aceita = Opcao(2, 0, 1000, True), Opcao(1, 0, 3, False)
        p.p_catastrofe.side_effect = [0.1, 0]
        self.assertIs(a.decidir(situacao([vetada, aceita])), aceita)
        self.assertEqual(a.vetados_agora, [vetada])

    def test_opcoes_vazias_limpam_estado_sem_percepcao(self):
        a = Synthai()
        p = pensamento_fixo(a, 0)
        o = Opcao(1, 0, 1, False)
        self.assertIs(a.decidir(situacao([o])), o)
        a.percepcao.perceber = Mock(side_effect=AssertionError("não deve perceber sem opções"))
        self.assertIsNone(a.decidir(situacao([])))
        a.observar(Resultado(o, False, 0, 0, 1))
        p.aprender.assert_not_called()
        self.assertEqual(a.vetados_agora, [])

    def test_variantes_herdam_abstencao(self):
        for cls in (SynthaiReconhecida, SynthaiAutorregulada, SynthaiComAncora):
            with self.subTest(agente=cls.__name__):
                a = cls()
                pensamento_fixo(a, 0.99)
                self.assertIsNone(a.decidir(situacao([Opcao(1, 0, 1, False)])))
                self.assertIsNone(a.decidir(situacao([], explorar=True)))


class TesteAbstencaoNosMundos(unittest.TestCase):
    def test_sequencial_conta_custos_sem_recompensa_ou_feedback(self):
        mundo = MundoSequencial(1, passos=3, n_acoes=1)
        mundo.humano.eps0 = mundo.humano.fadiga = 0
        a = Synthai()
        p = pensamento_fixo(a, 0.1)
        with patch("synthai.revisado.mundos._opcoes", side_effect=lambda *args: [Opcao(1, 0, 1000, True)]):
            r = mundo.rodar(a, 2)
        self.assertEqual(r["retorno"], -mundo.m["custo"] - CUSTO_LEITURA)
        self.assertEqual(r["bruto"], 0)
        self.assertEqual(r["catastrofes"], 0)
        self.assertEqual(r["abstencoes"], 1)
        self.assertEqual(r["acoes"], 0)
        self.assertEqual(r["cobertura"], 0)
        self.assertEqual(r["concluidos"], 0)
        self.assertEqual((r["perguntas"], r["leituras"]), (1, 1))
        p.aprender.assert_not_called()

    def test_sequencial_preserva_ganho_anterior_a_abstencao(self):
        mundo = MundoSequencial(1, passos=3, n_acoes=1)
        a = Synthai()
        p = pensamento_fixo(a, 0)
        p.p_catastrofe.side_effect = [0, 0.99]
        with patch("synthai.revisado.mundos._opcoes", side_effect=[
            [Opcao(1, 0, 3, False)], [Opcao(1, 0, 1000, True)]
        ]):
            r = mundo.rodar(a, 1)
        self.assertEqual(r["bruto"], 3)
        self.assertEqual(r["retorno"], 3 - 2*CUSTO_LEITURA)
        self.assertEqual((r["acoes"], r["abstencoes"], r["concluidos"]), (1, 1, 0))
        self.assertEqual(r["cobertura"], 1/3)
        p.aprender.assert_called_once()

    def test_horizonte_completo_tem_cobertura_um(self):
        mundo = MundoSequencial(1, passos=2, n_acoes=1)
        a = Synthai()
        pensamento_fixo(a, 0)
        with patch("synthai.revisado.mundos._opcoes", side_effect=lambda *args: [Opcao(1, 0, 3, False)]):
            r = mundo.rodar(a, 2)
        self.assertEqual((r["acoes"], r["abstencoes"], r["concluidos"], r["cobertura"]), (2, 0, 1, 1))

    def test_catastrofe_sequencial_interrompe_sem_contar_abstencao(self):
        for passos in (1, 2):
            with self.subTest(passos=passos):
                mundo = MundoSequencial(1, passos=passos, n_acoes=1)
                a = Synthai()
                pensamento_fixo(a, 0)
                with patch("synthai.revisado.mundos._opcoes", return_value=[Opcao(1, 0, 1000, True)]):
                    r = mundo.rodar(a, 1)
                self.assertEqual((r["catastrofes"], r["abstencoes"], r["concluidos"], r["cobertura"]),
                                 (1, 0, 0, 1/passos))

    def test_bandido_sem_braco_seguro_pode_encerrar(self):
        mundo = MundoBandido(1, bracos=1, puxadas=3)
        mundo.humano.eps0 = 0
        a = Synthai()
        p = pensamento_fixo(a, 0.1)
        with patch("synthai.revisado.mundos._gerar_acoes", return_value=[(1, 0, 1000, True)]):
            r = mundo.rodar(a, 1)
        self.assertEqual(r["retorno"], -0.1-CUSTO_LEITURA)
        self.assertEqual((r["acoes"], r["abstencoes"], r["concluidos"], r["cobertura"]), (0, 1, 0, 0))
        self.assertEqual(mundo.diagnostico, {"recompensa": 0, "teto": 0, "lai_robbins": 0})
        self.assertEqual(a.vetados_agora[0].vezes, 0)
        p.aprender.assert_not_called()

    def test_bandido_nao_apaga_teto_apos_abstencao(self):
        mundo = MundoBandido(1, bracos=1, puxadas=3)
        uniforme_original = mundo.fontes.uniforme
        mundo.fontes = Mock(wraps=mundo.fontes)
        mundo.fontes.uniforme.side_effect = lambda canal, *coords: (
            0 if canal == "recompensas" else uniforme_original(canal, *coords))
        a = Synthai()
        p = pensamento_fixo(a, 0)
        p.p_catastrofe.side_effect = [0, 0.99]
        with patch("synthai.revisado.mundos._gerar_acoes", return_value=[(1, 0, 0, False)]):
            r = mundo.rodar(a, 1)
        self.assertEqual((r["bruto"], r["acoes"], r["abstencoes"], r["cobertura"]), (1, 1, 1, 1/3))
        self.assertEqual(mundo.diagnostico["teto"], 1.5)
        self.assertEqual(mundo.diagnostico["recompensa"], 1)
        self.assertEqual(p.aprender.call_count, 1)
        self.assertEqual(p.aprender.call_args.args[0].vezes, 1)


class TesteFeedbackNaComposicao(unittest.TestCase):
    def test_autorregulacao_nao_concatena_episodio_abandonado(self):
        a = SynthaiAutorregulada(newton=False)
        p = pensamento_fixo(a, 0)
        p.p_catastrofe.side_effect = [0, 0.99, 0, 0]
        mundo = MundoSequencial(1, passos=2, n_acoes=1)
        with patch("synthai.revisado.mundos._opcoes", side_effect=[
            [Opcao(1, 0, 2, False)], [Opcao(1, 0, 1000, True)],
            [Opcao(1, 0, 5, False)], [Opcao(1, 0, 7, False)]
        ]):
            r = mundo.rodar(a, 2)
        self.assertEqual(a.futuro_soma, {0: 12, 1: 7})
        self.assertEqual(a.futuro_n, {0: 1, 1: 1})
        self.assertEqual(a.ganhos, [])
        self.assertEqual(a.decisoes, 3)
        self.assertEqual(a.n_r, 3)
        self.assertIsNone(a._pendente)
        self.assertEqual(r["concluidos"], 0.5)

    def test_autorregulacao_sem_orcamento_nao_cria_contrafactual(self):
        a = SynthaiAutorregulada(carga_alvo=-1)
        p = pensamento_fixo(a, 0.1)
        o = Opcao(1, 0, 1, False)
        a._pendente = (o, 0.1, 0, 1)
        a.ganhos = [10]
        self.assertIsNone(a.decidir(situacao([o])))
        self.assertEqual((a.n_d, a.decisoes), (0, 0))
        self.assertIsNone(a._pendente)
        self.assertEqual(a.ganhos, [])
        a.observar(Resultado(o, False, 0, 0, 1000))
        self.assertEqual(a.n_r, 0)
        p.aprender.assert_not_called()

    def test_composta_preserva_vetos_e_bloqueia_feedback_sem_acao(self):
        fora, bandido = Mock(), Mock()
        o = Opcao(1, 0, 1, False)
        fora.decidir.return_value = o
        bandido.decidir.return_value = None
        bandido.vetados_agora = [o]
        a = SynthaiComposta(fora=fora, bandido=bandido)
        self.assertIs(a.decidir(situacao([o])), o)
        res = Resultado(o, False, 0, 0, 1)
        a.observar(res)
        a.observar(res)
        fora.observar.assert_called_once_with(res)
        self.assertIsNone(a.decidir(situacao([o], explorar=True)))
        self.assertEqual(a.vetados_agora, [o])
        a.observar(res)
        bandido.observar.assert_not_called()


class TesteInstrumentacaoHistorica(unittest.TestCase):
    # test_auditorias_nao_inventam_valor_de_substituta_ausente: retirado na integração (Parte 82). Ele exercita as versões REESCRITAS
    # de p287, p314, p316 e p322 do calculos.py do pacote recebido, que não foram integradas (são experimentos históricos medidos;
    # reescrevê-las mudaria resultados publicados). As correções de abstenção que elas usam estão neste subpacote.
    pass


if __name__ == "__main__":
    unittest.main()
