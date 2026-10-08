"""Testes de unidade dos módulos (P286): `python3 -m unittest synthai.testes`.

Cada teste fixa uma propriedade que a série já demonstrou, agora no módulo isolado."""

import ast
import os
import unittest
from math import isclose

from calculos import _rng, p71_valor_da_pergunta

from .agente import Synthai
from .intuicao import Intuicao
from .metacognicao import auc, comparacao_pareada, normalizado
from .mundos import MundoBandido, MundoSequencial, Opcao, Situacao, Humano
from .pensamento import Pensamento
from .percepcao import Percepcao
from .relacao import Relacao
from .sentimento import Sentimento

MODULOS_DO_AGENTE = ("percepcao", "pensamento", "intuicao", "sentimento", "relacao", "agente")


def _situacao(opcoes, restantes=0, horizonte=1, semente=1):
    rng = _rng(semente)
    return Situacao(opcoes, restantes, 0.0, Humano(rng), _rng(semente + 1), 1.0, horizonte)


def acessos_escondidos(nome):
    """Atributos com `_` lidos de objetos que não são `self` (o que o agente não poderia saber, P7)."""
    caminho = os.path.join(os.path.dirname(__file__), nome + ".py")
    arvore = ast.parse(open(caminho, encoding="utf-8").read())
    return [n.attr for n in ast.walk(arvore) if isinstance(n, ast.Attribute) and n.attr.startswith("_")
            and not n.attr.startswith("__") and not (isinstance(n.value, ast.Name) and n.value.id == "self")]


class TestePercepcao(unittest.TestCase):
    def test_atencao_le_so_o_foco(self):
        opcoes = [Opcao(i, 0.0, 0.0, False) for i in range(50)]
        sit = _situacao(opcoes)
        lidas = Percepcao(foco=0.1).perceber(sit)
        self.assertEqual(len(lidas), 5)
        self.assertEqual(sit.leituras, 5)
        self.assertEqual(set(lidas), {id(o) for o in opcoes[-5:]})  # as cinco de nota mais alta


class TestePensamento(unittest.TestCase):
    def test_calibracao_separa_catastrofes(self):
        mundo = MundoSequencial(7, passos=1, n_acoes=200)
        p = Pensamento()
        p.calibrar(mundo.historico_auditado(150))
        teste = mundo.historico_auditado(100)
        esc, rot = [], []
        for ep in teste:
            melhor = max(o.comite for o, _, _ in ep)
            for o, r, s in ep:
                esc.append(p.p_catastrofe(o, melhor, s))
                rot.append(r)
        self.assertGreater(auc(esc, rot), 0.8)


class TesteIntuicao(unittest.TestCase):
    def test_peso_aprendido_e_um_sobre_um_mais_sigma2(self):  # P272/P273
        rng = _rng(3)
        i = Intuicao()
        for _ in range(20000):
            c = rng.gauss(0, 1)
            i.corrigir(c + rng.gauss(0, 2.0), 0.0, c)
        self.assertLess(abs(i.peso - 0.2), 0.02)

    def test_bonus_no_bandido_e_exploracao(self):
        o = Opcao(0, 0, 0, False, estimativa=0.7)
        sit = _situacao([o], restantes=3)
        self.assertEqual(Intuicao().bonus(o, sit), 0.7 * 3)
        sit.explorar = True
        self.assertEqual(Intuicao().bonus(o, sit), 0.7)


class TesteSentimento(unittest.TestCase):
    def test_quantiliza_e_alarga_no_ultimo_passo(self):
        opcoes = [Opcao(i, 0.0, 0.0, False) for i in range(100)]
        s, i = Sentimento(), Intuicao()
        ordem = s.ordenar(_situacao(opcoes), i)
        self.assertEqual(ordem[0].nota, 99)
        primeiras = {s.candidatas(ordem, _situacao(opcoes, 0, 5), _rng(k))[0].nota for k in range(200)}
        self.assertEqual(min(primeiras), 80)  # q_final = 20% no último de vários passos
        primeiras = {s.candidatas(ordem, _situacao(opcoes, 2, 5), _rng(k))[0].nota for k in range(200)}
        self.assertEqual(min(primeiras), 95)  # q = 5% nos outros


class TesteRelacao(unittest.TestCase):
    def test_limiar_da_p71_vezes_dois(self):
        self.assertTrue(isclose(Relacao().limiar, 2 * p71_valor_da_pergunta()))

    def test_orcamento_do_bandido(self):
        r = Relacao(orcamento_rodada=1)
        opcoes = [Opcao(0, 0, 0, True), Opcao(0, 0, 0, True)]
        sit = _situacao(opcoes)
        sit.explorar = True
        r.perguntar(opcoes[0], sit)
        self.assertTrue(r.pode_perguntar(opcoes[0], sit))   # já perguntado: a resposta fica guardada
        self.assertFalse(r.pode_perguntar(opcoes[1], sit))  # orçamento gasto


class TesteMetacognicao(unittest.TestCase):
    def test_reguas(self):
        self.assertEqual(auc([0.1, 0.9], [0, 1]), 1.0)
        m, _, _ = comparacao_pareada([1, 2, 3], [2, 3, 5])
        self.assertTrue(isclose(m, 4 / 3))
        self.assertEqual(normalizado(5, 0, 10), 0.5)


class TesteInterface(unittest.TestCase):
    def test_o_agente_nao_le_o_escondido(self):  # P7, P285
        for nome in MODULOS_DO_AGENTE:
            self.assertEqual(acessos_escondidos(nome), [], nome)

    def test_mesmo_agente_em_tres_tarefas(self):
        for mundo, n in ((MundoSequencial(11, passos=1, n_acoes=200), 20), (MundoSequencial(11), 10),
                         (MundoBandido(11), 1)):
            r = mundo.rodar(Synthai(11).calibrar(mundo, 30), n)
            self.assertEqual(set(r), {"retorno", "bruto", "catastrofes", "perguntas", "leituras"})


if __name__ == "__main__":
    unittest.main()
