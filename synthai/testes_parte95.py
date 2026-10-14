"""Testes de unidade da Parte 95 (o relatorio v2.0 recebido, auditado): `python3 -m unittest synthai.testes_parte95`."""

import sys
import unittest

import calculos
from synthai import evoluido


class TesteParte95(unittest.TestCase):
    def test_p2291_direcao_p_estrela(self):
        lo, hi, cresce = calculos.p2291_direcao_de_p_estrela()
        # P* cresce com eps -> a afirmacao do relatorio ('mais estrito') e falsa
        self.assertTrue(cresce)
        self.assertGreater(hi, lo)
        # caso de controle: com L maior, P* menor
        self.assertLess(evoluido.p_estrela(0.1, 0.1, 1000.0), evoluido.p_estrela(0.1, 0.1, 500.0))

    def test_p2292_ttts_nao_domina(self):
        ft, fs, dif = calculos.p2292_ttts_nao_domina()
        # ambas as fracoes sao probabilidades validas; a diferenca e modesta (nao 'drastica')
        self.assertTrue(0.0 <= ft <= 1.0 and 0.0 <= fs <= 1.0)
        self.assertLess(abs(dif), 0.30)

    def test_p2293_ewc_troca(self):
        alto_ok, baixo_ok, (ae, ai, be, bi) = calculos.p2293_ewc_troca_o_que_protege()
        # EWC segura o importante (Fisher alto) e libera o resto (Fisher baixo)
        self.assertTrue(alto_ok)
        self.assertTrue(baixo_ok)
        self.assertLess(ae, ai)
        self.assertGreater(be, bi)

    def test_p2294_oito_bits(self):
        rms, teo, razao = calculos.p2294_oito_bits_nao_e_float64()
        # o RMS de 8 bits esta longe do float64 (epsilon ~2.2e-16); a formula D/sqrt12 bate a menos de 20%
        self.assertGreater(razao, 1e10)
        self.assertLess(abs(rms - teo) / teo, 0.3)

    def test_quantizar_hex_roundtrip(self):
        # quantizar e recuperar um valor dentro de meio passo (todos os termos != 0)
        w = [0.9, -0.4, 0.1, -0.75]
        qw, codigos, passo = evoluido.quantizar_hex(w, bits=8)
        for a, b in zip(w, qw):
            self.assertLessEqual(abs(a - b), passo / 2.0 + 1e-12)
        self.assertTrue(all(c.startswith("0x") for c in codigos))

    def test_ttts_e_thompson_recomendam_validamente(self):
        import random
        rng = random.Random(0)
        ag = evoluido.TopTwoThompson(4, rng)
        for _ in range(50):
            i = ag.escolher()
            ag.atualizar(i, rng.random() < [0.9, 0.3, 0.3, 0.3][i])
        self.assertIn(ag.recomendar(), range(4))

    def test_p2295_rodada62(self):
        pesos, pcat = calculos.p2295_rodada62()
        self.assertEqual(len(pesos), 4)
        self.assertTrue(0.0 < pcat < 1.0)

    def test_p2296_vies_de_indice(self):
        reatribui, descasa = calculos.p2296_vies_de_indice_do_simulador()
        self.assertTrue(reatribui)
        self.assertTrue(descasa)
        # caso de controle limpo: um codigo que redefine o indice apos a migracao nao e acusado de descasamento
        limpo = ("idx_escolhido = esc()\n"
                 "acao_candidata = acoes[idx_escolhido]\n"
                 "if cond:\n"
                 "    acao_candidata = outra\n"
                 "    idx_escolhido = acoes.index(acao_candidata)\n"
                 "self.ttts.atualizar(idx_escolhido, sucesso=True)\n")
        _, descasa_limpo = calculos.p2296_vies_de_indice_do_simulador(limpo)
        self.assertFalse(descasa_limpo)

    def test_p1961_com_parte_95(self):
        ok, tot, frac, por = calculos.p1961_teste_e_da_calibracao()
        self.assertEqual(por[95], (5, 5))
        self.assertEqual((ok, tot), (68, 81))


if __name__ == "__main__":
    unittest.main()
