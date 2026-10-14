"""Testes de unidade da Parte 89 (o substrato que aprende): `python3 -m unittest synthai.testes_parte89`."""

import unittest

import calculos
from synthai.plasticidade import stdp_integral, stdp_timing_controlado, competicao_sinaptica


class TesteParte89(unittest.TestCase):
    def test_p2111_integral(self):
        self.assertEqual(calculos.p2111_stdp_integral(), (0.0, -0.3999999999999999))
        # controle: potenciacao dominante da integral positiva
        self.assertGreater(stdp_integral(a_mais=0.15), 0)

    def test_p2112_deriva_sinal(self):
        soma, sinal = calculos.p2112_stdp_deriva_sinal()
        self.assertEqual(sinal, -1)      # depressao dominante
        self.assertLess(soma, 0)         # a simulacao tem o sinal da integral

    def test_p2113_timing(self):
        antes, depois = calculos.p2113_stdp_timing()
        self.assertGreater(antes, 0.5)   # pre antes do pos: potencia
        self.assertLess(depois, 0.5)     # pre depois do pos: deprime
        # controle: com dt=0 (sem ordem definida) o teste nao vale; usamos +-5ms
        self.assertGreater(antes, depois)

    def test_p2114_competicao_nao_separa(self):
        mc, mr, dif = calculos.p2114_competicao_toy()
        self.assertLess(dif, 0.15)       # nao separa nesta escala
        self.assertGreater(mc, 0.9)
        self.assertGreater(mr, 0.9)

    def test_p1961_com_parte_89(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85, 86, 87, 88, 89))
        self.assertEqual(por[89], (4, 4))
        self.assertEqual((ok, tot), (42, 54))

    def test_p2115_rodada56(self):
        self.assertEqual(calculos.p2115_rodada56(), 12)


if __name__ == "__main__":
    unittest.main()
