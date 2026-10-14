"""(Integrado na Parte 82, do pacote SYNTHAI_consolidado.py recebido do usuário; caminhos ajustados para synthai.revisado.)"""
"""Integridade do benchmark, recusas sem publicação e reprodução dos registros."""

import hashlib
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import FunctionType
from unittest.mock import Mock, patch

from . import decisao, rsi
from .rsi import AvaliadorSelado, ConfiguracaoAvaliacao, genoma_inicial


class TesteDependenciasSeladas(unittest.TestCase):
    def setUp(self):
        self.av = AvaliadorSelado(k=3, t=30)

    def recusada(self):
        with self.assertRaises(RuntimeError):
            self.av.nota(genoma_inicial(), [1, 2])
        self.assertEqual(self.av.chamadas, 0)
        self.assertEqual(self.av.registros, ())

    def test_reproducao_da_troca_de_rodar_bandido(self):
        falsificador = Mock(return_value=[0])
        with patch.object(rsi, "rodar_bandido", falsificador):
            self.recusada()
        falsificador.assert_not_called()

    def test_troca_do_metodo_do_aprendiz(self):
        with patch.object(decisao.QEpsilon, "atualizar", lambda *args: None):
            self.recusada()

    def test_alteracao_de_codigo_sem_trocar_objeto(self):
        funcao = decisao.QEpsilon.atualizar
        original = funcao.__code__
        def nada(self, braco, recompensa):
            pass
        try:
            funcao.__code__ = nada.__code__
            self.recusada()
        finally:
            funcao.__code__ = original

    def test_alteracao_de_defaults_e_kwdefaults(self):
        for campo, valor in (("__defaults__", (1, 1)), ("__kwdefaults__", {"t": 1})):
            with self.subTest(campo=campo), patch.object(rsi.regret_do_genoma, campo, valor):
                self.recusada()

    def test_rebinding_de_funcao_com_codigo_identico(self):
        f = rsi.rodar_bandido
        copia = FunctionType(f.__code__, f.__globals__, f.__name__, f.__defaults__, f.__closure__)
        copia.__qualname__ = f.__qualname__
        with patch.object(rsi, "rodar_bandido", copia):
            # O manifesto é igual; a identidade privada detecta o rebinding.
            self.assertEqual(self.av.assinatura(), self.av.selo)
            self.recusada()

    def test_binding_do_modulo_de_origem_tambem_e_verificado(self):
        with patch.object(decisao, "rodar_bandido", lambda *args: [0]):
            self.recusada()

    def test_metodos_do_rng_sao_verificados(self):
        for metodo in ("choice", "seed", "_randbelow", "random"):
            with self.subTest(metodo=metodo), patch.object(random.Random, metodo, lambda *args: 0):
                self.recusada()

    def test_global_que_substitui_builtin_e_verificado(self):
        with patch.object(decisao, "max", lambda *args: 0, create=True):
            self.recusada()

    def test_adicao_de_atributo_da_classe_invalida_manifesto(self):
        with patch.object(decisao.QEpsilon, "novo_atributo", 1, create=True):
            self.recusada()

    def test_arquivo_alterado_ou_ausente_e_recusado(self):
        with tempfile.TemporaryDirectory() as d:
            copia = Path(d) / "decisao.py"
            copia.write_bytes(self.av._arquivos["decisao.py"].read_bytes())
            self.av._arquivos["decisao.py"] = copia
            # Localização diferente com conteúdo igual conserva o manifesto.
            self.assertEqual(self.av.assinatura(), self.av.selo)
            copia.write_bytes(copia.read_bytes() + b"\n# mudanca\n")
            self.recusada()
            copia.unlink()
            self.recusada()

    def test_configuracao_nao_pode_mudar_apos_criacao(self):
        self.av._config = ConfiguracaoAvaliacao(k=1, t=1)
        self.recusada()

    def test_limites_do_genoma_nao_podem_mudar_apos_criacao(self):
        with patch.dict(rsi.LIMITES, {"alfa": (0, 1)}):
            self.recusada()

    def test_reselar_tag_publica_nao_aprova_mudanca(self):
        with patch.object(rsi.regret_do_genoma, "__defaults__", (1, 1)):
            self.av.selo = self.av.assinatura()
            self.recusada()

    def test_mutacao_durante_calculo_nao_publica_nota(self):
        original, rodar_original = rsi.regret_do_genoma, rsi.rodar_bandido
        def muda_depois(genoma, sementes, k, t):
            nota = original(genoma, sementes, k, t)
            rsi.rodar_bandido = lambda *args: [0]
            return nota
        try:
            with patch.object(rsi, "regret_do_genoma", muda_depois):
                # A base é deliberadamente instrumentada para testar a checagem posterior.
                self.av = AvaliadorSelado(k=3, t=30)
                self.recusada()
        finally:
            rsi.rodar_bandido = rodar_original

    def test_iterador_que_muda_dependencias_e_recusado_antes_do_calculo(self):
        falsificador = Mock(return_value=[0])
        def sementes():
            yield 1
            rsi.rodar_bandido = falsificador
            yield 2
        original = rsi.rodar_bandido
        try:
            with self.assertRaises(RuntimeError):
                self.av.nota(genoma_inicial(), sementes())
            self.assertEqual(self.av.registros, ())
            falsificador.assert_not_called()
        finally:
            rsi.rodar_bandido = original


