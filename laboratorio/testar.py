"""Verificações do laboratório; nenhuma contagem de casos é contagem de módulos."""
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import math
import subprocess
import sys
import tempfile
import unittest

from evidencia import EvidenciaBernoulli, OrcamentoErro
from feedback import LedgerFeedback, FalhaInjetada

RAIZ = Path(__file__).resolve().parent


class Estatistica(unittest.TestCase):
    def test_observacao_sem_aposta(self):
        e = EvidenciaBernoulli('1/2', '1/20')
        with self.assertRaises(ValueError): e.observar(1)
        self.assertEqual(e.valor, 1)

    def test_nao_substituir_aposta(self):
        e = EvidenciaBernoulli('1/2', '1/20'); e.apostar(1)
        with self.assertRaises(ValueError): e.apostar(2)
        self.assertEqual(e.observar(0), Fraction(1, 2))

    def test_fator_zero_nao_reanima(self):
        e = EvidenciaBernoulli('1/2', '1/20'); e.apostar(2); e.observar(0)
        e.apostar(2); e.observar(1)
        self.assertEqual(e.valor, 0); self.assertFalse(e.cruzou)

    def test_resultado_invalido_preserva_aposta(self):
        e = EvidenciaBernoulli('1/2', '1/20'); e.apostar(1)
        for x in (2, -1, .5, True):
            with self.assertRaises(ValueError): e.observar(x)
        self.assertEqual(e.observar(1), Fraction(3, 2))

    def test_parametros_e_limites(self):
        for p0, alpha in ((0,.1),(1,.1),(.5,0),(.5,1),(float('nan'),.1),(.5,float('inf'))):
            with self.assertRaises(ValueError): EvidenciaBernoulli(p0, alpha)
        e = EvidenciaBernoulli('1/2','1/20', max_passos=1)
        for bet in (-1,'5/2',float('nan')):
            with self.assertRaises(ValueError): e.apostar(bet)
        e.apostar(0);e.observar(1)
        with self.assertRaises(ValueError):e.apostar(0)

    def test_orcamento_nao_reciclado(self):
        b = OrcamentoErro('1/20');b.alocar('A','1/40');b.alocar('B','1/40')
        with self.assertRaises(ValueError):b.alocar('C','1/1000')
        with self.assertRaises(ValueError):b.alocar('A','1/1000')
        self.assertEqual(sum(b.alocacoes.values()),Fraction(1,20))

    def test_esperanca_exata_sob_nula(self):
        # Aposta previsível muda com o histórico: sem consultar o próximo bit.
        expected = Fraction(0); n=8
        for xs in product((0,1),repeat=n):
            e=EvidenciaBernoulli('1/2','1/10')
            for i,x in enumerate(xs):
                bet=Fraction(1,2) if i and xs[i-1] else Fraction(3,2)
                e.apostar(bet);e.observar(x)
            expected+=e.valor/Fraction(2**n)
        self.assertEqual(expected,1)

    def test_esperanca_abaixo_da_nula(self):
        expected=Fraction(0);n=7
        for xs in product((0,1),repeat=n):
            prob=Fraction(1,4)**sum(xs)*Fraction(3,4)**(n-sum(xs))
            e=EvidenciaBernoulli('1/2','1/10')
            for x in xs:e.apostar(1);e.observar(x)
            expected+=prob*e.valor
        self.assertLessEqual(expected,1)

    def test_parada_adaptativa_enumera_caminhos(self):
        count=0;n=12;alpha=Fraction(1,10)
        for xs in product((0,1),repeat=n):
            e=EvidenciaBernoulli('1/2',alpha)
            for x in xs:
                e.apostar(1);e.observar(x)
                if e.cruzou:count+=1;break
        self.assertLessEqual(Fraction(count,2**n),alpha)
        self.assertGreater(count,0)

    def test_detecta_trajetoria_definida(self):
        e=EvidenciaBernoulli('1/2','1/20')
        for _ in range(8):e.apostar(1);e.observar(1)
        self.assertTrue(e.cruzou);self.assertEqual(e.valor,Fraction(3,2)**8)

    def test_exemplo_invalido_olha_o_futuro(self):
        # Se fosse permitido escolher lambda=2 para X=1 e lambda=0 para X=0,
        # E[f] = (2+1)/2 > 1. A ordem da API não detecta vazamento no gerador.
        self.assertEqual((Fraction(2)+Fraction(1))/2,Fraction(3,2))


