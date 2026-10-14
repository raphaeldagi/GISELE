"""Ledger SQLite: uma atualização local por decisão lógica, com versões e auditoria."""
from contextlib import contextmanager
import sqlite3


class FalhaInjetada(RuntimeError):
    pass


class LedgerFeedback:
    def __init__(self, caminho):
        self.db = sqlite3.connect(str(caminho), timeout=10, isolation_level=None)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS modelos (
          versao TEXT PRIMARY KEY, total INTEGER NOT NULL DEFAULT 0,
          atualizacoes INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS meta (chave TEXT PRIMARY KEY, valor TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS decisoes (
          id TEXT PRIMARY KEY, versao TEXT NOT NULL REFERENCES modelos(versao),
          epoca INTEGER NOT NULL,
          estado TEXT NOT NULL CHECK(estado IN ('pendente','aplicado','cancelado','incompativel')),
          recompensa INTEGER);
        CREATE TABLE IF NOT EXISTS tentativas (
          decisao TEXT NOT NULL REFERENCES decisoes(id), id TEXT NOT NULL,
          PRIMARY KEY(decisao,id));
        CREATE TABLE IF NOT EXISTS recibos (
          seq INTEGER PRIMARY KEY, decisao TEXT NOT NULL, tentativa TEXT NOT NULL,
          origem TEXT NOT NULL, recompensa INTEGER NOT NULL, resultado TEXT NOT NULL);
        """)

    @staticmethod
    def _id(valor):
        if not isinstance(valor, str) or not valor.strip() or len(valor) > 200:
            raise ValueError("Identificador textual não vazio de até 200 caracteres obrigatório.")

    @contextmanager
    def _transacao(self, imediata=True):
        self.db.execute("BEGIN IMMEDIATE" if imediata else "BEGIN")
        try:
            yield
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def fechar(self):
        self.db.close()

    def ativar_modelo(self, versao):
        self._id(versao)
        with self._transacao():
            anterior = self.db.execute("SELECT valor FROM meta WHERE chave='atual'").fetchone()
            if anterior and anterior[0] == versao:
                return
            epoca = self.db.execute("SELECT valor FROM meta WHERE chave='epoca'").fetchone()
            proxima = int(epoca[0]) + 1 if epoca else 1
            self.db.execute("INSERT OR IGNORE INTO modelos(versao) VALUES (?)", (versao,))
            self.db.execute("INSERT INTO meta VALUES ('atual',?) ON CONFLICT(chave) DO UPDATE SET valor=excluded.valor", (versao,))
            self.db.execute("INSERT INTO meta VALUES ('epoca',?) ON CONFLICT(chave) DO UPDATE SET valor=excluded.valor", (str(proxima),))

    def criar_decisao(self, decisao, tentativa):
        self._id(decisao); self._id(tentativa)
        with self._transacao():
            atual = self.db.execute("SELECT valor FROM meta WHERE chave='atual'").fetchone()
            if not atual:
                raise ValueError("Ative um modelo antes de criar decisões.")
            epoca = int(self.db.execute("SELECT valor FROM meta WHERE chave='epoca'").fetchone()[0])
            self.db.execute("INSERT INTO decisoes(id,versao,epoca,estado) VALUES (?,?,?,'pendente')", (decisao, atual[0], epoca))
            self.db.execute("INSERT INTO tentativas VALUES (?,?)", (decisao, tentativa))

    def repetir_transporte(self, decisao, tentativa):
        self._id(decisao); self._id(tentativa)
        with self._transacao():
            estado = self.db.execute("SELECT estado FROM decisoes WHERE id=?", (decisao,)).fetchone()
            if not estado or estado[0] != 'pendente':
                raise ValueError("Apenas decisões pendentes admitem uma nova tentativa de transporte.")
            self.db.execute("INSERT INTO tentativas VALUES (?,?)", (decisao, tentativa))

    def cancelar(self, decisao):
        self._id(decisao)
        with self._transacao():
            mudou = self.db.execute("UPDATE decisoes SET estado='cancelado' WHERE id=? AND estado='pendente'", (decisao,)).rowcount
            return bool(mudou)

    def aplicar(self, decisao, tentativa, origem, recompensa, falhar_apos_atualizacao=False):
        for identificador in (decisao, tentativa, origem):
            self._id(identificador)
        if type(recompensa) is not int or abs(recompensa) > 1_000_000:
            raise ValueError("Recompensa inteira de magnitude limitada obrigatória.")
        with self._transacao():
            registro = self.db.execute("SELECT versao,estado,recompensa,epoca FROM decisoes WHERE id=?", (decisao,)).fetchone()
            tentativa_valida = self.db.execute("SELECT 1 FROM tentativas WHERE decisao=? AND id=?", (decisao, tentativa)).fetchone()
            if not registro:
                resultado = 'decisao_desconhecida'
            elif not tentativa_valida:
                resultado = 'tentativa_desconhecida'
            elif origem != registro[0]:
                resultado = 'origem_incompativel'
            elif registro[1] == 'aplicado':
                resultado = 'duplicado' if recompensa == registro[2] else 'conflito'
            elif registro[1] != 'pendente':
                resultado = registro[1]
            else:
                atual = self.db.execute("SELECT valor FROM meta WHERE chave='atual'").fetchone()[0]
                epoca = int(self.db.execute("SELECT valor FROM meta WHERE chave='epoca'").fetchone()[0])
                if atual != registro[0] or epoca != registro[3]:
                    self.db.execute("UPDATE decisoes SET estado='incompativel' WHERE id=?", (decisao,))
                    resultado = 'incompativel'
                else:
                    total = self.db.execute("SELECT total FROM modelos WHERE versao=?", (atual,)).fetchone()[0]
                    if abs(total + recompensa) > 2**62:
                        raise OverflowError("Acumulador fora do domínio inteiro contratado.")
                    self.db.execute("UPDATE modelos SET total=total+?, atualizacoes=atualizacoes+1 WHERE versao=?", (recompensa, atual))
                    if falhar_apos_atualizacao:
                        raise FalhaInjetada("Falha antes de registrar a aplicação e confirmar a transação.")
                    self.db.execute("UPDATE decisoes SET estado='aplicado', recompensa=? WHERE id=? AND estado='pendente'", (recompensa, decisao))
                    resultado = 'aplicado'
            self.db.execute("INSERT INTO recibos(decisao,tentativa,origem,recompensa,resultado) VALUES (?,?,?,?,?)", (decisao, tentativa, origem, recompensa, resultado))
            return resultado

    def resumo(self):
        with self._transacao(imediata=False):
            return dict(modelos=self.db.execute("SELECT versao,total,atualizacoes FROM modelos ORDER BY versao").fetchall(),
                        decisoes=self.db.execute("SELECT id,versao,estado,recompensa FROM decisoes ORDER BY id").fetchall(),
                        recibos=self.db.execute("SELECT COUNT(*) FROM recibos").fetchone()[0])
