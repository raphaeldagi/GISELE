"""Testes de unidade da Parte 104 (a carta escondida; a fronteira do seno): `python3 -m unittest synthai.testes_parte104`."""

import unittest

import calculos
from synthai import jogo_cartas, posicional


class TesteParte104(unittest.TestCase):
    def test_p2561_duelo(self):
        slope, ev = calculos.p2561_duelo_carta_alta()
        self.assertAlmostEqual(slope, 1.0 / 13.0, places=12)
        self.assertTrue(0.49 <= ev <= 0.51)
        # P(ganhar|c) linear: todos os termos != 0 (regra da Parte 30)
        self.assertAlmostEqual(jogo_cartas.prob_ganhar_por_carta(7), 6.5 / 13.0, places=12)
        self.assertAlmostEqual(jogo_cartas.prob_ganhar_por_carta(13) - jogo_cartas.prob_ganhar_por_carta(12), 1.0 / 13.0, places=12)

    def test_p2562_limiar(self):
        self.assertEqual(calculos.p2562_limiar_pagar(7), 11)
        # controle: c=10 da exatamente 0,5 (nao > 0,5)
        self.assertEqual(jogo_cartas.prob_ganhar_dado_aposta(10, 7), 0.5)
        self.assertGreater(jogo_cartas.prob_ganhar_dado_aposta(11, 7), 0.5)

    def test_p2563_voi(self):
        frac, fechada = calculos.p2563_valor_info_oculta()
        self.assertAlmostEqual(fechada, 6.0 / 13.0, places=12)
        self.assertTrue(0.44 <= frac <= 0.48)

    def test_p2564_fronteira_seno(self):
        # MEDIDO: nesta maquina math.sin e corretamente arredondada nestes args (contar = 0) -> sin NAO e fronteira aqui
        self.assertEqual(calculos.p2564_fronteira_do_seno(100), 0)
        # o seno proprio concorda com math.sin a menos de ~1e-15 (precisao, nao arredondamento)
        self.assertAlmostEqual(posicional.sin_(1.0), __import__("math").sin(1.0), places=14)

    def test_p2565_invariancia(self):
        var, pk, pk2 = calculos.p2565_invariancia_translacao()
        self.assertLess(var, 1e-12)        # depende so de k
        self.assertNotAlmostEqual(pk, pk2, places=3)  # k diferente -> produto diferente (controle)

    def test_p2566_rodada71(self):
        saida = calculos.p2566_rodada71()
        self.assertEqual(len(saida), 8)   # d=8

    def test_p1961_com_parte_104(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=tuple(list(range(80, 82)) + [83] + list(range(84, 105))))
        self.assertEqual(por[104], (4, 5))   # (d) foi um erro honesto: sin nao e fronteira nos args benignos da Parte 104
        self.assertEqual((ok, tot), (111, 126))


if __name__ == "__main__":
    unittest.main()
