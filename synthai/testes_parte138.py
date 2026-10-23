"""Testes da Parte 138: synthai/memoria_congelada.py (de externos/pacote3/transferencia_metacognitiva.py) e as funções P3184–P3186 pelo nome."""
import unittest

import calculos as c
from synthai import memoria_congelada as m


class TestesMemoria(unittest.TestCase):
    def test_tarefas_familias_em_rodizio(self):
        t = m.gerar_tarefas(8, semente=5)
        self.assertEqual([x["familia"] for x in t], list(m.FAMILIAS) * 2)

    def test_contexto_cortes(self):
        self.assertEqual(m.contexto([2.0, 0.0], 1.0), "baixo")
        self.assertEqual(m.contexto([4.0, 0.0], 1.0), "medio")
        self.assertEqual(m.contexto([7.0, 0.0], 1.0), "alto")

    def test_fator_congelado(self):
        col = m.MemoriaFalhas()
        for i in range(10):
            col.registrar("baixo", "custo" if i < 2 else "aceita")
        col.registrar("alto", "custo")
        col.registrar("medio", "conflito")
        fator = col.congelar()
        self.assertAlmostEqual(fator("baixo"), 1 - 0.6 * 3 / 12)
        self.assertEqual(fator("alto"), 1.0)  # n < 8
        self.assertEqual(col.contagens["medio"], [0, 0])  # conflito não conta
        col.registrar("baixo", "custo")
        self.assertAlmostEqual(fator("baixo"), 1 - 0.6 * 3 / 12)  # congelada: não muda depois

    def test_executar_reduz_o_custo(self):
        t = m.gerar_tarefas(4, semente=9)[0]
        self.assertLess(m.executar(t, 0.05), 1.0)

    def test_comparacao_pareada(self):
        media, g, p, e, ic = m.comparacao_pareada([1.0, 1.0, 1.0, 1.0], [0.5, 1.0, 1.5, 1.0], list(m.FAMILIAS), replicas=200)
        self.assertAlmostEqual(media, 0.0)
        self.assertEqual((g, p, e), (1, 1, 2))
        self.assertLessEqual(ic[0], ic[1])


class TestesFuncoesParte138(unittest.TestCase):
    def test_p3184_contexto_e_curvatura(self):
        d, t = c.p3184_contexto_e_curvatura(direcoes=200)
        self.assertEqual(d, t)

    def test_p3185_memoria_congelada(self):
        r = c.p3185_memoria_congelada()
        self.assertEqual(r[0.05][2], 27)
        self.assertEqual(r[0.2][2], 19)
        for v in r.values():
            self.assertTrue(v[4][0] <= 0 <= v[4][1])

    def test_p3186_grupos_uteis(self):
        r = c.p3186_grupos_uteis()
        self.assertAlmostEqual(r[4][0], 0.9058, places=3)
        self.assertAlmostEqual(r[16][0], 0.8825, places=3)
        self.assertGreater(r[4][2], r[16][2])


if __name__ == "__main__":
    unittest.main()
