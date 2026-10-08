"""Testes de unidade do módulo `reconhecimento` (Parte 23): `python3 -m unittest synthai.testes_reconhecimento`.

Ficam num arquivo separado porque a P286 mede a suíte da Parte 22 (10 testes) e o número publicado não muda."""

import unittest

from calculos import _rng

from .mundos import Humano, MundoBandido, MundoSequencial, Opcao, Situacao, referencia_lai_robbins
from .pensamento import Pensamento
from .reconhecimento import IntuicaoBayes, LeiturasNeutras, PercepcaoReconhecida, SynthaiReconhecida
from .testes import acessos_escondidos


def _sit(opcoes, restantes=0, horizonte=1, explorar=False):
    rng = _rng(5)
    sit = Situacao(opcoes, restantes, 0.0, Humano(rng), _rng(6), 1.0, horizonte)
    sit.explorar = explorar
    return sit


class TesteReconhecimento(unittest.TestCase):
    def test_leitura_que_falta_vale_o_neutro(self):
        l = LeiturasNeutras({1: 2.0}, 0.4)
        self.assertEqual(l.get(1, 0.0), 2.0)
        self.assertEqual(l.get(2, 0.0), 0.4)

    def test_neutro_e_metade_do_peso(self):
        p = Pensamento()
        p.w = [0.0, 0.0, 0.0, 1.6]
        perc = PercepcaoReconhecida(foco=0.5, pensamento=p)
        lidas = perc.perceber(_sit([Opcao(i, 0, 0, False) for i in range(4)]))
        self.assertEqual(lidas.neutro, 0.8)

    def test_atencao_segue_a_intuicao(self):
        opcoes = [Opcao(1.0, 0, 0, False, estimativa=0.0), Opcao(0.0, 0, 0, False, estimativa=1.0)]
        perc = PercepcaoReconhecida(foco=0.5, pensamento=Pensamento(), intuicao=IntuicaoBayes())
        lidas = perc.perceber(_sit(opcoes, restantes=3, horizonte=5))
        self.assertIn(id(opcoes[1]), lidas)  # 0 + 1×3 > 1 + 0: lê a que o plano prefere

    def test_memoria_do_bandido(self):
        opcoes = [Opcao(float(i), 0, 0, False) for i in range(10)]
        perc = PercepcaoReconhecida(foco=0.1, pensamento=Pensamento(), atencao_inteira=False)
        sit = _sit(opcoes, explorar=True)
        perc.perceber(sit)
        opcoes[9].nota = -5.0  # agora outra é a mais promissora
        lidas = perc.perceber(_sit(opcoes, explorar=True))
        self.assertEqual(len(lidas), 2)  # a nova e a lembrada
        perc.esquecer()
        self.assertEqual(len(perc.perceber(_sit(opcoes, explorar=True))), 1)

    def test_thompson_concentra_com_dados(self):
        i = IntuicaoBayes(1)
        o = Opcao(0, 0, 0, False)
        o.vezes, o.sucessos = 1000, 700
        amostras = []
        for _ in range(200):
            i.nova_decisao()
            amostras.append(i.bonus(o, _sit([o], explorar=True)))
        self.assertLess(max(abs(a) for a in amostras), 0.06)

    def test_lai_robbins(self):
        self.assertEqual(referencia_lai_robbins([0.5, 0.5], 300), 0.0)
        self.assertGreater(referencia_lai_robbins([0.9, 0.5], 300), 0.0)
        self.assertLessEqual(referencia_lai_robbins([0.9, 0.89], 300), 0.01 * 300 + 1e-9)

    def test_nao_le_o_escondido(self):
        self.assertEqual(acessos_escondidos("reconhecimento"), [])

    def test_roda_nas_tres_tarefas(self):
        for mundo, n in ((MundoSequencial(12, passos=1, n_acoes=200), 10), (MundoSequencial(12), 5),
                         (MundoBandido(12), 1)):
            mundo.rodar(SynthaiReconhecida(12).calibrar(mundo, 30), n)


if __name__ == "__main__":
    unittest.main()