class Feedback(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'ledger.db'
        self.ledger=LedgerFeedback(self.path);self.ledger.ativar_modelo('v1')

    def tearDown(self):
        self.ledger.fechar();self.tmp.cleanup()

    def test_aplicacao_e_ack_perdido(self):
        self.ledger.criar_decisao('D','T1')
        self.assertEqual(self.ledger.aplicar('D','T1','v1',7),'aplicado')
        # O retorno pode ser perdido pelo chamador: reabrir e repetir.
        other=LedgerFeedback(self.path)
        try:self.assertEqual(other.aplicar('D','T1','v1',7),'duplicado')
        finally:other.fechar()
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',7,1)])

    def test_conflito_nao_sobrescreve(self):
        self.ledger.criar_decisao('D','T1');self.ledger.repetir_transporte('D','T2')
        self.ledger.aplicar('D','T1','v1',7)
        self.assertEqual(self.ledger.aplicar('D','T2','v1',9),'conflito')
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',7,1)])

    def test_resposta_de_outro_registro(self):
        self.ledger.criar_decisao('D1','T1');self.ledger.criar_decisao('D2','T2')
        self.assertEqual(self.ledger.aplicar('D1','T2','v1',7),'tentativa_desconhecida')
        self.assertEqual(self.ledger.aplicar('D3','T1','v1',7),'decisao_desconhecida')
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',0,0)])

    def test_origem_errada_nao_consume_decisao(self):
        self.ledger.criar_decisao('D','T1')
        self.assertEqual(self.ledger.aplicar('D','T1','v2',7),'origem_incompativel')
        self.assertEqual(self.ledger.aplicar('D','T1','v1',7),'aplicado')

    def test_cancelamento_bloqueia_atrasado(self):
        self.ledger.criar_decisao('D','T1');self.assertTrue(self.ledger.cancelar('D'))
        self.assertFalse(self.ledger.cancelar('D'))
        self.assertEqual(self.ledger.aplicar('D','T1','v1',7),'cancelado')
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',0,0)])

    def test_cancelamento_nao_apaga_aplicacao(self):
        self.ledger.criar_decisao('D','T1');self.ledger.aplicar('D','T1','v1',7)
        self.assertFalse(self.ledger.cancelar('D'))
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',7,1)])

    def test_versao_incompativel(self):
        self.ledger.criar_decisao('D','T1');self.ledger.ativar_modelo('v2')
        self.assertEqual(self.ledger.aplicar('D','T1','v1',7),'incompativel')
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',0,0),('v2',0,0)])

    def test_epoca_impede_aba(self):
        self.ledger.criar_decisao('D','T1');self.ledger.ativar_modelo('v2');self.ledger.ativar_modelo('v1')
        self.assertEqual(self.ledger.aplicar('D','T1','v1',7),'incompativel')

    def test_ativar_mesma_versao_e_noop(self):
        self.ledger.criar_decisao('D','T1');self.ledger.ativar_modelo('v1')
        self.assertEqual(self.ledger.aplicar('D','T1','v1',7),'aplicado')

    def test_falha_no_meio_da_transacao(self):
        self.ledger.criar_decisao('D','T1');before=self.ledger.resumo()
        with self.assertRaises(FalhaInjetada):self.ledger.aplicar('D','T1','v1',7,True)
        self.assertEqual(self.ledger.resumo(),before)
        self.assertEqual(self.ledger.aplicar('D','T1','v1',7),'aplicado')

    def test_encerramento_processo_antes_do_commit(self):
        self.ledger.criar_decisao('D','T1')
        code="""import sqlite3,os,sys
c=sqlite3.connect(sys.argv[1],isolation_level=None)
c.execute('BEGIN IMMEDIATE')
c.execute("UPDATE modelos SET total=7, atualizacoes=1 WHERE versao='v1'")
os._exit(23)
"""
        r=subprocess.run([sys.executable,'-c',code,str(self.path)])
        self.assertEqual(r.returncode,23)
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',0,0)])
        self.assertEqual(self.ledger.aplicar('D','T1','v1',7),'aplicado')

    def test_concorrencia_mesma_decisao(self):
        self.ledger.criar_decisao('D','T1')
        def apply(_):
            l=LedgerFeedback(self.path)
            try:return l.aplicar('D','T1','v1',7)
            finally:l.fechar()
        with ThreadPoolExecutor(max_workers=8) as pool:rs=list(pool.map(apply,range(32)))
        self.assertEqual(rs.count('aplicado'),1);self.assertEqual(rs.count('duplicado'),31)
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',7,1)])
        self.assertEqual(self.ledger.resumo()['recibos'],32)

    def test_concorrencia_decisoes_distintas(self):
        for i in range(16):self.ledger.criar_decisao(f'D{i}',f'T{i}')
        def apply(i):
            l=LedgerFeedback(self.path)
            try:return l.aplicar(f'D{i}',f'T{i}','v1',i)
            finally:l.fechar()
        with ThreadPoolExecutor(max_workers=8) as pool:rs=list(pool.map(apply,range(16)))
        self.assertEqual(rs.count('aplicado'),16)
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',sum(range(16)),16)])

    def test_cancelamento_concorrente(self):
        self.ledger.criar_decisao('D','T1')
        def run(cancel):
            l=LedgerFeedback(self.path)
            try:return l.cancelar('D') if cancel else l.aplicar('D','T1','v1',7)
            finally:l.fechar()
        with ThreadPoolExecutor(max_workers=2) as p:rs=list(p.map(run,[True,False]))
        r=self.ledger.resumo();state=r['decisoes'][0][2]
        self.assertIn(state,('cancelado','aplicado'))
        self.assertEqual(r['modelos'][0][1:],(0,0) if state=='cancelado' else (7,1))

    def test_dominio_recompensa(self):
        self.ledger.criar_decisao('D','T1')
        for x in (True,math.nan,7.0,1_000_001):
            with self.assertRaises(ValueError):self.ledger.aplicar('D','T1','v1',x)
        self.assertEqual(self.ledger.resumo()['recibos'],0)

    def test_auditoria_le_snapshot_coerente(self):
        self.ledger.criar_decisao('D','T1');other=LedgerFeedback(self.path)
        triggered=[]
        def entre_consultas(sql):
            if sql.startswith('SELECT id,versao,estado') and not triggered:
                triggered.append(True);other.aplicar('D','T1','v1',7)
        self.ledger.db.set_trace_callback(entre_consultas)
        try:before=self.ledger.resumo()
        finally:self.ledger.db.set_trace_callback(None);other.fechar()
        self.assertEqual(before['modelos'],[('v1',0,0)])
        self.assertEqual(before['decisoes'],[('D','v1','pendente',None)])
        self.assertEqual(before['recibos'],0)
        self.assertEqual(self.ledger.resumo()['modelos'],[('v1',7,1)])


if __name__ == '__main__':
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    (RAIZ/'resultado_testes.json').write_text(json.dumps(dict(testes=result.testsRun,
        falhas=len(result.failures),erros=len(result.errors),sucesso=result.wasSuccessful(),
        escopo='duas implementações de laboratório; não certificação dos cem módulos nem do SYNTHAI'),ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
