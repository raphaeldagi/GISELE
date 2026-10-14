"""(Integrado na Parte 82, do pacote SYNTHAI_consolidado.py recebido do usuário; caminhos ajustados para synthai.revisado.)"""
"""Eventos comuns apesar de calibração, consultas, escolhas e durações diferentes."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from calculos import _rng

from .aleatoriedade import FontesAleatorias
from .mundos import Humano, MundoBandido, MundoSequencial, Opcao, Situacao


def assinatura(o):
    # A régua pode registrar o mundo; isto não é uma interface pública do agente.
    return (o.comite, o.discordancia, o._valor, o._catastrofe, o._consequencia, o.estimativa)


def assinatura_hist(hist):
    return [[(assinatura(o), rotulo, leitura) for o, rotulo, leitura in ep] for ep in hist]


class RastreioSequencial:
    vetados_agora = ()

    def __init__(self, ler=(), perguntar=(), acao=0, parar_em=None):
        self.ler, self.perguntar, self.acao, self.parar_em = ler, perguntar, acao, parar_em
        self.episodio = -1
        self.eventos, self.resultados = {}, []

    def decidir(self, sit):
        passo = sit.horizonte - 1 - sit.restantes
        if passo == 0:
            self.episodio += 1
        leituras = {i: sit.ler_sensor(sit.opcoes[i]) for i in self.ler}
        consultas, ocorrencias = [], {}
        for i in self.perguntar:
            n = ocorrencias.get(i, 0)
            u = sit._ruido_pergunta(sit.opcoes[i], n)
            consultas.append((i, n, u, sit.perguntar(sit.opcoes[i])))
            ocorrencias[i] = n + 1
        self.eventos[self.episodio, passo] = {
            "opcoes": tuple(assinatura(o) for o in sit.opcoes), "leituras": leituras,
            "consultas": consultas, "carga": sit.carga_do_humano, "leituras_cobradas": sit.leituras}
        if passo == self.parar_em or not sit.opcoes:
            return None
        return sit.opcoes[self.acao]

    def observar(self, res):
        self.resultados.append((res.valor_recebido, res.catastrofe))


class RastreioBandido:
    def __init__(self, escolhas=(0,), ler=(), perguntar=(), parar_primeira=False, vetar_primeiro=False):
        self.escolhas, self.ler, self.perguntar = escolhas, ler, perguntar
        self.parar_primeira, self.vetar_primeiro = parar_primeira, vetar_primeiro
        self.rodada = -1
        self.eventos, self.resultados = {}, {}
        self.vetados_agora = []

    def nova_rodada(self):
        self.rodada += 1
        self.puxada = 0

    def decidir(self, sit):
        self.puxada += 1
        if self.puxada == 1:
            self.bracos = list(sit.opcoes)
        self.vetados_agora = [self.bracos[0]] if self.vetar_primeiro and self.puxada == 1 else []
        leituras = {i: sit.ler_sensor(self.bracos[i]) for i in self.ler}
        consultas, ocorrencias = [], {}
        for i in self.perguntar:
            n = ocorrencias.get(i, 0)
            u = sit._ruido_pergunta(self.bracos[i], n)
            consultas.append((i, n, u, sit.perguntar(self.bracos[i])))
            ocorrencias[i] = n + 1
        self.eventos[self.rodada, self.puxada] = {
            "opcoes": tuple((o.comite, o.discordancia, o._valor, o._catastrofe) for o in self.bracos),
            "leituras": leituras, "consultas": consultas, "leituras_cobradas": sit.leituras,
            "disponiveis": tuple(self.bracos.index(o) for o in sit.opcoes)}
        if self.parar_primeira and self.rodada == 0 or not sit.opcoes:
            return None
        i = self.escolhas[min(self.puxada - 1, len(self.escolhas) - 1)]
        return self.bracos[i]

    def observar(self, res):
        self.resultados[self.rodada, self.puxada] = {
            "braco": self.bracos.index(res.opcao), "recompensa": res.valor_recebido, "catastrofe": res.catastrofe}


class TesteFontesCoordenadas(unittest.TestCase):
    def test_repetir_evento_nao_depende_de_consumo_de_outros(self):
        f = FontesAleatorias(17, "teste")
        antes = f.uniforme("recompensas", 2, 3, 1)
        outro = f.gerador("consultas", 2, 3, 1)
        for _ in range(100):
            outro.random()
        self.assertEqual(f.uniforme("recompensas", 2, 3, 1), antes)
        self.assertNotEqual(f.uniforme("recompensas", 2, 3, 2), antes)
        self.assertNotEqual(FontesAleatorias(17, "outro").uniforme("recompensas", 2, 3, 1), antes)

    def test_derivacao_nao_depende_de_pythonhashseed(self):
        programa = ("import json; from synthai.revisado.aleatoriedade import FontesAleatorias; "
                    "f=FontesAleatorias(17,'teste'); "
                    "print(json.dumps([f.uniforme('consultas',1,2,3),f.gerador('sensor',4).gauss(0,1)]))")
        saidas = []
        for valor in ("1", "97"):
            ambiente = dict(os.environ, PYTHONHASHSEED=valor)
            saidas.append(subprocess.check_output([sys.executable, "-c", programa], env=ambiente,
                                                 cwd=Path(__file__).resolve().parents[2], text=True))
        self.assertEqual(json.loads(saidas[0]), json.loads(saidas[1]))

    def test_contextos_invalidos_sao_recusados(self):
        for semente, mundo in ((True, "teste"), (1.5, "teste"), (1, "")):
            with self.subTest(semente=semente, mundo=mundo), self.assertRaises(ValueError):
                FontesAleatorias(semente, mundo)
        f = FontesAleatorias(1, "teste")
        for canal, coords in (("", ()), ("x", (-1,)), ("x", (True,)), ("x", (1.5,))):
            with self.subTest(canal=canal, coords=coords), self.assertRaises(ValueError):
                f.gerador(canal, *coords)


class TesteCalibracaoIndependente(unittest.TestCase):
    def test_quantidade_de_historico_nao_desloca_execucao(self):
        for tipo in ("sequencial", "bandido"):
            referencias = []
            for n in (0, 2, 5):
                mundo = (MundoSequencial(8, passos=2, n_acoes=5, p_cat=0) if tipo == "sequencial"
                         else MundoBandido(8, bracos=5, puxadas=2))
                mundo.historico_auditado(n)
                a = RastreioSequencial(ler=(0,)) if tipo == "sequencial" else RastreioBandido(ler=(0,))
                mundo.rodar(a, 2)
                referencias.append((a.eventos, a.resultados))
            with self.subTest(tipo=tipo):
                self.assertEqual(referencias[0], referencias[1])
                self.assertEqual(referencias[1], referencias[2])

    def test_historico_em_lotes_com_execucao_entre_eles(self):
        for tipo in ("sequencial", "bandido"):
            fazer = lambda: (MundoSequencial(8, passos=2, n_acoes=5, p_cat=0) if tipo == "sequencial"
                             else MundoBandido(8, bracos=5, puxadas=2))
            completo, dividido = fazer(), fazer()
            alvo = assinatura_hist(completo.historico_auditado(5))
            inicio = dividido.historico_auditado(2)
            a = RastreioSequencial(perguntar=(0,)) if tipo == "sequencial" else RastreioBandido(perguntar=(0,))
            dividido.rodar(a, 2)
            fim = dividido.historico_auditado(3)
            with self.subTest(tipo=tipo):
                self.assertEqual(assinatura_hist(inicio + fim), alvo)
                self.assertEqual(dividido.protocolo_aleatorio["historicos_emitidos"], 5)

    def test_quantidades_invalidas_nao_avancam_contadores(self):
        for fazer, a, contador in ((lambda: MundoSequencial(8), RastreioSequencial(), "episodios_iniciados"),
                                   (lambda: MundoBandido(8), RastreioBandido(), "rodadas_iniciadas")):
            mundo = fazer()
            for n in (-1, True, 1.5):
                with self.assertRaises(ValueError):
                    mundo.historico_auditado(n)
            for n in (0, -1, True, 1.5):
                with self.assertRaises(ValueError):
                    mundo.rodar(a, n)
            self.assertEqual(mundo.historico_auditado(0), [])
            self.assertEqual(mundo.protocolo_aleatorio[contador], 0)
            self.assertEqual(mundo.protocolo_aleatorio["historicos_emitidos"], 0)


class TesteSensorEConsultas(unittest.TestCase):
    def test_ordem_subconjunto_e_repeticao_nao_deslocam_leitura_comum(self):
        a, b = RastreioSequencial(ler=(2, 0, 1, 1), parar_em=0), RastreioSequencial(ler=(1,), parar_em=0)
        ra = MundoSequencial(8, passos=1, n_acoes=3, p_cat=0).rodar(a, 1)
        rb = MundoSequencial(8, passos=1, n_acoes=3, p_cat=0).rodar(b, 1)
        self.assertEqual(a.eventos[0, 0]["leituras"][1], b.eventos[0, 0]["leituras"][1])
        self.assertEqual((ra["leituras"], rb["leituras"]), (3, 1))

    def test_consultas_repetidas_nao_deslocam_outra_opcao(self):
        a, b = RastreioSequencial(perguntar=(0, 0, 1), parar_em=0), RastreioSequencial(perguntar=(1,), parar_em=0)
        MundoSequencial(8, passos=1, n_acoes=3, p_cat=0).rodar(a, 1)
        MundoSequencial(8, passos=1, n_acoes=3, p_cat=0).rodar(b, 1)
        qa, qb = a.eventos[0, 0]["consultas"], b.eventos[0, 0]["consultas"]
        self.assertNotEqual(qa[0][2], qa[1][2])
        self.assertEqual(qa[-1], qb[0])

    def test_consultas_e_leituras_adicionais_nao_deslocam_cenarios(self):
        a, b = RastreioSequencial(ler=(0, 1), perguntar=(0, 0, 1)), RastreioSequencial(ler=(1,))
        ma, mb = MundoSequencial(8, passos=2, n_acoes=3, p_cat=0), MundoSequencial(8, passos=2, n_acoes=3, p_cat=0)
        ma.rodar(a, 3)
        mb.rodar(b, 3)
        for chave in a.eventos:
            self.assertEqual(a.eventos[chave]["opcoes"], b.eventos[chave]["opcoes"])
            self.assertEqual(a.eventos[chave]["leituras"][1], b.eventos[chave]["leituras"][1])
        self.assertGreater(ma.humano.carga, mb.humano.carga)

    def test_mesmo_uniforme_nao_apaga_efeito_da_fadiga(self):
        o = Opcao(1, 0, 1, False)
        descansado, cansado = Humano(_rng(1)), Humano(_rng(1))
        cansado.carga = 1
        self.assertFalse(descansado.responder(o, uniforme=0.2))
        self.assertTrue(cansado.responder(o, uniforme=0.2))

    def test_fallback_sequencial_de_situacao_permanece(self):
        o = Opcao(1, 0, 1, False)
        humano = Humano(_rng(1), eps0=0)
        sit = Situacao([o], 0, 0, humano, _rng(2), 1)
        leitura = sit.ler_sensor(o)
        self.assertEqual(sit.ler_sensor(o), leitura)
        self.assertEqual(sit.leituras, 1)
        self.assertFalse(sit.perguntar(o))
        self.assertEqual(sit.perguntas, 1)
        class HumanoAntigo(Humano):
            def responder(self, opcao):
                return True
        antigo = Situacao([o], 0, 0, HumanoAntigo(_rng(1)), _rng(2), 1)
        self.assertTrue(antigo.perguntar(o))


class TesteDuracoesEEscolhasDiferentes(unittest.TestCase):
    def test_abstencao_nao_desloca_episodio_seguinte(self):
        a, b = RastreioSequencial(parar_em=0), RastreioSequencial()
        MundoSequencial(8, passos=3, n_acoes=3, p_cat=0).rodar(a, 3)
        MundoSequencial(8, passos=3, n_acoes=3, p_cat=0).rodar(b, 3)
        for ep in range(3):
            self.assertEqual(a.eventos[ep, 0]["opcoes"], b.eventos[ep, 0]["opcoes"])

    def test_catastrofe_nao_desloca_episodio_seguinte(self):
        def opcoes(rng, m, com_futuro):
            nota = rng.random()
            return [Opcao(nota, 0, 1000, True), Opcao(-nota, 0, 1, False)]
        a, b = RastreioSequencial(acao=0), RastreioSequencial(acao=1)
        with patch("synthai.revisado.mundos._opcoes", side_effect=opcoes):
            ra = MundoSequencial(8, passos=3, n_acoes=2).rodar(a, 3)
            rb = MundoSequencial(8, passos=3, n_acoes=2).rodar(b, 3)
        self.assertEqual((ra["catastrofes"], rb["catastrofes"]), (1, 0))
        self.assertNotEqual(ra["cobertura"], rb["cobertura"])
        for ep in range(3):
            self.assertEqual(a.eventos[ep, 0]["opcoes"], b.eventos[ep, 0]["opcoes"])

    def test_bandido_escolhas_anteriores_nao_deslocam_resultado_comum(self):
        for semente in (2, 22):
            a, b = RastreioBandido(escolhas=(0, 1)), RastreioBandido(escolhas=(1, 1))
            with patch("synthai.revisado.mundos._gerar_acoes", return_value=[(0, 0, 0, False), (1, 0, 0, True)]):
                MundoBandido(semente, bracos=2, puxadas=2).rodar(a, 1)
                MundoBandido(semente, bracos=2, puxadas=2).rodar(b, 1)
            with self.subTest(semente=semente):
                self.assertEqual(a.resultados[0, 2], b.resultados[0, 2])

    def test_bandido_consultas_e_sensor_nao_deslocam_recompensas(self):
        a, b = RastreioBandido(ler=(2, 0, 1), perguntar=(0, 0, 1)), RastreioBandido(ler=(1,), perguntar=(1,))
        MundoBandido(8, bracos=3, puxadas=3).rodar(a, 2)
        MundoBandido(8, bracos=3, puxadas=3).rodar(b, 2)
        self.assertEqual(a.resultados, b.resultados)
        for chave in a.eventos:
            self.assertEqual(a.eventos[chave]["leituras"][1], b.eventos[chave]["leituras"][1])
            self.assertEqual(a.eventos[chave]["consultas"][-1], b.eventos[chave]["consultas"][0])
        self.assertEqual(a.eventos[0, 2]["leituras_cobradas"], 0)

    def test_vetos_nao_renumeram_ruido_dos_bracos_restantes(self):
        a, b = RastreioBandido(escolhas=(1,), ler=(1,), perguntar=(1,), vetar_primeiro=True), \
               RastreioBandido(escolhas=(1,), ler=(1,), perguntar=(1,))
        with patch("synthai.revisado.mundos._gerar_acoes", return_value=[(0, 0, 0, False), (1, 0, 0, True)]):
            MundoBandido(8, bracos=2, puxadas=2).rodar(a, 1)
            MundoBandido(8, bracos=2, puxadas=2).rodar(b, 1)
        self.assertEqual(a.eventos[0, 2]["disponiveis"], (1,))
        self.assertEqual(b.eventos[0, 2]["disponiveis"], (0, 1))
        self.assertEqual(a.eventos[0, 2]["consultas"], b.eventos[0, 2]["consultas"])
        self.assertEqual(a.resultados[0, 2], b.resultados[0, 2])

    def test_rodada_abandonada_nao_desloca_rodada_seguinte(self):
        a, b = RastreioBandido(parar_primeira=True), RastreioBandido()
        MundoBandido(8, bracos=3, puxadas=3).rodar(a, 2)
        MundoBandido(8, bracos=3, puxadas=3).rodar(b, 2)
        self.assertEqual(a.eventos[1, 1]["opcoes"], b.eventos[1, 1]["opcoes"])
        self.assertEqual(a.resultados[1, 1], b.resultados[1, 1])

    def test_execucao_em_lotes_preserva_eventos_e_metricas(self):
        for tipo in ("sequencial", "bandido"):
            fazer = lambda: (MundoSequencial(8, passos=2, n_acoes=3, p_cat=0) if tipo == "sequencial"
                             else MundoBandido(8, bracos=3, puxadas=3))
            completo, dividido = fazer(), fazer()
            a = RastreioSequencial(ler=(0,), perguntar=(0,)) if tipo == "sequencial" else RastreioBandido(ler=(0,))
            b = RastreioSequencial(ler=(0,), perguntar=(0,)) if tipo == "sequencial" else RastreioBandido(ler=(0,))
            alvo = completo.rodar(a, 4)
            inicio, fim = dividido.rodar(b, 1), dividido.rodar(b, 3)
            with self.subTest(tipo=tipo):
                self.assertEqual(a.eventos, b.eventos)
                self.assertEqual(a.resultados, b.resultados)
                for campo in alvo:
                    self.assertAlmostEqual(alvo[campo], (inicio[campo] + 3*fim[campo])/4)


if __name__ == "__main__":
    unittest.main()