class TesteRegistrosEReproducao(unittest.TestCase):
    def test_nota_e_registro_podem_ser_reproduzidos(self):
        av = AvaliadorSelado(k=4, t=50)
        genoma = genoma_inicial()
        nota = av.nota(genoma, iter([1, 2, 3]))
        registro = av.registros[0]
        replay = AvaliadorSelado(**registro["configuracao"])
        self.assertEqual(replay.selo, registro["selo"])
        self.assertEqual(replay.nota(registro["genoma"], registro["sementes"]), nota)
        self.assertEqual(nota, -rsi.regret_do_genoma(genoma, [1, 2, 3], k=4, t=50))
        self.assertEqual(av.chamadas, 1)
        checksum = registro.pop("sha256")
        canonico = json.dumps(registro, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        self.assertEqual(hashlib.sha256(canonico.encode()).hexdigest(), checksum)

    def test_copias_publicas_nao_alteram_manifesto_ou_historico(self):
        av = AvaliadorSelado(k=3, t=20)
        genoma = genoma_inicial()
        av.nota(genoma, [1])
        genoma["alfa"] = 0.9
        registro = av.registros[0]
        registro["genoma"]["alfa"] = 1
        registro["sementes"].append(2)
        manifesto = av.manifesto
        manifesto["configuracao"]["t"] = 1
        self.assertEqual(av.registros[0]["genoma"]["alfa"], 0.1)
        self.assertEqual(av.registros[0]["sementes"], [1])
        self.assertEqual(av.manifesto["configuracao"]["t"], 20)

    def test_selo_e_estavel_entre_processos(self):
        av = AvaliadorSelado(k=3, t=20)
        programa = "from synthai.revisado.rsi import AvaliadorSelado; print(AvaliadorSelado(k=3,t=20).selo)"
        outro = subprocess.check_output([sys.executable, "-c", programa],
                                       cwd=Path(__file__).resolve().parents[2], text=True).strip()
        self.assertEqual(av.selo, outro)

    def test_configuracoes_distintas_tem_selos_distintos(self):
        self.assertNotEqual(AvaliadorSelado(k=3, t=20).selo, AvaliadorSelado(k=3, t=21).selo)

    def test_entradas_invalidas_nao_publicam_registros(self):
        av = AvaliadorSelado(k=3, t=20)
        casos = [(genoma_inicial(), []), (genoma_inicial(), [True]), (genoma_inicial(), [1.5]),
                 (dict(genoma_inicial(), alfa=0), [1]), (dict(genoma_inicial(), eps=float("nan")), [1]),
                 (dict(genoma_inicial(), q0=True), [1]), ({}, [1]), ([], [1])]
        for g, sementes in casos:
            with self.subTest(g=g, sementes=sementes), self.assertRaises(ValueError):
                av.nota(g, sementes)
        self.assertEqual(av.chamadas, 0)
        self.assertEqual(av.registros, ())

    def test_dimensoes_invalidas_sao_recusadas(self):
        for k, t in ((0, 20), (3, 0), (True, 20), (3, -1), (3.0, 20)):
            with self.subTest(k=k, t=t), self.assertRaises(ValueError):
                AvaliadorSelado(k=k, t=t)

    def test_notas_invalidas_nao_sao_registradas(self):
        for texto in ("nan", "inf", "-1", "21"):
            with self.subTest(valor=texto), patch.object(rsi, "regret_do_genoma", lambda *args, **kwargs: float(texto)):
                av = AvaliadorSelado(k=3, t=20)
                with self.assertRaises(ValueError):
                    av.nota(genoma_inicial(), [1])
                self.assertEqual(av.registros, ())


if __name__ == "__main__":
    unittest.main()
