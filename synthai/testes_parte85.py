"""Testes de unidade da Parte 85 (a arquitetura recursiva recebida): `python3 -m unittest synthai.testes_parte85`."""

import math
import unittest

import calculos


class TesteParte85(unittest.TestCase):
    def test_p1991_cosseno_duplicado(self):
        self.assertEqual(calculos.p1991_cosseno_duplicado_recebido(), [1.3, 0.5, -0.3, -0.5, -0.7])
        # controle: beta=0 recupera o termo cos^2*sinal puro; em 90 graus da 0
        self.assertEqual(calculos.p1991_cosseno_duplicado_recebido(beta=0.0, angulos=(0, 90, 180)), [1.0, 0.0, -1.0])

    def test_p1992_sem_treino(self):
        escritas, tem = calculos.p1992_pilha_adversarial_sem_treino()
        self.assertEqual((escritas, tem), (0, False))
        # controle: um codigo COM atualizacao de self.layers fora do __init__ e detectado
        com_treino = ("class SevenLevelAdversarialStack:\n"
                      "    def __init__(self, d):\n        self.layers = [0]\n"
                      "    def treina(self):\n        self.layers = [1]\n")
        self.assertEqual(calculos.p1992_pilha_adversarial_sem_treino(com_treino), (1, True))

    def test_p1993_buraco(self):
        buracos = calculos.p1993_buraco_do_escrutinio()
        self.assertEqual(len(buracos), 3)
        self.assertIn((0.6, 0.5, False), buracos)
        # controle: um caso consistente (soma<=1) nao e buraco; um trivial tambem nao
        self.assertEqual(calculos.p1993_buraco_do_escrutinio([(0.4, 0.3), (0.95, 0.95)]), [])

    def test_p1994_preso_na_esfera(self):
        self.assertLess(calculos.p1994_vetor_preso_na_esfera(passos=20), 1e-6)

    def test_p1961_com_parte_85(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao(partes=(80, 81, 83, 84, 85))
        self.assertEqual(por[85], (4, 4))  # a (e) do 85 e descartada; sobram a,b,c,d
        self.assertEqual((ok, tot), (27, 35))

    def test_p1995_rodada52(self):
        melhor_i, melhor_e, mudancas = calculos.p1995_rodada52()
        self.assertEqual((melhor_i, melhor_e), (15, 0.0))
        self.assertTrue(0 < mudancas < 300)


if __name__ == "__main__":
    unittest.main()
