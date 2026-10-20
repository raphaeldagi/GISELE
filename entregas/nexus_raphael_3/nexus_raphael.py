#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NEXUS–RAPHAEL 3.0.0: laboratório experimental auditável, offline, só biblioteca padrão.

Execução: python3 nexus_raphael.py teste
          python3 nexus_raphael.py experimento --modo rapido
          python3 nexus_raphael.py kuhn | leduc | velha | sat | calibracao | bandidos | megasena3 | caos
          python3 nexus_raphael.py ciclo --texto "logic and learning"
          python3 nexus_raphael.py estado

O que mudou desde a 2.2.0 (cada item tem teste em TestesExtensao):
  CORRIGIDO
  - Rede removida: não há urllib nem consulta HTTP; permitir_rede=True levanta erro.
  - IC do bootstrap pelos quantis da contagem real de réplicas (os índices fixos [24]/[974]
    quebravam com 500 réplicas e erravam o percentil com 2000).
  - Qui-quadrado da Mega-Sena com o fator 54/59 (6 dezenas distintas por sorteio) e com p-valor.
  - Intervalo da Beta pelos quantis exatos (a aproximação ±1,96σ sai de [0, 1] em amostra pequena).
  - H-M3 com veredito combinado além do por seed; H-M7 com arrependimento pelas médias
    verdadeiras em muitas sementes (cinco sementes e 200 passos de avaliação não decidem nada).
  ACRESCENTADO (funcionalidade real, com teste)
  - Estatística: gama e beta incompletas, χ², t, normal, Wilson, Clopper-Pearson, t pareado,
    binomial exato, sinal, permutação, Holm.
  - Álgebra linear sem numpy: LU com pivô, determinante, inversa, mínimos quadrados (cumeeira),
    Gram-Schmidt, Jacobi, valores singulares, potência, PCA.
  - Calibração (isotônica PAV e Platt), bandidos (ε-guloso, UCB1, Thompson, cota de Lai-Robbins),
    informação (entropia, KL, informação mútua, Levenshtein), modelo de caracteres Witten-Bell,
    dinâmica (RK4, Lorenz, Lyapunov de Benettin, períodos e dobras do mapa logístico).
  - Jogos: pôquer de Kuhn e Leduc, CFR vanilla, com acaso amostrado e com amostragem externa,
    melhor resposta exata e explorabilidade, simplex exato em frações (Kuhn = −1/18 pela forma
    normal 64×64), jogo da velha com alfa-beta e Q-learning.
  - Lógica: Tseitin + DPLL (sem o teto de 16 variáveis), casa dos pombos, transição do 3-SAT.
  - Codificação: base 26 bijetiva, Hamming (7,4), CRC-32, Huffman, LZ78.

Comentários e textos em português. Dados offline são léxico manual de teste, não fonte primária.
Esta implementação NÃO constitui AGI, ASI, AFI ou evidência de consciência.
"""
from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import random
import re
import sqlite3
import statistics
import sys
import time
from functools import lru_cache
from typing import Any, Protocol
import unittest

VERSAO = "3.0.0"
ROTULOS = frozenset({"[MEDIDO]", "[DERIVADO]", "[HIPÓTESE]", "[SINTÉTICO]",
                     "[NÃO EXECUTADO]", "[ANALOGIA]", "[FICÇÃO EXPERIMENTAL]",
                     "[ESPECULAÇÃO FILOSÓFICA]", "[REJEITADO]"})
AGORA = lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
FONTES_DOCUMENTADAS = {
    "free_dictionary": "https://api.dictionaryapi.dev/api/v2/entries/en/",
    "referencia": "https://github.com/meetDeveloper/freeDictionaryAPI",
    "wordnet_licenca": "https://wordnet.princeton.edu/license-and-commercial-use",
    "wikimedia_documentacao": "https://www.mediawiki.org/wiki/Wikimedia_REST_API",
}


def serie_json(obj: Any) -> str:
    """Serializa números e estruturas simples para trilha de auditoria."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str, allow_nan=False)


def validar_rotulo(rotulo: str) -> str:
    if rotulo not in ROTULOS:
        raise ValueError("Rótulo epistêmico desconhecido")
    return rotulo


@dataclass(frozen=True)
class Configuracao:
    seed: int = 42
    seeds_comparacao: tuple[int, ...] = (0, 1, 2, 3, 4)
    profundidade_maxima: int = 3
    rodadas_debate: int = 4
    rodadas_criativas: int = 5
    max_passos: int = 100_000
    limite_segundos: float = 60.0
    bootstrap: int = 1_000
    faixas_calibracao: int = 10
    tolerancia: float = 1e-9
    permitir_rede: bool = False
    raiz: str = "nexus_raphael"

    def __post_init__(self) -> None:
        if self.profundidade_maxima > 3 or self.profundidade_maxima < 0:
            raise ValueError("Limite seguro de recursão: 0 a 3")
        if not 1 <= self.max_passos <= 1_000_000:
            raise ValueError("Orçamento de passos inválido")
        if self.limite_segundos <= 0:
            raise ValueError("Orçamento temporal inválido")


class Orcamento:
    """Limita recursos por tempo, passos e profundidade."""
    def __init__(self, cfg: Configuracao):
        self.cfg = cfg
        self.inicio = time.monotonic()
        self.passos = 0

    def consumir(self, quantidade: int = 1, profundidade: int = 0) -> None:
        self.passos += quantidade
        if (profundidade > self.cfg.profundidade_maxima or
                self.passos > self.cfg.max_passos or
                time.monotonic() - self.inicio > self.cfg.limite_segundos):
            raise TimeoutError("Orçamento de processamento ultrapassado")


class Repositorio:
    """Diretório de projeto restrito; dados persistidos em SQLite e JSONL."""
    def __init__(self, cfg: Configuracao):
        self.raiz = Path(cfg.raiz).expanduser().resolve()
        self.raiz.mkdir(parents=True, exist_ok=True)
        self.execucoes = self.caminho("execucoes")
        self.execucoes.mkdir(exist_ok=True)
        self.banco = self.caminho("nexus.sqlite3")
        self.criar_esquema()

    def caminho(self, relativo: str) -> Path:
        caminho = (self.raiz / relativo).resolve()
        if caminho != self.raiz and self.raiz not in caminho.parents:
            raise ValueError("Tentativa de acessar caminho fora do projeto")
        return caminho

    def conexao(self) -> sqlite3.Connection:
        conexao = sqlite3.connect(self.banco, timeout=5)
        conexao.execute("PRAGMA foreign_keys=ON")
        return conexao

    def criar_esquema(self) -> None:
        with self.conexao() as con:
            con.executescript("""
            CREATE TABLE IF NOT EXISTS fonte (
                id INTEGER PRIMARY KEY, nome TEXT UNIQUE NOT NULL,
                licenca TEXT NOT NULL, url TEXT, obtido_em TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS palavra (
                id INTEGER PRIMARY KEY, forma TEXT NOT NULL,
                lema TEXT NOT NULL, idioma TEXT NOT NULL,
                frequencia REAL, UNIQUE(forma, idioma));
            CREATE TABLE IF NOT EXISTS sentido (
                id INTEGER PRIMARY KEY, palavra_id INTEGER NOT NULL,
                classe TEXT NOT NULL, definicao TEXT NOT NULL,
                exemplo TEXT, fonte_id INTEGER NOT NULL, confianca REAL NOT NULL,
                FOREIGN KEY(palavra_id) REFERENCES palavra(id),
                FOREIGN KEY(fonte_id) REFERENCES fonte(id));
            CREATE TABLE IF NOT EXISTS relacao (
                origem INTEGER, destino INTEGER, tipo TEXT, fonte_id INTEGER,
                UNIQUE(origem, destino, tipo, fonte_id));
            CREATE TABLE IF NOT EXISTS divergencia (
                palavra_id INTEGER, campo TEXT, fonte_a INTEGER,
                fonte_b INTEGER, nota TEXT);
            CREATE TABLE IF NOT EXISTS cache_http (
                chave TEXT PRIMARY KEY, resposta TEXT,
                obtido_em TEXT, validade_s INTEGER);
            CREATE TABLE IF NOT EXISTS registro (
                id INTEGER PRIMARY KEY, tipo TEXT NOT NULL,
                chave TEXT NOT NULL, valor TEXT NOT NULL,
                rotulo TEXT NOT NULL, fonte TEXT NOT NULL,
                criado_em TEXT NOT NULL, expira_em TEXT);
            CREATE TABLE IF NOT EXISTS versao (
                id INTEGER PRIMARY KEY, numero TEXT, motivo TEXT,
                resultado TEXT, criado_em TEXT);
            """)

    def evento(self, categoria: str, dados: dict[str, Any], rotulo: str = "[MEDIDO]") -> None:
        validar_rotulo(rotulo)
        evento = dict(data=AGORA(), categoria=categoria, versao=VERSAO,
                      rotulo=rotulo, dados=dados)
        with self.caminho("execucoes/eventos.jsonl").open("a", encoding="utf-8") as arq:
            arq.write(serie_json(evento) + "\n")

    def salvar_json(self, nome: str, dados: Any) -> Path:
        if "/" in nome or "\\" in nome or not nome.endswith(".json"):
            raise ValueError("Nome de relatório inválido")
        destino = self.caminho("execucoes/" + nome)
        temporario = destino.with_suffix(".tmp")
        temporario.write_text(serie_json(dados) + "\n", encoding="utf-8")
        temporario.replace(destino)
        return destino

    def memorizar(self, tipo: str, chave: str, valor: Any, rotulo: str,
                  fonte: str = "sistema", expira_em: str | None = None) -> None:
        validar_rotulo(rotulo)
        with self.conexao() as con:
            con.execute("INSERT INTO registro(tipo,chave,valor,rotulo,fonte,criado_em,expira_em) "
                        "VALUES (?,?,?,?,?,?,?)",
                        (tipo, chave, serie_json(valor), rotulo, fonte, AGORA(), expira_em))

    def consultar(self, tipo: str, chave: str) -> list[dict[str, Any]]:
        with self.conexao() as con:
            linhas = con.execute("SELECT valor,rotulo,fonte,criado_em FROM registro "
                                 "WHERE tipo=? AND chave=? AND (expira_em IS NULL OR expira_em>?) "
                                 "ORDER BY id DESC", (tipo, chave, AGORA())).fetchall()
        return [dict(valor=json.loads(v), rotulo=r, fonte=f, criado_em=t)
                for v, r, f, t in linhas]


# Mini-léxico manual, explicitamente não autoritativo: palavra|classe|definição.
# Direitos sobre o texto das definições: redação original deste arquivo (CC0).
_LEXICO_TEXTO = """
ability|noun|capacity to do something
abstract|adjective|not concrete or physical
accuracy|noun|closeness to the correct value
action|noun|something that is done
adapt|verb|to change in response to conditions
agent|noun|a person or system that acts
algorithm|noun|a finite procedure for a task
analysis|noun|careful examination of components
angle|noun|the space between intersecting lines
answer|noun|a response to a question
argument|noun|a reason offered in support of a claim
array|noun|an ordered collection of elements
artificial|adjective|made through human design
assumption|noun|a proposition accepted provisionally
attention|noun|selective focus on information
attribute|noun|a property of something
audit|verb|to examine records systematically
average|noun|a value representing a set
axiom|noun|a proposition taken as a starting rule
balance|noun|a condition of equilibrium
base|noun|a foundation or starting reference
behavior|noun|a pattern of actions
belief|noun|acceptance of a proposition
bias|noun|a systematic tendency or distortion
binary|adjective|using two distinct states
bootstrap|noun|a method of resampling observations
boundary|noun|a defined limit
budget|noun|resources available for a task
calibration|noun|agreement between predicted rates and observations
cause|noun|something that brings about an effect
change|verb|to become different
chance|noun|the possibility of an event
character|noun|a written symbol
choice|noun|an act of selecting among alternatives
class|noun|a group with common properties
code|noun|instructions or a system of symbols
coherent|adjective|logically consistent
compare|verb|to examine similarities and differences
complex|adjective|composed of many interacting parts
concept|noun|an abstract idea
condition|noun|a circumstance affecting an outcome
confidence|noun|degree of certainty assigned to a claim
conflict|noun|incompatibility between claims
constant|noun|a quantity with fixed value
context|noun|circumstances surrounding an event
control|noun|a reference used for comparison
correct|adjective|free from a particular error
correlation|noun|statistical association between variables
cost|noun|resources spent on an action
counterexample|noun|an instance disproving a universal claim
creative|adjective|producing original combinations
critical|adjective|carefully evaluating claims
data|noun|recorded observations or symbols
decision|noun|selection of an action
decode|verb|to recover information from an encoding
definition|noun|a statement of meaning
delta|noun|a difference or change
dependence|noun|a relationship of reliance
design|noun|a plan for a structure
detect|verb|to discover an identifiable property
dictionary|noun|a reference collection of words
difference|noun|a result of subtraction or contrast
distance|noun|a measure of separation
distribution|noun|a description of possible values and their frequencies
diverse|adjective|having varied forms
domain|noun|a defined field or set
double|adjective|twice a quantity
dynamic|adjective|changing over time
effect|noun|a consequence of a cause
efficient|adjective|achieving a goal with low resource cost
element|noun|one member of a set
encode|verb|to represent information with symbols
entropy|noun|a measure of uncertainty in a distribution
episode|noun|one complete sequence of events
equation|noun|a statement of equality
equilibrium|noun|a state with no net change
error|noun|difference from a true or expected result
evidence|noun|observations supporting or opposing a claim
evolution|noun|change across successive states
example|noun|an instance illustrating a rule
experiment|noun|a controlled procedure for testing a claim
explain|verb|to give reasons or causes
feature|noun|a measurable property used by a model
feedback|noun|information returned about a result
finite|adjective|having a limit
function|noun|a mapping from inputs to outputs
game|noun|a structured activity with rules
general|adjective|applying to many cases
generate|verb|to produce an output
global|adjective|pertaining to the whole
gradient|noun|a vector of partial derivatives
graph|noun|a set of nodes connected by edges
group|noun|a collection of related items
hash|noun|a compact digest of data
hidden|adjective|not directly observable
history|noun|a record of previous events
honest|adjective|truthfully representing what is known
hypothesis|noun|a claim that can be evaluated
identity|noun|a distinguishing property
independent|adjective|not dependent on a specified factor
index|noun|a position or reference key
inference|noun|drawing conclusions from evidence
information|noun|data that reduces uncertainty
input|noun|data supplied to a procedure
inspect|verb|to examine carefully
integer|noun|a whole number
interpret|verb|to assign meaning to information
interval|noun|a continuous range of values
inverse|adjective|reversing a transformation
iteration|noun|one repetition of a procedure
judge|noun|an evaluator of outcomes
label|noun|a tag describing a category
language|noun|a structured system of communication
layer|noun|a stage in a processing system
learn|verb|to improve performance using examples
length|noun|the extent of a sequence
lexical|adjective|relating to words
limit|noun|a bound beyond which a process cannot go
linear|adjective|following a proportional relationship
logic|noun|the study of valid reasoning
loss|noun|a numerical measure of prediction error
machine|noun|a device or system that performs work
mapping|noun|an association between sets
matrix|noun|a rectangular array of values
meaning|noun|the significance of a symbol
measure|verb|to determine a quantity
memory|noun|stored information that may be retrieved
method|noun|a reproducible way of proceeding
metric|noun|a defined numerical measure
model|noun|a simplified representation of a system
module|noun|a component with a defined interface
monitor|verb|to observe behavior over time
mutation|noun|a change to a stored state
negative|adjective|less than zero or expressing denial
network|noun|a set of connected entities
node|noun|an element in a graph
noise|noun|unwanted or random variation
nonlinear|adjective|not adequately described by a linear relation
norm|noun|a quantity measuring vector magnitude
novel|adjective|new relative to a reference
number|noun|a mathematical quantity
object|noun|an entity represented by data
observe|verb|to collect information about a state
option|noun|an available alternative
optimal|adjective|best according to a chosen criterion
order|noun|a particular arrangement
output|noun|a result generated by a procedure
parameter|noun|a variable controlling a model
pattern|noun|a recurring arrangement
performance|noun|measured success on a task
policy|noun|a rule for selecting actions
position|noun|a location in a sequence or space
positive|adjective|greater than zero or expressing affirmation
possible|adjective|capable of occurring
predict|verb|to estimate an unknown result
precision|noun|closeness among repeated measurements
probability|noun|a measure of likelihood
process|noun|a sequence of operations
program|noun|instructions executed by a computer
projection|noun|a component along a defined direction
proof|noun|a valid logical demonstration
quality|noun|degree of meeting specified standards
question|noun|a request for information
random|adjective|selected according to chance
rate|noun|a ratio measured over a reference
reason|noun|a justification or cause
record|noun|a stored account of events
recover|verb|to regain information
recursive|adjective|using a procedure within itself
reference|noun|a known comparison point
regression|noun|a model for estimating relationships
reinforcement|noun|feedback used to improve action policies
reject|verb|to decline to accept a proposal
relation|noun|a connection between entities
reliable|adjective|producing consistent dependable results
report|noun|a structured account of findings
reproduce|verb|to obtain results under stated procedures
research|noun|systematic investigation
reward|noun|feedback assigning value to an action
risk|noun|possibility of an adverse outcome
robust|adjective|stable under variation
rotation|noun|movement around an axis
rule|noun|an explicit constraint or instruction
sample|noun|a subset drawn from a population
scale|noun|a range used for measurement
score|noun|a numerical evaluation
search|verb|to look for information or a solution
security|noun|protection against undesirable access or change
seed|noun|a starting value for a pseudorandom generator
semantic|adjective|relating to meaning
sequence|noun|an ordered series of items
signal|noun|information distinguished from noise
simulate|verb|to imitate a process with a model
solution|noun|an answer satisfying a problem
source|noun|the origin of information
space|noun|a set equipped with specified structure
sparse|adjective|containing many zero entries
state|noun|a description of a system at a time
statistic|noun|a quantity computed from data
strategy|noun|a plan for choosing actions
structure|noun|a defined arrangement of components
symbol|noun|a sign representing something
system|noun|a set of interacting parts
task|noun|a defined piece of work
test|noun|a procedure to check a property
theory|noun|an explanatory framework
threshold|noun|a cutoff determining a decision
time|noun|a measure of duration or ordering
token|noun|a unit in a text sequence
tool|noun|a device or software function used for a task
trace|noun|a record of execution steps
train|verb|to adjust a model using examples
transform|verb|to change representation
truth|noun|the property of agreeing with what is the case
uncertain|adjective|not known with certainty
unicode|noun|a standard for character encoding
uniform|adjective|having equal values or likelihoods
update|verb|to replace or amend stored values
useful|adjective|having practical benefit
validate|verb|to assess against specified criteria
value|noun|a numerical or symbolic quantity
variable|noun|a symbol whose value can change
vector|noun|an ordered collection of components
verify|verb|to check against independent criteria
version|noun|a distinct revision of a system
word|noun|a unit of language
workflow|noun|a sequence of connected operations
"""


def lexico_embutido() -> list[tuple[str, str, str]]:
    linhas = [linha.split("|", 2) for linha in _LEXICO_TEXTO.strip().splitlines()]
    if any(len(linha) != 3 for linha in linhas):
        raise ValueError("Mini-léxico malformado")
    return [(p, c, d) for p, c, d in linhas]


class LagoLexical:
    """Data lake local com fonte e licença. Desde a 3.0.0, sem rede: só o léxico embutido."""
    def __init__(self, repo: Repositorio, permitir_rede: bool = False):
        if permitir_rede:
            raise ValueError("A 3.0.0 é offline: não há consulta de rede")
        self.repo = repo
        self.permitir_rede = permitir_rede
        self.ultima_consulta = 0.0

    def instalar_offline(self) -> int:
        with self.repo.conexao() as con:
            con.execute("INSERT OR IGNORE INTO fonte(nome,licenca,url,obtido_em) VALUES (?,?,?,?)",
                        ("mini_lexico_manual", "CC0 - redação original de teste",
                         "arquivo:nexus_raphael.py", AGORA()))
            id_fonte = con.execute("SELECT id FROM fonte WHERE nome=?",
                                   ("mini_lexico_manual",)).fetchone()[0]
            for palavra, classe, definicao in lexico_embutido():
                con.execute("INSERT OR IGNORE INTO palavra(forma,lema,idioma) "
                            "VALUES (?,?,?)", (palavra, palavra, "en"))
                id_palavra = con.execute("SELECT id FROM palavra WHERE forma=? AND idioma='en'",
                                         (palavra,)).fetchone()[0]
                existe = con.execute("SELECT 1 FROM sentido WHERE palavra_id=? AND fonte_id=?",
                                      (id_palavra, id_fonte)).fetchone()
                if not existe:
                    con.execute("INSERT INTO sentido(palavra_id,classe,definicao,fonte_id,confianca) "
                                "VALUES (?,?,?,?,?)", (id_palavra, classe, definicao,
                                                        id_fonte, 0.5))
        return len(lexico_embutido())

    def procurar(self, palavra: str) -> list[dict[str, Any]]:
        if not re.fullmatch(r"[a-zA-Z-]{1,60}", palavra):
            raise ValueError("Consulta lexical inválida")
        with self.repo.conexao() as con:
            linhas = con.execute("""SELECT p.forma,s.classe,s.definicao,s.exemplo,
                                       f.nome,f.licenca,f.obtido_em,s.confianca
                                   FROM palavra p JOIN sentido s ON s.palavra_id=p.id
                                   JOIN fonte f ON f.id=s.fonte_id
                                   WHERE p.forma=? AND p.idioma='en'""",
                                (palavra.lower(),)).fetchall()
        if linhas:
            return [dict(palavra=p, classe=c, definicao=d, exemplo=e, fonte=f,
                         licenca=l, obtido_em=t, confianca=conf)
                    for p, c, d, e, f, l, t, conf in linhas]
        return []


class Codificador:
    """Representações exatas, sem atribuir significado a bytes ou hashes."""
    @staticmethod
    def codificar(texto: str) -> dict[str, Any]:
        dados = texto.encode("utf-8")
        return dict(unicode=[ord(c) for c in texto], utf8=list(dados),
                    hexadecimal=dados.hex(), binario="".join(f"{n:08b}" for n in dados),
                    sha256=hashlib.sha256(dados).hexdigest(), reversivel=True)

    @staticmethod
    def decodificar_hex(hexadecimal: str) -> str:
        return bytes.fromhex(hexadecimal).decode("utf-8", errors="strict")

    @staticmethod
    def decodificar_bin(binario: str) -> str:
        if len(binario) % 8 or any(c not in "01" for c in binario):
            raise ValueError("Código binário malformado")
        return bytes(int(binario[n:n+8], 2) for n in range(0, len(binario), 8)).decode("utf-8")

    @staticmethod
    def numerologia(texto: str) -> int:
        return sum(ord(c) - 64 for c in texto.upper() if "A" <= c <= "Z")


_CONSOANTES = "bcdfghjklmnprs"  # 14 consoantes
_VOGAIS = "aeiou"
_SILABAS = [c + v for c in _CONSOANTES for v in _VOGAIS]
assert len(_SILABAS) == 70


class LinguaArtificial:
    """Números inteiros não negativos em base bijetiva de 70 sílabas."""
    @staticmethod
    def codificar(numero: int) -> str:
        if not isinstance(numero, int) or numero < 0:
            raise ValueError("Esperado inteiro não negativo")
        numero += 1
        resultado = []
        while numero:
            numero, resto = divmod(numero - 1, 70)
            resultado.append(_SILABAS[resto])
        return "".join(reversed(resultado))

    @staticmethod
    def decodificar(palavra: str) -> int:
        if len(palavra) < 2 or len(palavra) % 2:
            raise ValueError("Palavra artificial inválida")
        numero = 0
        for pos in range(0, len(palavra), 2):
            silaba = palavra[pos:pos+2]
            if silaba not in _SILABAS:
                raise ValueError("Sílaba não pertence à língua")
            numero = numero * 70 + _SILABAS.index(silaba) + 1
        return numero - 1


class Geometria:
    @staticmethod
    def produto(a: list[float], b: list[float]) -> float:
        if len(a) != len(b):
            raise ValueError("Dimensões diferentes")
        return sum(x*y for x, y in zip(a, b))

    @staticmethod
    def norma(a: list[float]) -> float:
        return math.sqrt(Geometria.produto(a, a))

    @staticmethod
    def cosseno(a: list[float], b: list[float]) -> float:
        divisor = Geometria.norma(a) * Geometria.norma(b)
        return Geometria.produto(a, b)/divisor if divisor else 0.0

    @staticmethod
    def distancia(a: list[float], b: list[float]) -> float:
        return Geometria.norma([x-y for x, y in zip(a, b)]) if len(a) == len(b) else math.nan

    @staticmethod
    def projecao(a: list[float], b: list[float]) -> list[float]:
        divisor = Geometria.produto(b, b)
        if divisor == 0:
            raise ValueError("Projeção sobre vetor nulo")
        escala = Geometria.produto(a, b)/divisor
        return [escala*x for x in b]

    @staticmethod
    def rotacionar2(v: list[float], angulo: float) -> list[float]:
        if len(v) != 2:
            raise ValueError("Rotação 2D requer dois componentes")
        x, y = v
        return [x*math.cos(angulo)-y*math.sin(angulo),
                x*math.sin(angulo)+y*math.cos(angulo)]

    @staticmethod
    def erro_angulo_duplo(quantidade: int = 10_000, seed: int = 42) -> float:
        rng = random.Random(seed)
        return max(abs(math.cos(2*(t := rng.uniform(-math.pi, math.pi))) -
                       (2*math.cos(t)**2 - 1)) for _ in range(quantidade))

    @staticmethod
    def lyapunov_logistico(r: float, n: int = 20_000, descarte: int = 2_000) -> float:
        """Expoente do mapa x[t+1]=r*x[t]*(1-x[t]), não de uma mente."""
        x = 0.123456789
        valores = []
        for i in range(n + descarte):
            x = r*x*(1-x)
            if i >= descarte:
                valores.append(math.log(max(1e-300, abs(r*(1-2*x)))))
        return statistics.fmean(valores)


class BetaBernoulli:
    """Distribuição posterior sobre taxa de sucesso, com priori Beta(1,1)."""
    def __init__(self, a: float = 1.0, b: float = 1.0):
        if a <= 0 or b <= 0:
            raise ValueError("Parâmetros Beta positivos são obrigatórios")
        self.a, self.b = a, b

    def observar(self, acerto: int) -> None:
        if acerto not in (0, 1):
            raise ValueError("Observação deve ser zero ou um")
        self.a += acerto
        self.b += 1 - acerto

    def prever(self) -> float:
        return self.a / (self.a + self.b)

    def variancia_parametro(self) -> float:
        n = self.a + self.b
        return self.a * self.b / (n*n*(n+1))

    def intervalo_exato(self, nivel: float = .95) -> tuple[float, float]:
        return Estatistica.beta_credivel(self.a, self.b, nivel)

    def intervalo_aproximado(self) -> tuple[float, float]:
        media = self.prever()
        desvio = math.sqrt(self.variancia_parametro())
        return max(0.0, media-1.96*desvio), min(1.0, media+1.96*desvio)


class Decisor:
    """Escolhe ação binária pela menor perda esperada."""
    @staticmethod
    def escolher(probabilidade: float, custo_falso_positivo: float = 1.,
                custo_falso_negativo: float = 1.) -> int:
        if not 0 <= probabilidade <= 1 or min(custo_falso_positivo,
                                               custo_falso_negativo) < 0:
            raise ValueError("Probabilidade/custos inválidos")
        perda_um = (1-probabilidade)*custo_falso_positivo
        perda_zero = probabilidade*custo_falso_negativo
        return int(perda_um < perda_zero)


class AvaliadorProbabilistico:
    @staticmethod
    def pontuar(probs: list[float], rotulos: list[int], faixas: int = 10) -> dict[str, float]:
        if not probs or len(probs) != len(rotulos):
            raise ValueError("Prognósticos e observações incompatíveis")
        if any(not math.isfinite(p) or p < 0 or p > 1 for p in probs):
            raise ValueError("Probabilidades inválidas")
        if any(y not in (0, 1) for y in rotulos):
            raise ValueError("Rótulos binários inválidos")
        brier = statistics.fmean((p-y)**2 for p, y in zip(probs, rotulos))
        perda = -statistics.fmean(y*math.log(max(1e-15, p)) +
                                  (1-y)*math.log(max(1e-15, 1-p))
                                  for p, y in zip(probs, rotulos))
        ece = 0.0
        for faixa in range(faixas):
            pares = [(p, y) for p, y in zip(probs, rotulos)
                     if min(faixas-1, int(p*faixas)) == faixa]
            if pares:
                ece += len(pares)/len(probs) * abs(
                    statistics.fmean(p for p, _ in pares) -
                    statistics.fmean(y for _, y in pares))
        acuracia = statistics.fmean(int(p >= .5) == y for p, y in zip(probs, rotulos))
        return dict(brier=brier, log_loss=perda, ece=ece, acuracia=acuracia)

    @staticmethod
    def bootstrap_ganho(erros_base: list[float], erros_modelo: list[float],
                        seed: int, repeticoes: int = 1000) -> tuple[float, float, float]:
        if len(erros_base) != len(erros_modelo) or not erros_base:
            raise ValueError("Diferenças incompatíveis")
        deltas = [a-b for a, b in zip(erros_base, erros_modelo)]
        media = statistics.fmean(deltas)
        rng = random.Random(seed)
        n = len(deltas)
        replicas = sorted(sum(deltas[rng.randrange(n)] for _ in range(n))/n
                          for _ in range(repeticoes))
        return media, Estatistica.quantil(replicas, .025), Estatistica.quantil(replicas, .975)


@dataclass
class CartaoHipotese:
    identificador: str
    titulo: str
    enunciado: str
    implementacao: str
    linha_base: str
    metrica_primaria: str
    criterio_aceitacao: str
    criterio_rejeicao: str
    origem: str = "lógica criativa"
    dados: str = ""
    orcamento: str = "60 s, 100.000 passos"
    riscos: str = ""
    resultado: str = "[NÃO EXECUTADO]"
    veredito: str = "ADIADA"


class Experimentos:
    """Cartões registrados antes do experimento, juiz usa apenas dados reservados."""
    @staticmethod
    def probabilidade(cfg: Configuracao, repo: Repositorio, modo: str) -> dict[str, Any]:
        cartao = CartaoHipotese(
            identificador="H-M3-001", titulo="Taxas condicionais vs frequência global",
            enunciado="Uma taxa Beta condicional a um atributo binário supera a taxa global",
            implementacao="Beta-Binomial por grupo; treino e teste sem vazamento",
            linha_base="Beta-Binomial global",
            metrica_primaria="ganho de Brier no teste (positivo)",
            criterio_aceitacao="Limite inferior bootstrap 95% do ganho > 0 em cada seed",
            criterio_rejeicao="Limite superior 95% <= 0; caso contrário inconclusiva",
            dados="[SINTÉTICO] 60/20/20, 5 seeds, treino de 600 observações por seed",
            riscos="Estímulo sintético foi construído para beneficiar condicionamento")
        repo.memorizar("hipotese", cartao.identificador, asdict(cartao), "[HIPÓTESE]")
        n = 300 if modo == "rapido" else (1_500 if modo == "padrao" else 8_000)
        relatorios = []
        for seed in cfg.seeds_comparacao:
            rng = random.Random(seed)
            amostras = [(rng.randrange(2), None) for _ in range(n)]
            amostras = [(x, int(rng.random() < (.15 if x == 0 else .85))) for x, _ in amostras]
            treino = amostras[:int(.6*n)]
            validacao = amostras[int(.6*n):int(.8*n)]
            teste = amostras[int(.8*n):]
            global_modelo = BetaBernoulli()
            grupos = {0: BetaBernoulli(), 1: BetaBernoulli()}
            for x, y in treino:
                global_modelo.observar(y)
                grupos[x].observar(y)
            # Validação é registrada, mas não reconfigura os modelos.
            probs_validacao = [grupos[x].prever() for x, _ in validacao]
            y_validacao = [y for _, y in validacao]
            p_base = [global_modelo.prever() for _ in teste]
            p_cond = [grupos[x].prever() for x, _ in teste]
            y_teste = [y for _, y in teste]
            base = AvaliadorProbabilistico.pontuar(p_base, y_teste, cfg.faixas_calibracao)
            modelo = AvaliadorProbabilistico.pontuar(p_cond, y_teste, cfg.faixas_calibracao)
            erro_base = [(p-y)**2 for p, y in zip(p_base, y_teste)]
            erro_mod = [(p-y)**2 for p, y in zip(p_cond, y_teste)]
            ganho, inf, sup = AvaliadorProbabilistico.bootstrap_ganho(
                erro_base, erro_mod, seed+100, cfg.bootstrap)
            relatorios.append(dict(seed=seed, n_treino=len(treino),
                                   n_validacao=len(validacao), n_teste=len(teste),
                                   validacao=AvaliadorProbabilistico.pontuar(
                                       probs_validacao, y_validacao, cfg.faixas_calibracao),
                                   referencia=base, modelo=modelo, ganho_brier=ganho,
                                   ic95_ganho=[inf, sup],
                                   veredito=("ACEITA" if inf > 0 else
                                              "REJEITADA" if sup <= 0 else "INCONCLUSIVA")))
        geral = ("ACEITA" if all(r["veredito"] == "ACEITA" for r in relatorios)
                 else "REJEITADA" if all(r["veredito"] == "REJEITADA" for r in relatorios)
                 else "INCONCLUSIVA")
        cartao.veredito = geral
        cartao.resultado = "[MEDIDO]"
        resultado = dict(versao=VERSAO, cartao=asdict(cartao),
                         dados="[SINTÉTICO]", n_por_seed=n, relatorios=relatorios,
                         escada_evidencias=3, avaliador="funções de métrica separadas do modelo")
        repo.memorizar("resultado", cartao.identificador, resultado, "[MEDIDO]",
                       fonte="gerador sintético e avaliador externo")
        repo.evento("experimento", {"hipotese": cartao.identificador, "veredito": geral})
        repo.salvar_json("experimento_probabilidade.json", resultado)
        return resultado


# Parser lógico puro: sem eval/exec e sem dependência externa.
_PADRAO_LOGICO = re.compile(r"\s*(<->|->|[()!&|]|[A-Za-z][A-Za-z0-9_]*)")


class Logica:
    """Verificador proposicional com limites explícitos."""
    @staticmethod
    def analisar(texto: str) -> tuple:
        if len(texto) > 2_000:
            raise ValueError("Fórmula muito grande")
        partes = _PADRAO_LOGICO.findall(texto)
        if "".join(partes) != re.sub(r"\s+", "", texto):
            raise ValueError("Caractere não permitido na fórmula")
        pos = 0

        def atomico() -> tuple:
            nonlocal pos
            if pos >= len(partes):
                raise ValueError("Fórmula incompleta")
            token = partes[pos]
            pos += 1
            if token == "!":
                return ("not", atomico())
            if token == "(":
                resultado = bicondicional()
                if pos >= len(partes) or partes[pos] != ")":
                    raise ValueError("Parêntese não fechado")
                pos += 1
                return resultado
            if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", token):
                return ("var", token)
            raise ValueError("Token inesperado")

        def conjuncao() -> tuple:
            nonlocal pos
            esquerdo = atomico()
            while pos < len(partes) and partes[pos] == "&":
                pos += 1
                esquerdo = ("and", esquerdo, atomico())
            return esquerdo

        def disjuncao() -> tuple:
            nonlocal pos
            esquerdo = conjuncao()
            while pos < len(partes) and partes[pos] == "|":
                pos += 1
                esquerdo = ("or", esquerdo, conjuncao())
            return esquerdo

        def implicacao() -> tuple:
            nonlocal pos
            esquerdo = disjuncao()
            if pos < len(partes) and partes[pos] == "->":
                pos += 1
                return ("imp", esquerdo, implicacao())
            return esquerdo

        def bicondicional() -> tuple:
            nonlocal pos
            esquerdo = implicacao()
            while pos < len(partes) and partes[pos] == "<->":
                pos += 1
                esquerdo = ("iff", esquerdo, implicacao())
            return esquerdo

        arvore = bicondicional()
        if pos != len(partes):
            raise ValueError("Token restante")
        return arvore

    @staticmethod
    def variaveis(ast: tuple) -> set[str]:
        if ast[0] == "var":
            return {ast[1]}
        return set().union(*(Logica.variaveis(x) for x in ast[1:] if isinstance(x, tuple)))

    @staticmethod
    def calcular(ast: tuple, valores: dict[str, bool]) -> bool:
        op = ast[0]
        if op == "var": return valores[ast[1]]
        if op == "not": return not Logica.calcular(ast[1], valores)
        a, b = Logica.calcular(ast[1], valores), Logica.calcular(ast[2], valores)
        if op == "and": return a and b
        if op == "or": return a or b
        if op == "imp": return (not a) or b
        if op == "iff": return a == b
        raise ValueError("Operação lógica desconhecida")

    @staticmethod
    def satisfativel(formulas: list[str], max_variaveis: int = 16,
                    max_passos: int = 100_000) -> dict[str, Any]:
        arvores = [Logica.analisar(f) for f in formulas]
        nomes = sorted(set().union(*(Logica.variaveis(ast) for ast in arvores)))
        if len(nomes) > max_variaveis or 2**len(nomes) > max_passos:
            return dict(estado="INCONCLUSIVO", motivo="Limite de custo", variaveis=len(nomes))
        for bits in itertools.product((False, True), repeat=len(nomes)):
            valores = dict(zip(nomes, bits))
            if all(Logica.calcular(ast, valores) for ast in arvores):
                return dict(estado="CONSISTENTE", testemunha=valores,
                            variaveis=len(nomes))
        return dict(estado="CONTRADITORIO", variaveis=len(nomes))

    @staticmethod
    def nucleo_inconsistente(formulas: list[str]) -> list[str] | None:
        if len(formulas) > 12:
            return None
        if Logica.satisfativel(formulas)["estado"] != "CONTRADITORIO":
            return None
        for tamanho in range(1, len(formulas)+1):
            for combinacao in itertools.combinations(formulas, tamanho):
                if Logica.satisfativel(list(combinacao))["estado"] == "CONTRADITORIO":
                    return list(combinacao)
        return None


class GeradorCriativo:
    """Gera alternativas formais; a crítica valida, não o gerador."""
    @staticmethod
    def divergente(proposicao: str, seed: int, max_rodadas: int = 5) -> list[dict[str, Any]]:
        rng = random.Random(seed)
        palavras = re.findall(r"[A-Za-z]+", proposicao)[:10] or ["hypothesis"]
        propostas = []
        for rodada in range(min(5, max_rodadas)):
            base = rng.choice(palavras)
            rotacao = (rodada+1) % len(palavras)
            segunda = palavras[rotacao]
            propostas.append(dict(hipotese=f"Se {base}, investigar condição alternativa {segunda}",
                                  contraponto=f"E se {base} não for relevante?",
                                  rotulo="[FICÇÃO EXPERIMENTAL]", status="PENDENTE"))
        return propostas

    @staticmethod
    def criticar(propostas: list[dict[str, Any]], teste: Any | None = None) -> list[dict[str, Any]]:
        """Nenhuma hipótese gerada por texto é aceita sem teste externo."""
        for proposta in propostas:
            proposta["status"] = "INCONCLUSIVA" if teste is None else "TESTE PENDENTE"
        return propostas


# Os agentes são políticas explícitas e auditáveis, não LLMs independentes.
class Agente:
    def __init__(self, papel: str):
        self.papel = papel

    def argumento(self, hipotese: str) -> dict[str, str]:
        textos = {
            "cetico": "Que referência mais simples explica o mesmo efeito?",
            "socratico": "Qual observação falsificaria a hipótese?",
            "criativo": "Imaginar uma combinação alternativa requer um teste externo.",
            "logico": "Formalizar a afirmação antes de decidir consistência.",
            "probabilistico": "Comparar Brier, log loss e calibração fora da amostra.",
            "gradiente": "Comparar o gradiente analítico com diferenças finitas.",
            "simbolico": "Verificar regras explícitas e exceções.",
            "pro_consciencia": "Verificar indicadores funcionais e hipóteses alternativas.",
            "contra_consciencia": "Comportamento observável não prova experiência subjetiva.",
            "auditor": "Não aceitar ganho sem linha de base e teste reservado.",
        }
        return dict(papel=self.papel, argumento=textos[self.papel],
                    hipotese=hipotese, evidencia="não anexada")


def debate(hipotese: str, rodadas: int = 4) -> list[dict[str, Any]]:
    agentes = [Agente(papel) for papel in ("cetico", "socratico", "criativo", "logico",
                      "probabilistico", "gradiente", "simbolico", "pro_consciencia",
                      "contra_consciencia")]
    respostas = []
    for rodada in range(min(rodadas, 4)):
        respostas.append(dict(rodada=rodada+1,
                              argumentos=[a.argumento(hipotese) for a in agentes],
                              parecer=Agente("auditor").argumento(hipotese)))
        if rodada == 0:
            # Políticas fixas repetiriam os mesmos argumentos: parada antecipada.
            break
    return respostas


# Referência adversarial: jogo da velha ótimo e pôquer Kuhn mínimo.
VITORIAS = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))


def vencedor_velha(tabuleiro: str) -> str | None:
    for i, j, k in VITORIAS:
        if tabuleiro[i] != "." and tabuleiro[i] == tabuleiro[j] == tabuleiro[k]:
            return tabuleiro[i]
    return None


@lru_cache(maxsize=None)
def valor_velha(tabuleiro: str, jogador: str = "X") -> int:
    ganhador = vencedor_velha(tabuleiro)
    if ganhador: return 1 if ganhador == jogador else -1
    if "." not in tabuleiro: return 0
    valores = []
    outro = "O" if jogador == "X" else "X"
    for i, item in enumerate(tabuleiro):
        if item == ".":
            proximo = tabuleiro[:i] + jogador + tabuleiro[i+1:]
            valores.append(-valor_velha(proximo, outro))
    return max(valores)


def jogada_otima_velha(tabuleiro: str, jogador: str = "X") -> int:
    outro = "O" if jogador == "X" else "X"
    jogadas = [( -valor_velha(tabuleiro[:i] + jogador + tabuleiro[i+1:], outro), i)
               for i, item in enumerate(tabuleiro) if item == "."]
    if not jogadas: raise ValueError("Partida encerrada")
    return min((-valor, i) for valor, i in jogadas)[1]


def contar_estados_velha() -> int:
    vistos: set[str] = set()
    def visitar(tabuleiro: str, jogador: str) -> None:
        if tabuleiro in vistos: return
        vistos.add(tabuleiro)
        if vencedor_velha(tabuleiro) or "." not in tabuleiro: return
        for i, c in enumerate(tabuleiro):
            if c == ".":
                visitar(tabuleiro[:i] + jogador + tabuleiro[i+1:],
                        "O" if jogador == "X" else "X")
    visitar("."*9, "X")
    return len(vistos)


class PokerKuhn:
    """Jogo de informação imperfeita: 3 cartas, 1 rodada de apostas."""
    @staticmethod
    def premio(cartas: tuple[int, int], historico: str) -> int:
        aposta = historico[-1] == "c" and "b" in historico
        vencedor = 1 if cartas[0] > cartas[1] else -1
        if historico.endswith("f"):
            # Quem desiste é o último jogador que agiria no ramo terminal.
            # 'bf' -> P2 desiste; 'kbf' -> P1 desiste.
            return 1 if historico == "bf" else -1
        return (2 if aposta else 1) * vencedor

    @staticmethod
    def resultado_fixo(cartas: tuple[int, int], rng: random.Random) -> dict[str, Any]:
        # Estratégias propositalmente simples, sem alegação de equilíbrio Nash.
        aposta_primeiro = (cartas[0] == 2 or (cartas[0] == 0 and rng.random() < .25))
        if aposta_primeiro:
            historico = "bc" if cartas[1] == 2 else "bf"
        else:
            aposta_segundo = cartas[1] == 2 or (cartas[1] == 0 and rng.random() < .20)
            if not aposta_segundo:
                historico = "kk"
            else:
                historico = "kbc" if cartas[0] == 2 else "kbf"
        return dict(cartas=["JQK"[c] for c in cartas], historico=historico,
                    lucro_primeiro=PokerKuhn.premio(cartas, historico))


def politica_lexica(definicao: str, treino: list[tuple[str, str, str]]) -> str:
    """Política lexical por similaridade Jaccard; não recebe o gabarito."""
    consulta = set(re.findall(r"[a-z]+", definicao.lower()))
    pares = []
    for palavra, _, descricao in treino:
        termos = set(re.findall(r"[a-z]+", descricao.lower()))
        uniao = consulta | termos
        intersecao = consulta & termos
        pares.append((len(intersecao) / max(1, len(uniao)), palavra))
    return max(pares)[1] if pares else "unknown"


class Raphael:
    """Jogo misto de sete rodadas, árbitro determinístico independente da política."""
    ARENAS = ("lexica", "numerica", "velha", "cartas", "logica")

    @staticmethod
    def pontos(acerto: float, confianca: float, passos_excedentes: int = 0) -> float:
        if not 0 <= acerto <= 1 or not 0 <= confianca <= 1:
            raise ValueError("Acerto/confiança fora de [0,1]")
        return acerto + .5*(1-(confianca-acerto)**2) - .01*max(0, passos_excedentes)

    @staticmethod
    def simular(seed: int, lexico: LagoLexical, repo: Repositorio) -> dict[str, Any]:
        rng = random.Random(seed)
        arenas = list(Raphael.ARENAS) + rng.choices(Raphael.ARENAS, k=2)
        rng.shuffle(arenas)
        itens = lexico_embutido()
        historico = []
        total = 0.0
        for i, arena in enumerate(arenas):
            if arena == "lexica":
                # Conjunto de teste lexical reservado; o agente recebe apenas a definição.
                indice_treino = [entrada for j, entrada in enumerate(itens) if j % 5 != 0]
                teste_lexical = [entrada for j, entrada in enumerate(itens) if j % 5 == 0]
                entrada = rng.choice(teste_lexical)
                dica = entrada[2]
                resposta = politica_lexica(dica, indice_treino)
                # Somente o árbitro usa o gabarito.
                correto = float(resposta == entrada[0])
                estado = {"definicao": dica, "conjunto": "teste_lexical_reservado"}
                acao = resposta
                confianca = .05
            elif arena == "numerica":
                numero = rng.randrange(100_000)
                palavra = LinguaArtificial.codificar(numero)
                resposta = LinguaArtificial.decodificar(palavra)
                correto = float(resposta == numero)
                estado = {"palavra": palavra}
                acao = resposta
                confianca = .99
            elif arena == "velha":
                tabuleiro = "........."
                acao = jogada_otima_velha(tabuleiro)
                correto = float(-valor_velha(tabuleiro[:acao]+"X"+tabuleiro[acao+1:], "O") == 0)
                estado = {"tabuleiro": tabuleiro, "regra": "jogo da velha por minimax"}
                confianca = .99
            elif arena == "cartas":
                cartas = tuple(rng.sample(range(3), 2))
                partida = PokerKuhn.resultado_fixo(cartas, rng)
                correto = max(0., min(1., (partida["lucro_primeiro"]+2)/4))
                estado = {"modalidade": "pôquer Kuhn, estratégia fixa"}
                acao = partida
                confianca = .5
            else:
                formulas = ["A -> B", "A", "!B"] if rng.randrange(2) else ["A -> B", "!B"]
                esperado = "CONTRADITORIO" if len(formulas) == 3 else "CONSISTENTE"
                acao = Logica.satisfativel(formulas)["estado"]
                correto = float(acao == esperado)
                estado = {"formulas": formulas}
                confianca = .95
            pts = Raphael.pontos(correto, confianca)
            rodada = dict(partida=seed, rodada=i+1, arena=arena, estado=estado,
                          acao=acao, confianca=confianca, acerto=correto,
                          pontos=pts, parametros={"seed": seed, "versao": VERSAO})
            historico.append(rodada)
            repo.evento("acao_jogo", rodada)
            total += pts
        return dict(seed=seed, total=round(total, 6), rodadas=historico,
                    observacao="demonstração de arenas; sem treino RL nem juiz isolado")


class Reforco:
    """Recompensa ordinária e extraordinária com penalidade anti-sabotagem."""
    @staticmethod
    def ordinario(acerto: int) -> float:
        return float(acerto)

    @staticmethod
    def extraordinario(acerto: int, diagnostico_correto: int,
                       custo_erro: float = 1., peso_diagnostico: float = .4) -> float:
        if acerto not in (0, 1) or diagnostico_correto not in (0, 1):
            raise ValueError("Rótulos de reforço inválidos")
        if not 0 <= peso_diagnostico < custo_erro:
            raise ValueError("Peso de diagnóstico permitiria sabotagem")
        return acerto - custo_erro*(1-acerto) + peso_diagnostico*diagnostico_correto*(1-acerto)


class Auditor:
    """Auditoria independente do gerador de hipóteses, mas não processo isolado."""
    @staticmethod
    def validar_melhoria(ganho: float, intervalo: tuple[float, float],
                        regressao: bool, licenca_ok: bool, testes_ok: bool) -> dict[str, Any]:
        verificacoes = dict(intervalo_positivo=(intervalo[0] > 0),
                            sem_regressao=(not regressao),
                            licencas=licenca_ok, testes=testes_ok,
                            ganho_observado=(ganho > 0))
        return dict(aceita=all(verificacoes.values()), verificacoes=verificacoes)

    @staticmethod
    def defensivo(entrada: str, caminho: str = "") -> dict[str, Any]:
        # Análise de texto NÃO executa instruções da entrada.
        indicadores = []
        if re.search(r"ignore (all )?previous instructions|ignore as instruções", entrada,
                     flags=re.IGNORECASE):
            indicadores.append("possivel_injecao_de_instrucoes")
        if re.search(r"-----BEGIN .*PRIVATE KEY-----|(?:api[_-]?key|secret)\s*[:=]",
                     entrada, flags=re.IGNORECASE):
            indicadores.append("possivel_segredo")
        if caminho and (".." in Path(caminho).parts or Path(caminho).is_absolute()):
            indicadores.append("caminho_potencialmente_perigoso")
        return dict(sinalizadores=indicadores, executou_entrada=False)


@dataclass
class Mensagem:
    origem: str
    conteudo: Any
    rotulo: str
    confianca: float
    custo: float
    trilha: list[str] = field(default_factory=list)
    carimbo: str = field(default_factory=AGORA)

    def __post_init__(self) -> None:
        validar_rotulo(self.rotulo)
        if not 0 <= self.confianca <= 1:
            raise ValueError("Confiança inválida")


@dataclass
class Contexto:
    config: Configuracao
    repo: Repositorio
    orcamento: Orcamento
    rng: random.Random


class Camada(Protocol):
    nome: str
    def processar(self, msg: Mensagem, ctx: Contexto) -> Mensagem: ...
    def inverter(self, msg: Mensagem, ctx: Contexto) -> Mensagem | None: ...
    def metricas(self) -> dict[str, float]: ...


class CamadaBase:
    nome = "base"

    def __init__(self) -> None:
        self.executadas = 0
        self.segundos = 0.0

    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        return dados

    def processar(self, msg: Mensagem, ctx: Contexto) -> Mensagem:
        ctx.orcamento.consumir()
        inicio = time.monotonic()
        dados = self.transformar(dict(msg.conteudo), ctx)
        gasto = time.monotonic() - inicio
        self.executadas += 1
        self.segundos += gasto
        return Mensagem(origem=self.nome, conteudo=dados, rotulo=msg.rotulo,
                        confianca=msg.confianca, custo=msg.custo+gasto,
                        trilha=msg.trilha+[self.nome])

    def inverter(self, msg: Mensagem, ctx: Contexto) -> Mensagem | None:
        return None

    def metricas(self) -> dict[str, float]:
        return {"executadas": float(self.executadas), "segundos": self.segundos}


class C01Ingestao(CamadaBase):
    nome = "c01_ingestao"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        texto = dados.get("texto")
        if not isinstance(texto, str) or len(texto) > 4_000:
            raise ValueError("Texto ausente ou excede o limite")
        dados["proveniencia"] = dict(fonte="entrada_local", obtido_em=AGORA(),
                                     qualidade="não validada")
        return dados


class C02Linguagem(CamadaBase):
    nome = "c02_linguagem"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        dados["tokens"] = re.findall(r"[^\W_]+", dados["texto"].lower(), flags=re.UNICODE)
        dados["lemas_aproximados"] = list(dados["tokens"])
        dados["lematizacao_validada"] = False
        return dados


class C03Codificacao(CamadaBase):
    nome = "c03_codificacao"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        dados["representacao"] = Codificador.codificar(dados["texto"])
        return dados

    def inverter(self, msg: Mensagem, ctx: Contexto) -> Mensagem | None:
        hex_str = msg.conteudo.get("representacao", {}).get("hexadecimal")
        if not isinstance(hex_str, str): return None
        texto = Codificador.decodificar_hex(hex_str)
        return Mensagem(origem=self.nome+"_inverso", conteudo={"texto": texto},
                        rotulo="[DERIVADO]", confianca=1., custo=msg.custo,
                        trilha=msg.trilha+["inversao_c03"])


class C04Geometria(CamadaBase):
    nome = "c04_geometria"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        vetor = [float(n) for n in dados["representacao"]["utf8"][:32]]
        dados["geometria"] = {"dimensoes": len(vetor), "norma": Geometria.norma(vetor),
                              "cosseno_proprio": Geometria.cosseno(vetor, vetor)}
        return dados


class C05Inferencia(CamadaBase):
    nome = "c05_inferencia"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        # Prior explícito, nunca chamado de previsão semanticamente treinada.
        modelo = BetaBernoulli()
        for palavra in dados["tokens"]:
            modelo.observar(int(palavra in {"logic", "reason", "evidence", "logica"}))
        dados["inferencia"] = {"taxa_de_palavras_alvo": modelo.prever(),
                               "incerteza_parametro": modelo.variancia_parametro(),
                               "observacao": "estatística descritiva com suavização Beta"}
        return dados


class C06Criatividade(CamadaBase):
    nome = "c06_criatividade"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        dados["hipoteses"] = GeradorCriativo.divergente(
            dados["texto"], ctx.config.seed, ctx.config.rodadas_criativas)
        return dados


class C07Critica(CamadaBase):
    nome = "c07_critica"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        dados["hipoteses"] = GeradorCriativo.criticar(dados["hipoteses"])
        dados["teste_logico_padrao"] = Logica.satisfativel(["A -> B", "A", "!B"])["estado"]
        return dados


class C08Jogos(CamadaBase):
    nome = "c08_jogos"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        dados["jogos"] = {"valor_inicial_velha": valor_velha("."*9),
                          "status": "teste de referência, não treinamento"}
        return dados


class C09Metacognicao(CamadaBase):
    nome = "c09_metacognicao"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        dados["metacognicao"] = {
            "descritiva": "trilha por camada",
            "analitica": "ablação ainda necessária",
            "probabilistica": dados["inferencia"],
            "contrafactual": "hipótese alternativa não testada",
            "adversarial": "objeções textuais ainda sem evidência",
            "recursiva": "profundidade finita, execução de uma passagem",
            "pragmatica": "ganho em tarefa não estabelecido",
        }
        return dados


class C10Auditoria(CamadaBase):
    nome = "c10_auditoria"
    def transformar(self, dados: dict[str, Any], ctx: Contexto) -> dict[str, Any]:
        dados["auditoria"] = Auditor.defensivo(dados["texto"])
        dados["auditoria"]["hipoteses_validadas_empiricamente"] = 0
        return dados


CAMADAS = (C01Ingestao, C02Linguagem, C03Codificacao, C04Geometria,
           C05Inferencia, C06Criatividade, C07Critica, C08Jogos,
           C09Metacognicao, C10Auditoria)


class Nucleo:
    def __init__(self, cfg: Configuracao, repo: Repositorio):
        self.cfg = cfg
        self.repo = repo
        self.camadas = [cls() for cls in CAMADAS]

    def executar(self, texto: str) -> Mensagem:
        ctx = Contexto(self.cfg, self.repo, Orcamento(self.cfg), random.Random(self.cfg.seed))
        mensagem = Mensagem("usuario", {"texto": texto}, "[HIPÓTESE]", 0.5, 0.)
        for camada in self.camadas:
            mensagem = camada.processar(mensagem, ctx)
        inverso = self.camadas[2].inverter(mensagem, ctx)
        if inverso is None or inverso.conteudo["texto"] != texto:
            raise AssertionError("Perda de reversibilidade da terceira camada")
        self.repo.evento("ciclo", {"trilha": mensagem.trilha, "passos": ctx.orcamento.passos})
        return mensagem


class RegressaoLogistica:
    """Classificador binário pequeno; inferência estatística separada do gradiente."""
    def __init__(self, dimensoes: int):
        self.pesos = [0.0] * (dimensoes + 1)

    @staticmethod
    def sigmoide(z: float) -> float:
        if z >= 0:
            return 1.0/(1+math.exp(-z))
        e = math.exp(z)
        return e/(1+e)

    def predizer(self, atributos: list[float]) -> float:
        return self.sigmoide(self.pesos[0]+Geometria.produto(self.pesos[1:], atributos))

    def gradiente(self, dados: list[tuple[list[float], int]]) -> list[float]:
        g = [0.0]*len(self.pesos)
        for x, y in dados:
            residuo = self.predizer(x)-y
            g[0] += residuo
            for i, v in enumerate(x):
                g[i+1] += residuo*v
        return [v/len(dados) for v in g]

    def perda(self, dados: list[tuple[list[float], int]]) -> float:
        return -statistics.fmean(y*math.log(max(1e-12,self.predizer(x))) +
            (1-y)*math.log(max(1e-12,1-self.predizer(x))) for x,y in dados)

    def treinar(self, dados: list[tuple[list[float], int]], passos: int = 300,
               taxa: float = .8) -> None:
        for _ in range(passos):
            g = self.gradiente(dados)
            self.pesos = [p-taxa*v for p,v in zip(self.pesos,g)]


def experimento_angulo(cfg: Configuracao, repo: Repositorio, modo: str) -> dict[str, Any]:
    """Testa ganho representacional, não criação de informação pelo ângulo duplo."""
    cartao = CartaoHipotese(
        identificador="H-M2-001", titulo="Ângulo duplo e classificadores lineares",
        enunciado="Um atributo cos(2θ) melhora classificação com simetria de 180°",
        implementacao="Gradiente descendente em regressão logística sem e com cos(2θ)",
        linha_base="Mesma regressão com somente cos(θ)",
        metrica_primaria="ganho de Brier em teste reservado",
        criterio_aceitacao="ganho Brier positivo com IC95% acima de zero em cinco seeds",
        criterio_rejeicao="ganho não positivo com IC95% abaixo de zero",
        dados="[SINTÉTICO] 60/20/20, 5 seeds; sem ajustar pelo teste",
        riscos="Alvo sintético construído com simetria angular conhecida")
    repo.memorizar("hipotese", cartao.identificador, asdict(cartao), "[HIPÓTESE]")
    n = 500 if modo == "rapido" else (1200 if modo == "padrao" else 4000)
    saidas = []
    for seed in cfg.seeds_comparacao:
        rng = random.Random(seed)
        amostras = [(t := rng.uniform(-math.pi, math.pi), None) for _ in range(n)]
        amostras = [(t,int(math.cos(t)**2 > .49)) for t,_ in amostras]
        corte = int(.6*n)
        treino, teste = amostras[:corte], amostras[int(.8*n):]
        basico, transformado = RegressaoLogistica(1), RegressaoLogistica(2)
        basico.treinar([([math.cos(t)],y) for t,y in treino])
        transformado.treinar([([math.cos(t),math.cos(2*t)],y) for t,y in treino])
        y_teste = [y for _,y in teste]
        pb = [basico.predizer([math.cos(t)]) for t,_ in teste]
        pt = [transformado.predizer([math.cos(t),math.cos(2*t)]) for t,_ in teste]
        mb = AvaliadorProbabilistico.pontuar(pb,y_teste)
        mt = AvaliadorProbabilistico.pontuar(pt,y_teste)
        delta,li,ls = AvaliadorProbabilistico.bootstrap_ganho(
            [(p-y)**2 for p,y in zip(pb,y_teste)],
            [(p-y)**2 for p,y in zip(pt,y_teste)], seed+101, cfg.bootstrap)
        saidas.append(dict(seed=seed, referencia=mb, transformado=mt,
                           ganho_brier=delta, ic95=[li,ls]))
    cartao.resultado = "[MEDIDO]"
    cartao.veredito = "ACEITA" if all(s["ic95"][0] > 0 for s in saidas) else "INCONCLUSIVA"
    resultado = dict(cartao=asdict(cartao), versao=VERSAO, rotulo="[MEDIDO]",
                     dados="[SINTÉTICO]", relatorios=saidas,
                     limite="não acrescenta informação matemática; apenas representa não linearidade")
    repo.memorizar("resultado", cartao.identificador, resultado, "[MEDIDO]")
    repo.salvar_json("experimento_angulo.json", resultado)
    return resultado


class MegaSenaLaboratorio:
    """Experimento de hipótese nula; sorteios sintéticos sem recomendação de aposta."""
    @staticmethod
    def probabilidades() -> dict[str, float | int]:
        total = math.comb(60,6)
        return dict(total_combinacoes=total, sena=1/total,
                    quina=math.comb(6,5)*math.comb(54,1)/total,
                    quadra=math.comb(6,4)*math.comb(54,2)/total,
                    acertos_esperados=6*6/60)

    @staticmethod
    def realizar(cfg: Configuracao, repo: Repositorio, modo: str) -> dict[str, Any]:
        cartao = CartaoHipotese(
            identificador="H-M10-001", titulo="Frequência passada prevê sorteio futuro?",
            enunciado="Últimos 100 sorteios aumentam acertos em relação ao acaso",
            implementacao="Janela histórica móvel e teste cronológico reservado",
            linha_base="Seis dezenas uniformes independentes",
            metrica_primaria="diferença na média de acertos",
            criterio_aceitacao="IC95% do ganho > 0 em dados posteriores independentes",
            criterio_rejeicao="IC95% <= 0, caso contrário inconclusivo",
            dados="[SINTÉTICO], sorteios uniformes 6 de 60",
            riscos="Sem dados oficiais; não transferir resultado para sorteios reais")
        repo.memorizar("hipotese", cartao.identificador, asdict(cartao), "[HIPÓTESE]")
        rng = random.Random(cfg.seed)
        n = 400 if modo == "rapido" else (2900 if modo == "padrao" else 10000)
        sorteios = [set(rng.sample(range(1,61),6)) for _ in range(n)]
        resultados = {p: [] for p in ("quentes","frias","aleatoria")}
        deltas = []
        for pos in range(100,n):
            passado = collections.Counter(x for sorteio in sorteios[pos-100:pos] for x in sorteio)
            ranking = sorted(range(1,61),key=lambda x:(-passado[x],x))
            quentes = set(ranking[:6])
            frias = set(ranking[-6:])
            aleatoria = set(rng.sample(range(1,61),6))
            futuro = sorteios[pos]
            for nome, escolha in (("quentes",quentes),("frias",frias),("aleatoria",aleatoria)):
                resultados[nome].append(len(escolha & futuro))
            deltas.append(len(quentes & futuro)-len(aleatoria & futuro))
        media_delta = statistics.fmean(deltas)
        # Bootstrap pareado: reutiliza o mesmo sorteio para ambas as políticas.
        rng_boot = random.Random(cfg.seed+999)
        replicacoes = sorted(statistics.fmean(deltas[rng_boot.randrange(len(deltas))]
                               for _ in deltas) for _ in range(cfg.bootstrap))
        ic = [Estatistica.quantil(replicacoes, .025), Estatistica.quantil(replicacoes, .975)]
        contagem = collections.Counter(x for s in sorteios for x in s)
        esperado = n/10  # cada uma das 60 dezenas aparece em 6/60 dos sorteios
        qui2 = sum((contagem[x]-esperado)**2/esperado for x in range(1,61))
        cartao.resultado = "[MEDIDO]"
        cartao.veredito = ("ACEITA" if ic[0] > 0 else
                           "REJEITADA" if ic[1] <= 0 else "INCONCLUSIVA")
        relatorio = dict(versao=VERSAO, cartao=asdict(cartao),
                         origem="[SINTÉTICO] - sorteios artificiais uniformes",
                         sorteios=n, testes_futuros=n-100, probabilidades=MegaSenaLaboratorio.probabilidades(),
                         medias={k:statistics.fmean(v) for k,v in resultados.items()},
                         diferenca_quentes_menos_aleatorio=media_delta, ic95_pareado=ic,
                         qui_quadrado=qui2, p_valor=Estatistica.qui2_sf(qui2 / (54 / 59), 59),
                         nota="p-valor com o fator 54/59 (6 dezenas distintas por sorteio); nenhum palpite ou vantagem alegada")
        repo.memorizar("resultado", cartao.identificador, relatorio, "[MEDIDO]")
        repo.salvar_json("experimento_megasena.json", relatorio)
        return relatorio


class BandidoContextual:
    """Teste preliminar de RL em dois braços; não é treinamento completo Raphael."""
    @staticmethod
    def simular(seed: int, tipo: str, passos: int = 1000) -> dict[str,float]:
        if tipo not in ("ordinario", "extraordinario"):
            raise ValueError("Algoritmo de reforço desconhecido")
        rng = random.Random(seed)
        q = [0.,0.]
        usos = [0,0]
        erros = 0
        recompensas = 0.
        for _ in range(passos):
            acao = rng.randrange(2) if rng.random() < .1 else (0 if q[0]>=q[1] else 1)
            acerto = int(rng.random() < (.75 if acao == 0 else .55))
            # Ambiente fornece a causa real, mas diagnóstico não é premiado por autodeclaração.
            diagnostico_conferido = int(acerto == 0 and rng.random()<.5)
            recompensa = (Reforco.ordinario(acerto) if tipo == "ordinario" else
                          Reforco.extraordinario(acerto, diagnostico_conferido))
            usos[acao] += 1
            q[acao] += (recompensa-q[acao])/usos[acao]
            erros += 1-acerto
            recompensas += recompensa
        # Teste independente: a política final recebe novos resultados, sem aprendizado.
        melhor = 0 if q[0]>=q[1] else 1
        avaliador = random.Random(seed+10000)
        desempenho = statistics.fmean(int(avaliador.random()<(.75 if melhor == 0 else .55))
                                            for _ in range(200))
        return dict(seed=seed, taxa_erros_treino=erros/passos,
                    recompensa_media_treino=recompensas/passos,
                    desempenho_reservado=desempenho, acao_escolhida=float(melhor))

    @staticmethod
    def comparar(cfg: Configuracao, repo: Repositorio) -> dict[str, Any]:
        cartao = CartaoHipotese(
            identificador="H-M7-001", titulo="Diagnóstico orientado ao erro em bandido",
            enunciado="Reforço extraordinário supera reforço ordinário fora da amostra",
            implementacao="Bandido de dois braços, atualização incremental e testes reservados",
            linha_base="Reforço ordinário com mesmo orçamento e exploração",
            metrica_primaria="taxa de acerto na avaliação reservada",
            criterio_aceitacao="Ganho positivo nas cinco seeds e replicação posterior",
            criterio_rejeicao="Resultado inferior em cinco seeds",
            dados="[SINTÉTICO] 1000 passos/seed; teste 200 passos/seed",
            riscos="Ambiente simples e diagnóstico simulado; não identifica causas no mundo real")
        repo.memorizar("hipotese", cartao.identificador, asdict(cartao), "[HIPÓTESE]")
        rodadas = {tipo:[BandidoContextual.simular(seed,tipo)
                         for seed in cfg.seeds_comparacao]
                    for tipo in ("ordinario","extraordinario")}
        diferencas = [a["desempenho_reservado"]-b["desempenho_reservado"]
                      for a,b in zip(rodadas["extraordinario"],rodadas["ordinario"])]
        cartao.resultado="[MEDIDO]"
        cartao.veredito = "ACEITA" if all(x>0 for x in diferencas) else "INCONCLUSIVA"
        resultado = dict(versao=VERSAO, cartao=asdict(cartao), dados="[SINTÉTICO]",
                         rodadas=rodadas, deltas=diferencas,
                         ressalva="As duas recompensas são avaliadas na mesma tarefa, sem recompensa por alegar consciência")
        repo.memorizar("resultado",cartao.identificador,resultado,"[MEDIDO]")
        repo.salvar_json("experimento_reforco.json",resultado)
        return resultado


# =============================================================================
# EXTENSÃO 3.0 — ESTATÍSTICA EXATA (biblioteca padrão, sem scipy)
# =============================================================================
# Cada função aqui tem um teste em TestesExtensao contra um valor conhecido
# (forma fechada, tabela clássica ou outra função independente).

class Estatistica:
    """Distribuições e testes com funções especiais calculadas por série e fração
    contínua (Numerical Recipes, cap. 6), sem dependências externas."""

    # ---------------- funções especiais ----------------
    @staticmethod
    def gama_inferior_regularizada(a: float, x: float) -> float:
        """P(a, x) = γ(a, x)/Γ(a). Série para x < a+1, fração contínua (Lentz) caso contrário."""
        if a <= 0:
            raise ValueError("a deve ser positivo")
        if x <= 0:
            return 0.0
        if x < a + 1:
            termo = 1.0 / a
            soma = termo
            n = a
            for _ in range(10_000):
                n += 1
                termo *= x / n
                soma += termo
                if abs(termo) < abs(soma) * 1e-16:
                    break
            return soma * math.exp(-x + a * math.log(x) - math.lgamma(a))
        return 1.0 - Estatistica._gama_superior_fc(a, x)

    @staticmethod
    def _gama_superior_fc(a: float, x: float) -> float:
        minusculo = 1e-300
        b = x + 1 - a
        c = 1 / minusculo
        d = 1 / b
        h = d
        for i in range(1, 10_000):
            an = -i * (i - a)
            b += 2
            d = an * d + b
            if abs(d) < minusculo:
                d = minusculo
            c = b + an / c
            if abs(c) < minusculo:
                c = minusculo
            d = 1 / d
            delta = d * c
            h *= delta
            if abs(delta - 1) < 1e-16:
                break
        return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h

    @staticmethod
    def beta_regularizada(x: float, a: float, b: float) -> float:
        """I_x(a, b) pela fração contínua de Lentz, com a simetria I_x(a,b) = 1 − I_{1−x}(b,a)."""
        if not 0 <= x <= 1:
            raise ValueError("x fora de [0, 1]")
        if x in (0.0, 1.0):
            return x
        ln_frente = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                     + a * math.log(x) + b * math.log(1 - x))
        if x < (a + 1) / (a + b + 2):
            return math.exp(ln_frente) * Estatistica._beta_fc(x, a, b) / a
        return 1 - math.exp(ln_frente) * Estatistica._beta_fc(1 - x, b, a) / b

    @staticmethod
    def _beta_fc(x: float, a: float, b: float) -> float:
        minusculo = 1e-300
        qab, qap, qam = a + b, a + 1, a - 1
        c, d = 1.0, 1 - qab * x / qap
        d = 1 / (d if abs(d) > minusculo else minusculo)
        h = d
        for m in range(1, 10_000):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1 + aa * d
            d = 1 / (d if abs(d) > minusculo else minusculo)
            c = 1 + aa / c
            c = c if abs(c) > minusculo else minusculo
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1 + aa * d
            d = 1 / (d if abs(d) > minusculo else minusculo)
            c = 1 + aa / c
            c = c if abs(c) > minusculo else minusculo
            delta = d * c
            h *= delta
            if abs(delta - 1) < 1e-16:
                break
        return h

    @staticmethod
    def _inverter(f, alvo: float, lo: float, hi: float, iteracoes: int = 200) -> float:
        """Bisseção para f crescente: o x em [lo, hi] com f(x) = alvo."""
        for _ in range(iteracoes):
            meio = (lo + hi) / 2
            if f(meio) < alvo:
                lo = meio
            else:
                hi = meio
        return (lo + hi) / 2

    # ---------------- distribuições ----------------
    @staticmethod
    def qui2_cdf(x: float, gl: float) -> float:
        return Estatistica.gama_inferior_regularizada(gl / 2, x / 2) if x > 0 else 0.0

    @staticmethod
    def qui2_sf(x: float, gl: float) -> float:
        return 1.0 - Estatistica.qui2_cdf(x, gl)

    @staticmethod
    def t_cdf(t: float, gl: float) -> float:
        """F(t) da t de Student: 1 − ½ I_{gl/(gl+t²)}(gl/2, ½) para t ≥ 0."""
        x = gl / (gl + t * t)
        cauda = 0.5 * Estatistica.beta_regularizada(x, gl / 2, 0.5)
        return 1 - cauda if t >= 0 else cauda

    @staticmethod
    def t_quantil(p: float, gl: float) -> float:
        if not 0 < p < 1:
            raise ValueError("p fora de (0, 1)")
        if p < 0.5:
            return -Estatistica.t_quantil(1 - p, gl)
        return Estatistica._inverter(lambda t: Estatistica.t_cdf(t, gl), p, 0.0, 1e4)

    @staticmethod
    def beta_quantil(p: float, a: float, b: float) -> float:
        return Estatistica._inverter(lambda x: Estatistica.beta_regularizada(x, a, b), p, 0.0, 1.0)

    @staticmethod
    def normal_cdf(z: float) -> float:
        return 0.5 * math.erfc(-z / math.sqrt(2))

    @staticmethod
    def normal_quantil(p: float) -> float:
        return statistics.NormalDist().inv_cdf(p)

    # ---------------- intervalos ----------------
    @staticmethod
    def wilson(sucessos: int, n: int, confianca: float = 0.95) -> tuple[float, float]:
        if n <= 0:
            raise ValueError("n deve ser positivo")
        z = Estatistica.normal_quantil(0.5 + confianca / 2)
        p = sucessos / n
        centro = (p + z * z / (2 * n)) / (1 + z * z / n)
        meia = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        return max(0.0, centro - meia), min(1.0, centro + meia)

    @staticmethod
    def clopper_pearson(sucessos: int, n: int, confianca: float = 0.95) -> tuple[float, float]:
        """Intervalo binomial EXATO pelos quantis da Beta."""
        a = (1 - confianca) / 2
        lo = 0.0 if sucessos == 0 else Estatistica.beta_quantil(a, sucessos, n - sucessos + 1)
        hi = 1.0 if sucessos == n else Estatistica.beta_quantil(1 - a, sucessos + 1, n - sucessos)
        return lo, hi

    @staticmethod
    def beta_credivel(a: float, b: float, nivel: float = 0.95) -> tuple[float, float]:
        """Intervalo de credibilidade EXATO da posterior Beta(a, b) (corrige a aproximação normal da 2.2.0)."""
        cauda = (1 - nivel) / 2
        return Estatistica.beta_quantil(cauda, a, b), Estatistica.beta_quantil(1 - cauda, a, b)

    @staticmethod
    def media_ic_t(dados: list[float], confianca: float = 0.95) -> tuple[float, float, float]:
        n = len(dados)
        if n < 2:
            raise ValueError("São necessários ao menos 2 dados")
        media = statistics.fmean(dados)
        s = statistics.stdev(dados)
        m = Estatistica.t_quantil(0.5 + confianca / 2, n - 1) * s / math.sqrt(n)
        return media, media - m, media + m

    @staticmethod
    def quantil(valores: list[float], p: float) -> float:
        """Quantil por interpolação linear (tipo 7), para qualquer número de valores."""
        v = sorted(valores)
        if not v:
            raise ValueError("Lista vazia")
        h = (len(v) - 1) * p
        i = math.floor(h)
        j = min(i + 1, len(v) - 1)
        return v[i] + (h - i) * (v[j] - v[i])

    @staticmethod
    def bootstrap_media(dados: list[float], seed: int, repeticoes: int = 1000,
                        confianca: float = 0.95) -> tuple[float, float, float]:
        """IC percentil da média com os quantis calculados do NÚMERO de réplicas (corrige os índices
        fixos [24]/[974] da 2.2.0, que quebravam com outro número de réplicas)."""
        if not dados:
            raise ValueError("Lista vazia")
        rng = random.Random(seed)
        n = len(dados)
        replicas = [statistics.fmean(dados[rng.randrange(n)] for _ in range(n)) for _ in range(repeticoes)]
        a = (1 - confianca) / 2
        return statistics.fmean(dados), Estatistica.quantil(replicas, a), Estatistica.quantil(replicas, 1 - a)

    # ---------------- testes ----------------
    @staticmethod
    def t_pareado(a: list[float], b: list[float]) -> dict[str, float]:
        if len(a) != len(b) or len(a) < 2:
            raise ValueError("Amostras pareadas incompatíveis")
        d = [x - y for x, y in zip(a, b)]
        n = len(d)
        s = statistics.stdev(d)
        media = statistics.fmean(d)
        if s == 0:
            return dict(t=math.inf if media else 0.0, gl=n - 1, p_bilateral=0.0 if media else 1.0, media=media)
        t = media / (s / math.sqrt(n))
        return dict(t=t, gl=n - 1, p_bilateral=2 * (1 - Estatistica.t_cdf(abs(t), n - 1)), media=media)

    @staticmethod
    def binomial_exato(sucessos: int, n: int, p: float = 0.5) -> float:
        """P-valor bilateral exato: soma das probabilidades ≤ a do observado."""
        probs = [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
        obs = probs[sucessos]
        return min(1.0, sum(x for x in probs if x <= obs * (1 + 1e-12)))

    @staticmethod
    def sinal(diferencas: list[float]) -> dict[str, float]:
        pos = sum(d > 0 for d in diferencas)
        neg = sum(d < 0 for d in diferencas)
        n = pos + neg
        return dict(positivos=pos, negativos=neg, empates=len(diferencas) - n,
                    p_bilateral=Estatistica.binomial_exato(pos, n) if n else 1.0)

    @staticmethod
    def permutacao_pareada(a: list[float], b: list[float], seed: int, repeticoes: int = 5000) -> float:
        """P-valor bilateral por troca aleatória de sinal das diferenças pareadas."""
        d = [x - y for x, y in zip(a, b)]
        obs = abs(statistics.fmean(d))
        rng = random.Random(seed)
        extremos = 0
        for _ in range(repeticoes):
            m = abs(statistics.fmean(x if rng.random() < 0.5 else -x for x in d))
            extremos += m >= obs - 1e-15
        return (extremos + 1) / (repeticoes + 1)

    @staticmethod
    def holm(p_valores: dict[str, float], alfa: float = 0.05) -> dict[str, bool]:
        """Correção de Holm–Bonferroni para várias hipóteses: devolve quem é rejeitada."""
        ordem = sorted(p_valores.items(), key=lambda kv: kv[1])
        m = len(ordem)
        rejeita, parou = {}, False
        for i, (nome, p) in enumerate(ordem):
            if not parou and p <= alfa / (m - i):
                rejeita[nome] = True
            else:
                parou = True
                rejeita[nome] = False
        return rejeita

    @staticmethod
    def qui2_uniformidade(contagens: list[int], fator: float = 1.0) -> dict[str, float]:
        """Qui-quadrado de aderência à uniforme. `fator` corrige a escala quando as categorias não são
        multinomiais (Mega-Sena: 6 dezenas DISTINTAS por sorteio; ver MegaSenaCorrigida)."""
        n = sum(contagens)
        k = len(contagens)
        e = n / k
        x = sum((c - e) ** 2 / e for c in contagens)
        return dict(estatistica=x, gl=k - 1, fator=fator, p_valor=Estatistica.qui2_sf(x / fator, k - 1))


# =============================================================================
# EXTENSÃO 3.0 — ÁLGEBRA LINEAR (listas de listas, sem numpy)
# =============================================================================

class AlgebraLinear:
    @staticmethod
    def identidade(n: int) -> list[list[float]]:
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    @staticmethod
    def transposta(a: list[list[float]]) -> list[list[float]]:
        return [list(c) for c in zip(*a)]

    @staticmethod
    def produto(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
        if len(a[0]) != len(b):
            raise ValueError("Dimensões incompatíveis")
        bt = AlgebraLinear.transposta(b)
        return [[sum(x * y for x, y in zip(linha, coluna)) for coluna in bt] for linha in a]

    @staticmethod
    def aplicar(a: list[list[float]], v: list[float]) -> list[float]:
        return [sum(x * y for x, y in zip(linha, v)) for linha in a]

    @staticmethod
    def eliminacao(a: list[list[float]]) -> tuple[list[list[float]], list[int], int]:
        """LU com pivô parcial (Doolittle, no lugar). Devolve (LU, permutação, sinal)."""
        n = len(a)
        m = [list(map(float, linha)) for linha in a]
        perm = list(range(n))
        sinal = 1
        for c in range(n):
            p = max(range(c, n), key=lambda r: abs(m[r][c]))
            if abs(m[p][c]) < 1e-300:
                raise ValueError("Matriz singular")
            if p != c:
                m[c], m[p] = m[p], m[c]
                perm[c], perm[p] = perm[p], perm[c]
                sinal = -sinal
            for r in range(c + 1, n):
                f = m[r][c] / m[c][c]
                m[r][c] = f
                for k in range(c + 1, n):
                    m[r][k] -= f * m[c][k]
        return m, perm, sinal

    @staticmethod
    def determinante(a: list[list[float]]) -> float:
        try:
            lu, _, sinal = AlgebraLinear.eliminacao(a)
        except ValueError:
            return 0.0
        d = float(sinal)
        for i in range(len(a)):
            d *= lu[i][i]
        return d

    @staticmethod
    def resolver(a: list[list[float]], b: list[float]) -> list[float]:
        lu, perm, _ = AlgebraLinear.eliminacao(a)
        n = len(a)
        y = [0.0] * n
        for i in range(n):
            y[i] = b[perm[i]] - sum(lu[i][k] * y[k] for k in range(i))
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(lu[i][k] * x[k] for k in range(i + 1, n))) / lu[i][i]
        return x

    @staticmethod
    def inversa(a: list[list[float]]) -> list[list[float]]:
        n = len(a)
        colunas = [AlgebraLinear.resolver(a, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
        return AlgebraLinear.transposta(colunas)

    @staticmethod
    def minimos_quadrados(x: list[list[float]], y: list[float], cumeeira: float = 0.0) -> list[float]:
        """β = (XᵀX + λI)⁻¹ Xᵀy pelas equações normais (λ = 0: mínimos quadrados ordinários)."""
        xt = AlgebraLinear.transposta(x)
        xtx = AlgebraLinear.produto(xt, x)
        for i in range(len(xtx)):
            xtx[i][i] += cumeeira
        return AlgebraLinear.resolver(xtx, AlgebraLinear.aplicar(xt, y))

    @staticmethod
    def gram_schmidt(a: list[list[float]]) -> tuple[list[list[float]], list[list[float]]]:
        """QR por Gram–Schmidt modificado (colunas de a). Devolve (Q, R)."""
        n, m = len(a), len(a[0])
        colunas = [[a[i][j] for i in range(n)] for j in range(m)]
        q, r = [], [[0.0] * m for _ in range(m)]
        for j, v in enumerate(colunas):
            v = list(v)
            for i, u in enumerate(q):
                r[i][j] = sum(x * y for x, y in zip(u, v))
                v = [x - r[i][j] * y for x, y in zip(v, u)]
            r[j][j] = math.sqrt(sum(x * x for x in v))
            if r[j][j] < 1e-300:
                raise ValueError("Colunas linearmente dependentes")
            q.append([x / r[j][j] for x in v])
        return AlgebraLinear.transposta(q), r

    @staticmethod
    def jacobi(s: list[list[float]], varreduras: int = 100) -> tuple[list[float], list[list[float]]]:
        """Autovalores e autovetores de uma matriz simétrica (Jacobi cíclico). Devolve (valores, vetores em colunas)."""
        n = len(s)
        a = [list(map(float, l)) for l in s]
        v = AlgebraLinear.identidade(n)
        for _ in range(varreduras):
            fora = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
            if fora < 1e-30:
                break
            for p in range(n - 1):
                for q in range(p + 1, n):
                    if abs(a[p][q]) < 1e-300:
                        continue
                    th = (a[q][q] - a[p][p]) / (2 * a[p][q])
                    t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1))
                    c = 1 / math.sqrt(t * t + 1)
                    sn = t * c
                    for k in range(n):
                        akp, akq = a[k][p], a[k][q]
                        a[k][p], a[k][q] = c * akp - sn * akq, sn * akp + c * akq
                    for k in range(n):
                        apk, aqk = a[p][k], a[q][k]
                        a[p][k], a[q][k] = c * apk - sn * aqk, sn * apk + c * aqk
                    for k in range(n):
                        vkp, vkq = v[k][p], v[k][q]
                        v[k][p], v[k][q] = c * vkp - sn * vkq, sn * vkp + c * vkq
        return [a[i][i] for i in range(n)], v

    @staticmethod
    def valores_singulares(a: list[list[float]]) -> list[float]:
        valores, _ = AlgebraLinear.jacobi(AlgebraLinear.produto(AlgebraLinear.transposta(a), a))
        return sorted((math.sqrt(max(x, 0.0)) for x in valores), reverse=True)

    @staticmethod
    def potencia(a: list[list[float]], iteracoes: int = 1000, seed: int = 0) -> tuple[float, list[float]]:
        """Maior autovalor em módulo pela iteração de potência (com o quociente de Rayleigh)."""
        rng = random.Random(seed)
        v = [rng.gauss(0, 1) for _ in range(len(a))]
        for _ in range(iteracoes):
            w = AlgebraLinear.aplicar(a, v)
            nw = math.sqrt(sum(x * x for x in w))
            if nw == 0:
                return 0.0, v
            v = [x / nw for x in w]
        av = AlgebraLinear.aplicar(a, v)
        return sum(x * y for x, y in zip(v, av)), v

    @staticmethod
    def componentes_principais(dados: list[list[float]], k: int) -> dict[str, Any]:
        """PCA pela covariância (Jacobi): as k direções, as variâncias e a fração explicada."""
        n, d = len(dados), len(dados[0])
        medias = [statistics.fmean(l[j] for l in dados) for j in range(d)]
        centrados = [[l[j] - medias[j] for j in range(d)] for l in dados]
        cov = [[sum(c[i] * c[j] for c in centrados) / (n - 1) for j in range(d)] for i in range(d)]
        valores, vetores = AlgebraLinear.jacobi(cov)
        ordem = sorted(range(d), key=lambda i: -valores[i])
        total = sum(valores)
        return dict(variancias=[valores[i] for i in ordem[:k]],
                    fracao_explicada=sum(valores[i] for i in ordem[:k]) / total if total else 0.0,
                    direcoes=[[vetores[r][i] for r in range(d)] for i in ordem[:k]], medias=medias)


# =============================================================================
# EXTENSÃO 3.0 — CALIBRAÇÃO (recalibrar probabilidades com dados reservados)
# =============================================================================

class Calibracao:
    @staticmethod
    def isotonica(probs: list[float], rotulos: list[int]) -> list[tuple[float, float]]:
        """Regressão isotônica pelo algoritmo PAV (pool adjacent violators). Devolve os degraus
        [(limite superior da probabilidade, frequência calibrada)], monotônicos."""
        pares = sorted(zip(probs, rotulos))
        blocos = []  # [soma_y, contagem, maior_p]
        for p, y in pares:
            blocos.append([float(y), 1, p])
            while len(blocos) > 1 and blocos[-2][0] / blocos[-2][1] > blocos[-1][0] / blocos[-1][1]:
                s, c, m = blocos.pop()
                blocos[-1][0] += s
                blocos[-1][1] += c
                blocos[-1][2] = m
        return [(m, s / c) for s, c, m in blocos]

    @staticmethod
    def aplicar_isotonica(degraus: list[tuple[float, float]], p: float) -> float:
        for limite, valor in degraus:
            if p <= limite:
                return valor
        return degraus[-1][1]

    @staticmethod
    def platt(probs: list[float], rotulos: list[int], iteracoes: int = 100) -> tuple[float, float]:
        """Escala de Platt: p' = σ(a·logit(p) + b), a e b por Newton na perda logarítmica."""
        z = [math.log(max(1e-12, p) / max(1e-12, 1 - p)) for p in probs]
        a, b = 1.0, 0.0
        for _ in range(iteracoes):
            ga = gb = haa = hab = hbb = 0.0
            for zi, y in zip(z, rotulos):
                q = RegressaoLogistica.sigmoide(a * zi + b)
                r = q - y
                w = q * (1 - q)
                ga += r * zi
                gb += r
                haa += w * zi * zi
                hab += w * zi
                hbb += w
            det = haa * hbb - hab * hab + 1e-12
            da = (hbb * ga - hab * gb) / det
            db = (haa * gb - hab * ga) / det
            a, b = a - da, b - db
            if abs(da) + abs(db) < 1e-12:
                break
        return a, b

    @staticmethod
    def diagrama(probs: list[float], rotulos: list[int], faixas: int = 10) -> list[dict[str, float]]:
        """Diagrama de confiabilidade: por faixa, a confiança média, a frequência observada, n e o IC de Wilson."""
        linhas = []
        for f in range(faixas):
            pares = [(p, y) for p, y in zip(probs, rotulos) if min(faixas - 1, int(p * faixas)) == f]
            if not pares:
                continue
            k = sum(y for _, y in pares)
            lo, hi = Estatistica.wilson(k, len(pares))
            linhas.append(dict(faixa=f, n=len(pares), confianca=statistics.fmean(p for p, _ in pares),
                               frequencia=k / len(pares), ic_lo=lo, ic_hi=hi))
        return linhas

    @staticmethod
    def experimento(seed: int = 7, n: int = 3000) -> dict[str, Any]:
        """Um previsor DESCALIBRADO de propósito (p' = p^0,5, superconfiante para baixo) recalibrado com
        metade dos dados e avaliado na outra metade: ECE antes e depois, para isotônica e Platt."""
        rng = random.Random(seed)
        verdade = [rng.random() for _ in range(n)]
        y = [int(rng.random() < p) for p in verdade]
        previsto = [math.sqrt(p) for p in verdade]
        meio = n // 2
        degraus = Calibracao.isotonica(previsto[:meio], y[:meio])
        a, b = Calibracao.platt(previsto[:meio], y[:meio])
        teste_p, teste_y = previsto[meio:], y[meio:]
        iso = [Calibracao.aplicar_isotonica(degraus, p) for p in teste_p]
        pl = [RegressaoLogistica.sigmoide(a * math.log(max(1e-12, p) / max(1e-12, 1 - p)) + b) for p in teste_p]
        return dict(ece_antes=AvaliadorProbabilistico.pontuar(teste_p, teste_y)["ece"],
                    ece_isotonica=AvaliadorProbabilistico.pontuar(iso, teste_y)["ece"],
                    ece_platt=AvaliadorProbabilistico.pontuar(pl, teste_y)["ece"],
                    brier_antes=AvaliadorProbabilistico.pontuar(teste_p, teste_y)["brier"],
                    brier_isotonica=AvaliadorProbabilistico.pontuar(iso, teste_y)["brier"],
                    platt=(a, b), rotulo="[MEDIDO]", dados="[SINTÉTICO]")


# =============================================================================
# EXTENSÃO 3.0 — BANDIDOS DE K BRAÇOS (ε-guloso, UCB1, Thompson) com arrependimento
# =============================================================================

class Bandidos:
    """Braços de Bernoulli. O arrependimento é calculado com as médias VERDADEIRAS (não com
    as amostras), então a comparação entre políticas não depende da sorte do avaliador."""

    @staticmethod
    def jogar(politica: str, medias: list[float], passos: int, seed: int, epsilon: float = 0.1) -> dict[str, float]:
        rng = random.Random(seed)
        k = len(medias)
        n = [0] * k
        s = [0.0] * k
        a_beta, b_beta = [1.0] * k, [1.0] * k
        melhor = max(medias)
        arrependimento = 0.0
        for t in range(1, passos + 1):
            if politica == "epsilon":
                if rng.random() < epsilon or 0 in n:
                    braco = rng.randrange(k)
                else:
                    braco = max(range(k), key=lambda i: s[i] / n[i])
            elif politica == "ucb1":
                if 0 in n:
                    braco = n.index(0)
                else:
                    braco = max(range(k), key=lambda i: s[i] / n[i] + math.sqrt(2 * math.log(t) / n[i]))
            elif politica == "thompson":
                braco = max(range(k), key=lambda i: rng.betavariate(a_beta[i], b_beta[i]))
            else:
                raise ValueError("Política desconhecida")
            r = int(rng.random() < medias[braco])
            n[braco] += 1
            s[braco] += r
            a_beta[braco] += r
            b_beta[braco] += 1 - r
            arrependimento += melhor - medias[braco]
        return dict(arrependimento=arrependimento, fracao_melhor=n[medias.index(melhor)] / passos)

    @staticmethod
    def comparar(medias: list[float] = (0.75, 0.55, 0.5), passos: int = 2000,
                 sementes: range = range(30)) -> dict[str, Any]:
        """As três políticas nas MESMAS sementes; teste t pareado do arrependimento e correção de Holm."""
        medias = list(medias)
        res = {p: [Bandidos.jogar(p, medias, passos, s)["arrependimento"] for s in sementes]
               for p in ("epsilon", "ucb1", "thompson")}
        pares = {"thompson-ucb1": Estatistica.t_pareado(res["thompson"], res["ucb1"]),
                 "thompson-epsilon": Estatistica.t_pareado(res["thompson"], res["epsilon"]),
                 "ucb1-epsilon": Estatistica.t_pareado(res["ucb1"], res["epsilon"])}
        holm = Estatistica.holm({k: v["p_bilateral"] for k, v in pares.items()})
        return dict(medias_arrependimento={k: statistics.fmean(v) for k, v in res.items()},
                    pares=pares, rejeita_holm=holm, sementes=len(sementes), rotulo="[MEDIDO]")

    @staticmethod
    def lai_robbins(medias: list[float]) -> float:
        """A constante de Lai–Robbins: arrependimento ≥ c·ln T assintoticamente, c = Σ Δᵢ/KL(μᵢ, μ*)."""
        melhor = max(medias)
        c = 0.0
        for m in medias:
            if m < melhor:
                kl = m * math.log(m / melhor) + (1 - m) * math.log((1 - m) / (1 - melhor))
                c += (melhor - m) / kl
        return c


# =============================================================================
# EXTENSÃO 3.0 — INFORMAÇÃO E TEXTO
# =============================================================================

class Informacao:
    @staticmethod
    def entropia(probs: list[float], base: float = 2.0) -> float:
        return -sum(p * math.log(p, base) for p in probs if p > 0)

    @staticmethod
    def kl(p: list[float], q: list[float], base: float = 2.0) -> float:
        if any(pi > 0 and qi == 0 for pi, qi in zip(p, q)):
            return math.inf
        return sum(pi * math.log(pi / qi, base) for pi, qi in zip(p, q) if pi > 0)

    @staticmethod
    def informacao_mutua(pares: list[tuple[Any, Any]]) -> float:
        """I(X; Y) empírica em bits a partir de pares observados."""
        n = len(pares)
        cxy = collections.Counter(pares)
        cx = collections.Counter(x for x, _ in pares)
        cy = collections.Counter(y for _, y in pares)
        return sum(c / n * math.log2((c / n) / ((cx[x] / n) * (cy[y] / n))) for (x, y), c in cxy.items())

    @staticmethod
    def levenshtein(a: str, b: str) -> int:
        anterior = list(range(len(b) + 1))
        for i, ca in enumerate(a, 1):
            atual = [i]
            for j, cb in enumerate(b, 1):
                atual.append(min(anterior[j] + 1, atual[j - 1] + 1, anterior[j - 1] + (ca != cb)))
            anterior = atual
        return anterior[-1]

    @staticmethod
    def jaccard(a: set, b: set) -> float:
        return len(a & b) / len(a | b) if a | b else 1.0


class ModeloCaracteres:
    """Modelo de n-gramas de caracteres com suavização de Witten–Bell (interpolada até o unigrama
    e a uniforme). Mede bits por caractere num texto reservado."""

    def __init__(self, ordem: int = 3):
        if ordem < 1:
            raise ValueError("Ordem mínima 1")
        self.ordem = ordem
        self.contagens: list[dict[str, collections.Counter]] = [collections.defaultdict(collections.Counter)
                                                                 for _ in range(ordem)]
        self.alfabeto: set[str] = set()

    def treinar(self, texto: str) -> "ModeloCaracteres":
        texto = "\x02" * (self.ordem - 1) + texto
        self.alfabeto |= set(texto)
        for i in range(self.ordem - 1, len(texto)):
            for k in range(self.ordem):
                contexto = texto[i - k:i]
                self.contagens[k][contexto][texto[i]] += 1
        return self

    def prob(self, contexto: str, c: str) -> float:
        p = 1.0 / max(1, len(self.alfabeto) + 1)
        for k in range(self.ordem):
            ctx = contexto[len(contexto) - k:] if k else ""
            tabela = self.contagens[k].get(ctx)
            if not tabela:
                continue
            total = sum(tabela.values())
            tipos = len(tabela)
            lam = total / (total + tipos)
            p = lam * tabela.get(c, 0) / total + (1 - lam) * p
        return p

    def bits_por_caractere(self, texto: str) -> float:
        texto = "\x02" * (self.ordem - 1) + texto
        bits = 0.0
        n = 0
        for i in range(self.ordem - 1, len(texto)):
            bits -= math.log2(self.prob(texto[i - self.ordem + 1:i], texto[i]))
            n += 1
        return bits / max(1, n)

    def gerar(self, n: int, seed: int) -> str:
        rng = random.Random(seed)
        contexto = "\x02" * (self.ordem - 1)
        saida = []
        letras = sorted(self.alfabeto - {"\x02"})
        for _ in range(n):
            pesos = [self.prob(contexto, c) for c in letras]
            c = rng.choices(letras, weights=pesos)[0]
            saida.append(c)
            contexto = (contexto + c)[-(self.ordem - 1):] if self.ordem > 1 else ""
        return "".join(saida)


# =============================================================================
# EXTENSÃO 3.0 — DINÂMICA NÃO LINEAR
# =============================================================================

class Dinamica:
    @staticmethod
    def rk4(f, estado: list[float], dt: float, passos: int) -> list[list[float]]:
        """Runge–Kutta de 4ª ordem para d estado/dt = f(estado)."""
        trajetoria = [list(estado)]
        x = list(estado)
        for _ in range(passos):
            k1 = f(x)
            k2 = f([a + dt / 2 * b for a, b in zip(x, k1)])
            k3 = f([a + dt / 2 * b for a, b in zip(x, k2)])
            k4 = f([a + dt * b for a, b in zip(x, k3)])
            x = [a + dt / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(x, k1, k2, k3, k4)]
            trajetoria.append(x)
        return trajetoria

    @staticmethod
    def lorenz(sigma: float = 10.0, rho: float = 28.0, beta: float = 8 / 3):
        return lambda v: [sigma * (v[1] - v[0]), v[0] * (rho - v[2]) - v[1], v[0] * v[1] - beta * v[2]]

    @staticmethod
    def lyapunov_benettin(f, estado: list[float], dt: float = 0.01, passos: int = 20_000,
                          d0: float = 1e-8, descarte: int = 1000) -> float:
        """Maior expoente de Lyapunov por duas trajetórias vizinhas renormalizadas a cada passo (Benettin)."""
        x = list(estado)
        for _ in range(descarte):
            x = Dinamica.rk4(f, x, dt, 1)[-1]
        y = [x[0] + d0] + x[1:]
        soma = 0.0
        for _ in range(passos):
            x = Dinamica.rk4(f, x, dt, 1)[-1]
            y = Dinamica.rk4(f, y, dt, 1)[-1]
            d = math.sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))
            soma += math.log(d / d0)
            y = [a + d0 * (b - a) / d for a, b in zip(x, y)]
        return soma / (passos * dt)

    @staticmethod
    def periodo_logistico(r: float, transiente: int = 5000, maximo: int = 64, tol: float = 1e-9) -> int | None:
        """O período da órbita atratora do mapa logístico (None se não periódica até `maximo`)."""
        x = 0.4
        for _ in range(transiente):
            x = r * x * (1 - x)
        orbita = [x]
        for _ in range(maximo):
            x = r * x * (1 - x)
            orbita.append(x)
        for p in range(1, maximo + 1):
            if all(abs(orbita[i] - orbita[i + p]) < tol for i in range(maximo + 1 - p)):
                return p
        return None

    @staticmethod
    def feigenbaum(r_inicial: float = 2.9, r_final: float = 3.57, passos: int = 3000) -> list[float]:
        """Os valores de r em que o período dobra (1→2→4→8...), por varredura; as razões entre os
        intervalos sucessivos convergem para δ = 4,669..."""
        dobras = []
        ultimo = Dinamica.periodo_logistico(r_inicial)
        for i in range(1, passos + 1):
            r = r_inicial + (r_final - r_inicial) * i / passos
            p = Dinamica.periodo_logistico(r)
            if p is not None and ultimo is not None and p == 2 * ultimo:
                dobras.append(r)
            if p is not None:
                ultimo = p
        return dobras


# =============================================================================
# EXTENSÃO 3.0 — JOGOS DE INFORMAÇÃO IMPERFEITA: KUHN E LEDUC, CFR E MCCFR,
# MELHOR RESPOSTA EXATA E PROGRAMAÇÃO LINEAR (SIMPLEX EM FRAÇÕES)
# =============================================================================
# A 2.2.0 tinha só o prêmio do Kuhn e uma estratégia fixa "sem alegação de equilíbrio".
# Aqui o equilíbrio é CALCULADO de três jeitos independentes (CFR, programação linear
# exata e melhor resposta), e a explorabilidade mede quanto uma estratégia cede.

class JogoKuhn:
    """Pôquer de Kuhn: cartas 0 < 1 < 2 (valete, dama, rei), ante 1, uma aposta de 1.
    Ações: "p" (passar/desistir) e "b" (apostar/pagar)."""
    nome = "kuhn"
    DISTRIBUICOES = tuple((a, b, -1) for a in range(3) for b in range(3) if a != b)

    @staticmethod
    def acoes(h: str) -> tuple[str, ...]:
        return ("p", "b")

    @staticmethod
    def jogador(h: str) -> int:
        return len(h) % 2

    @staticmethod
    def proximo(h: str, a: str) -> str:
        return h + a

    @staticmethod
    def terminal(h: str, c1: int, c2: int, _b: int = -1) -> float | None:
        ganha = 1.0 if c1 > c2 else -1.0
        if h == "pp":
            return ganha
        if h in ("bb", "pbb"):
            return 2 * ganha
        if h == "bp":
            return 1.0
        if h == "pbp":
            return -1.0
        return None

    @staticmethod
    def chave(h: str, c1: int, c2: int, _b: int = -1) -> tuple:
        return (c1 if len(h) % 2 == 0 else c2, h)


class JogoLeduc:
    """Pôquer Leduc (Southey et al., 2005): 6 cartas (2×valete, 2×dama, 2×rei), ante 1, carta pública
    entre as rodadas, apostas fixas 2 e 4, no máximo 2 aumentos por rodada, o jogador 1 abre as duas.
    Ações "c" (passar/pagar), "r" (apostar/aumentar), "f" (desistir diante de aposta). Pareia com a
    pública: ganha; senão a maior; iguais dividem. As 120 distribuições ordenadas são o acaso."""
    nome = "leduc"
    POSTOS = (0, 0, 1, 1, 2, 2)
    DISTRIBUICOES = tuple((a // 2, b // 2, c // 2) for a, b, c in itertools.permutations(range(6), 3))
    APOSTA = (2, 4)

    @staticmethod
    def _rodada(h: str) -> tuple[str, int]:
        return h.split("/")[-1], h.count("/")

    @staticmethod
    def acoes(h: str) -> tuple[str, ...]:
        s, _ = JogoLeduc._rodada(h)
        if s.endswith("r"):
            return ("f", "c", "r") if s.count("r") < 2 else ("f", "c")
        return ("c", "r")

    @staticmethod
    def jogador(h: str) -> int:
        return len(JogoLeduc._rodada(h)[0]) % 2

    @staticmethod
    def _acabou(s: str) -> bool:
        return s == "cc" or (len(s) >= 2 and s.endswith("rc"))

    @staticmethod
    def proximo(h: str, a: str) -> str:
        h2 = h + a
        s, r = JogoLeduc._rodada(h2)
        return h2 + "/" if r == 0 and JogoLeduc._acabou(s) else h2

    @staticmethod
    def contribuicoes(h: str) -> list[int]:
        pos = [1, 1]
        for r, s in enumerate(h.split("/")):
            devido = [0, 0]
            for i, a in enumerate(s):
                if a == "c":
                    devido[i % 2] = max(devido)
                elif a == "r":
                    devido[i % 2] = max(devido) + JogoLeduc.APOSTA[r]
            pos[0] += devido[0]
            pos[1] += devido[1]
        return pos

    @staticmethod
    def terminal(h: str, c1: int, c2: int, b: int) -> float | None:
        s, r = JogoLeduc._rodada(h)
        if s.endswith("f"):
            quem = (len(s) - 1) % 2
            pos = JogoLeduc.contribuicoes(h[:-1])
            return -float(pos[0]) if quem == 0 else float(pos[1])
        if r == 1 and JogoLeduc._acabou(s):
            pos = JogoLeduc.contribuicoes(h)
            f1 = 10 + c1 if c1 == b else c1
            f2 = 10 + c2 if c2 == b else c2
            return float(pos[1]) if f1 > f2 else (-float(pos[0]) if f2 > f1 else 0.0)
        return None

    @staticmethod
    def chave(h: str, c1: int, c2: int, b: int) -> tuple:
        j = JogoLeduc.jogador(h)
        return (c1 if j == 0 else c2, b if "/" in h else -1, h)


class LCGPortavel:
    """Gerador congruencial inteiro (portável entre linguagens): o uniforme x/2³¹ é exato."""
    def __init__(self, semente: int):
        self.x = semente

    def inteiro(self, n: int) -> int:
        self.x = (1103515245 * self.x + 12345) % 2147483648
        return (self.x >> 16) % n

    def uniforme(self) -> float:
        self.x = (1103515245 * self.x + 12345) % 2147483648
        return self.x / 2147483648.0


class CFR:
    """Minimização do arrependimento contrafactual (Zinkevich et al., 2007) para qualquer jogo
    com a interface acima: vanilla, com o acaso amostrado e com amostragem externa
    (Lanctot et al., 2009). `nos` conta as chamadas da recursão (a unidade de custo)."""

    def __init__(self, jogo):
        self.jogo = jogo
        self.arrependimento: dict[tuple, list[float]] = {}
        self.soma: dict[tuple, list[float]] = {}
        self.nos = 0

    def estrategia(self, k: tuple, n: int) -> list[float]:
        r = self.arrependimento.get(k)
        if r is None:
            return [1.0 / n] * n
        pos = [x if x > 0 else 0.0 for x in r]
        s = sum(pos)
        return [x / s for x in pos] if s > 0 else [1.0 / n] * n

    def _cfr(self, d: tuple, h: str, p1: float, p2: float) -> float:
        self.nos += 1
        g = self.jogo
        u = g.terminal(h, *d)
        if u is not None:
            return u
        j = g.jogador(h)
        acs = g.acoes(h)
        k = g.chave(h, *d)
        s = self.estrategia(k, len(acs))
        util = [0.0] * len(acs)
        no = 0.0
        for i, a in enumerate(acs):
            util[i] = (self._cfr(d, g.proximo(h, a), p1 * s[i], p2) if j == 0
                       else self._cfr(d, g.proximo(h, a), p1, p2 * s[i]))
            no += s[i] * util[i]
        sinal = 1.0 if j == 0 else -1.0
        adv, prop = (p2, p1) if j == 0 else (p1, p2)
        r = self.arrependimento.setdefault(k, [0.0] * len(acs))
        m = self.soma.setdefault(k, [0.0] * len(acs))
        for i in range(len(acs)):
            r[i] += adv * sinal * (util[i] - no)
            m[i] += prop * s[i]
        return no

    def _externo(self, d: tuple, h: str, viajante: int, rng: LCGPortavel) -> float:
        self.nos += 1
        g = self.jogo
        u = g.terminal(h, *d)
        if u is not None:
            return u if viajante == 0 else -u
        acs = g.acoes(h)
        k = g.chave(h, *d)
        s = self.estrategia(k, len(acs))
        if g.jogador(h) == viajante:
            util = [self._externo(d, g.proximo(h, a), viajante, rng) for a in acs]
            no = sum(x * y for x, y in zip(s, util))
            r = self.arrependimento.setdefault(k, [0.0] * len(acs))
            for i in range(len(acs)):
                r[i] += util[i] - no
            return no
        m = self.soma.setdefault(k, [0.0] * len(acs))
        for i in range(len(acs)):
            m[i] += s[i]
        x, acum, escolhida = rng.uniforme(), 0.0, acs[-1]
        for i, a in enumerate(acs):
            acum += s[i]
            if x < acum:
                escolhida = a
                break
        return self._externo(d, g.proximo(h, escolhida), viajante, rng)

    def vanilla(self, iteracoes: int) -> "CFR":
        for _ in range(iteracoes):
            for d in self.jogo.DISTRIBUICOES:
                self._cfr(d, "", 1.0, 1.0)
        return self

    def acaso_amostrado(self, iteracoes: int, semente: int) -> "CFR":
        rng = LCGPortavel(semente)
        n = len(self.jogo.DISTRIBUICOES)
        for _ in range(iteracoes):
            self._cfr(self.jogo.DISTRIBUICOES[rng.inteiro(n)], "", 1.0, 1.0)
        return self

    def amostragem_externa(self, iteracoes: int, semente: int) -> "CFR":
        rng = LCGPortavel(semente)
        n = len(self.jogo.DISTRIBUICOES)
        for _ in range(iteracoes):
            for viajante in (0, 1):
                self._externo(self.jogo.DISTRIBUICOES[rng.inteiro(n)], "", viajante, rng)
        return self

    def media(self) -> dict[tuple, list[float]]:
        out = {}
        for k, m in self.soma.items():
            s = sum(m)
            out[k] = [x / s for x in m] if s > 0 else [1.0 / len(m)] * len(m)
        return out


class AnaliseJogo:
    """Valor exato de um perfil e melhor resposta exata (conjunto por conjunto, do mais fundo ao mais raso)."""

    @staticmethod
    def _s(estr: dict, k: tuple, n: int) -> list[float]:
        return estr.get(k) or [1.0 / n] * n

    @staticmethod
    def valor(jogo, estr: dict) -> float:
        def v(d, h):
            u = jogo.terminal(h, *d)
            if u is not None:
                return u
            acs = jogo.acoes(h)
            s = AnaliseJogo._s(estr, jogo.chave(h, *d), len(acs))
            return sum(s[i] * v(d, jogo.proximo(h, a)) for i, a in enumerate(acs))
        return sum(v(d, "") for d in jogo.DISTRIBUICOES) / len(jogo.DISTRIBUICOES)

    @staticmethod
    def melhor_resposta(jogo, estr: dict, resp: int) -> float:
        entradas: dict[tuple, list] = {}

        def anda(d, h, alc):
            if jogo.terminal(h, *d) is not None:
                return
            acs = jogo.acoes(h)
            k = jogo.chave(h, *d)
            if jogo.jogador(h) == resp:
                entradas.setdefault(k, []).append((d, h, alc))
                for a in acs:
                    anda(d, jogo.proximo(h, a), alc)
            else:
                s = AnaliseJogo._s(estr, k, len(acs))
                for i, a in enumerate(acs):
                    if s[i] > 0:
                        anda(d, jogo.proximo(h, a), alc * s[i])
        for d in jogo.DISTRIBUICOES:
            anda(d, "", 1.0)
        escolha, memo = {}, {}
        sinal = 1.0 if resp == 0 else -1.0

        def v(d, h):
            chave_memo = (d, h)
            if chave_memo in memo:
                return memo[chave_memo]
            u = jogo.terminal(h, *d)
            if u is not None:
                return u
            acs = jogo.acoes(h)
            k = jogo.chave(h, *d)
            if jogo.jogador(h) == resp:
                x = v(d, jogo.proximo(h, escolha[k]))
            else:
                s = AnaliseJogo._s(estr, k, len(acs))
                x = sum(s[i] * v(d, jogo.proximo(h, a)) for i, a in enumerate(acs) if s[i] > 0)
            memo[chave_memo] = x
            return x
        for k in sorted(entradas, key=lambda k: -len(k[-1])):
            melhor, qual = None, None
            for a in jogo.acoes(k[-1]):
                tot = sum(alc * v(d, jogo.proximo(h, a)) for d, h, alc in entradas[k])
                if melhor is None or sinal * tot > sinal * melhor:
                    melhor, qual = tot, a
            escolha[k] = qual
        return sum(v(d, "") for d in jogo.DISTRIBUICOES) / len(jogo.DISTRIBUICOES)

    @staticmethod
    def explorabilidade(jogo, estr: dict) -> float:
        """Soma do que o perfil cede às duas melhores respostas; 0 só no equilíbrio de Nash."""
        return AnaliseJogo.melhor_resposta(jogo, estr, 0) - AnaliseJogo.melhor_resposta(jogo, estr, 1)

    @staticmethod
    def conjuntos(jogo) -> tuple[int, int]:
        vistos = (set(), set())

        def anda(d, h):
            if jogo.terminal(h, *d) is not None:
                return
            vistos[jogo.jogador(h)].add(jogo.chave(h, *d))
            for a in jogo.acoes(h):
                anda(d, jogo.proximo(h, a))
        for d in jogo.DISTRIBUICOES:
            anda(d, "")
        return len(vistos[0]), len(vistos[1])

    @staticmethod
    def estrategia_fixa_kuhn_2_2_0() -> dict[tuple, list[float]]:
        """A estratégia fixa de PokerKuhn.resultado_fixo (2.2.0) escrita como perfil: o 1 aposta com o rei
        e blefa com o valete 25%; o 2 paga só com o rei, e aposta (após passe) com o rei ou blefa 20% com o valete."""
        e = {}
        for c in range(3):
            aposta = 1.0 if c == 2 else (0.25 if c == 0 else 0.0)
            e[(c, "")] = [1 - aposta, aposta]
            e[(c, "pb")] = [0.0, 1.0] if c == 2 else [1.0, 0.0]
            e[(c, "b")] = [0.0, 1.0] if c == 2 else [1.0, 0.0]
            aposta2 = 1.0 if c == 2 else (0.20 if c == 0 else 0.0)
            e[(c, "p")] = [1 - aposta2, aposta2]
        return e


class Simplex:
    """Programação linear EXATA em frações (regra de Bland, sem ciclagem): max cᵀx, Ax ≤ b, x ≥ 0, b ≥ 0."""

    @staticmethod
    def maximizar(a: list[list], b: list, c: list) -> tuple[Any, list, list]:
        from fractions import Fraction as F
        m, n = len(a), len(c)
        t = [[F(x) for x in a[i]] + [F(int(i == j)) for j in range(m)] + [F(b[i])] for i in range(m)]
        z = [-F(x) for x in c] + [F(0)] * m + [F(0)]
        base = [n + i for i in range(m)]
        while True:
            entra = next((j for j in range(n + m) if z[j] < 0), None)
            if entra is None:
                break
            linhas = [(t[i][-1] / t[i][entra], base[i], i) for i in range(m) if t[i][entra] > 0]
            if not linhas:
                raise ValueError("Problema ilimitado")
            _, _, sai = min(linhas)
            piv = t[sai][entra]
            t[sai] = [x / piv for x in t[sai]]
            for i in range(m):
                if i != sai and t[i][entra] != 0:
                    f = t[i][entra]
                    t[i] = [x - f * y for x, y in zip(t[i], t[sai])]
            f = z[entra]
            z = [x - f * y for x, y in zip(z, t[sai])]
            base[sai] = entra
        x = [F(0)] * n
        for i, bi in enumerate(base):
            if bi < n:
                x[bi] = t[i][-1]
        dual = [z[n + i] for i in range(m)]
        return z[-1], x, dual

    @staticmethod
    def resolver_jogo(matriz: list[list]) -> dict[str, Any]:
        """Jogo de soma zero (linhas maximizam). Desloca a matriz para positiva, resolve o LP do jogador
        das colunas e lê as estratégias dos dois (primal e dual). Valor exato em frações."""
        from fractions import Fraction as F
        menor = min(min(l) for l in matriz)
        k = F(1) - F(menor) if menor <= 0 else F(0)
        a = [[F(x) + k for x in l] for l in matriz]
        m, n = len(a), len(a[0])
        opt, y, dual = Simplex.maximizar(a, [1] * m, [1] * n)
        valor = 1 / opt - k
        return dict(valor=valor, linhas=[d / opt for d in dual], colunas=[v / opt for v in y])

    @staticmethod
    def kuhn_forma_normal() -> list[list]:
        """A matriz 64 × 64 do Kuhn em estratégias puras (2⁶ por jogador), com valor esperado exato em frações."""
        from fractions import Fraction as F
        conj1 = [(c, h) for c in range(3) for h in ("", "pb")]
        conj2 = [(c, h) for c in range(3) for h in ("p", "b")]
        puras1 = list(itertools.product((0, 1), repeat=6))
        puras2 = list(itertools.product((0, 1), repeat=6))
        acao = JogoKuhn.acoes("")

        def jogar(e1, e2, d):
            h = ""
            while True:
                u = JogoKuhn.terminal(h, *d)
                if u is not None:
                    return F(int(u))
                j = JogoKuhn.jogador(h)
                k = JogoKuhn.chave(h, *d)
                escolha = e1[conj1.index(k)] if j == 0 else e2[conj2.index(k)]
                h += acao[escolha]
        return [[sum(jogar(e1, e2, d) for d in JogoKuhn.DISTRIBUICOES) / 6 for e2 in puras2] for e1 in puras1]


class VelhaAvancada:
    """Jogo da velha: poda alfa-beta, contagem por camadas (caminho independente do da 2.2.0) e um
    agente de Q-learning tabular treinado contra um adversário aleatório e avaliado em partidas novas."""

    @staticmethod
    def alfa_beta(t: str = "." * 9, j: str = "X", alfa: int = -2, beta: int = 2) -> int:
        v = vencedor_velha(t)
        if v:
            return 1 if v == j else -1
        if "." not in t:
            return 0
        outro = "O" if j == "X" else "X"
        melhor = -2
        for i, c in enumerate(t):
            if c == ".":
                x = -VelhaAvancada.alfa_beta(t[:i] + j + t[i + 1:], outro, -beta, -alfa)
                melhor = max(melhor, x)
                alfa = max(alfa, x)
                if alfa >= beta:
                    break
        return melhor

    @staticmethod
    def estados_por_camadas() -> int:
        camada, total = {"." * 9}, 1
        for k in range(9):
            j = "X" if k % 2 == 0 else "O"
            nova = set()
            for t in camada:
                if vencedor_velha(t) or "." not in t:
                    continue
                for i, c in enumerate(t):
                    if c == ".":
                        nova.add(t[:i] + j + t[i + 1:])
            total += len(nova)
            camada = nova
        return total

    @staticmethod
    def treinar_q(episodios: int, seed: int, alfa: float = 0.3, gama: float = 1.0,
                  epsilon: float = 0.2) -> dict[str, float]:
        """O agente joga de X contra O aleatório. Q[tabuleiro][casa]; recompensa só no fim (+1/0/−1)."""
        rng = random.Random(seed)
        q: dict[str, dict[int, float]] = collections.defaultdict(dict)

        def livres(t):
            return [i for i, c in enumerate(t) if c == "."]
        for _ in range(episodios):
            t = "." * 9
            while True:
                acs = livres(t)
                if rng.random() < epsilon:
                    a = rng.choice(acs)
                else:
                    a = max(acs, key=lambda i: q[t].get(i, 0.0))
                t2 = t[:a] + "X" + t[a + 1:]
                if vencedor_velha(t2) == "X" or "." not in t2:
                    r = 1.0 if vencedor_velha(t2) == "X" else 0.0
                    q[t][a] = q[t].get(a, 0.0) + alfa * (r - q[t].get(a, 0.0))
                    break
                o = rng.choice(livres(t2))
                t3 = t2[:o] + "O" + t2[o + 1:]
                if vencedor_velha(t3) == "O" or "." not in t3:
                    r = -1.0 if vencedor_velha(t3) == "O" else 0.0
                    q[t][a] = q[t].get(a, 0.0) + alfa * (r - q[t].get(a, 0.0))
                    break
                alvo = gama * max(q[t3].get(i, 0.0) for i in livres(t3))
                q[t][a] = q[t].get(a, 0.0) + alfa * (alvo - q[t].get(a, 0.0))
                t = t3
        return VelhaAvancada.avaliar(lambda t: max(livres(t), key=lambda i: q[t].get(i, 0.0)), 1000, seed + 1)

    @staticmethod
    def avaliar(politica, partidas: int, seed: int) -> dict[str, float]:
        """A política (de X) contra O aleatório em partidas novas: frações de vitória, empate e derrota."""
        rng = random.Random(seed)
        v = e = d = 0
        for _ in range(partidas):
            t = "." * 9
            while True:
                a = politica(t)
                t = t[:a] + "X" + t[a + 1:]
                if vencedor_velha(t) == "X":
                    v += 1
                    break
                if "." not in t:
                    e += 1
                    break
                livres = [i for i, c in enumerate(t) if c == "."]
                o = rng.choice(livres)
                t = t[:o] + "O" + t[o + 1:]
                if vencedor_velha(t) == "O":
                    d += 1
                    break
        return dict(vitorias=v / partidas, empates=e / partidas, derrotas=d / partidas)


# =============================================================================
# EXTENSÃO 3.0 — LÓGICA (FNC, TSEITIN, DPLL), CODIFICAÇÕES E EXPERIMENTOS CORRIGIDOS
# =============================================================================
# A 2.2.0 decide satisfatibilidade por força bruta (2ⁿ, até 16 variáveis). Aqui: conversão de
# Tseitin (fórmula → cláusulas, tamanho linear) e DPLL com propagação de unidade e literal puro,
# conferidos contra a tabela-verdade da 2.2.0 em fórmulas aleatórias.

class LogicaSAT:
    @staticmethod
    def tseitin(ast: tuple) -> tuple[list[list[int]], dict[str, int]]:
        """Cláusulas equi-satisfatíveis: cada subfórmula ganha uma variável nova; literal = ±índice."""
        nomes: dict[str, int] = {}
        clausulas: list[list[int]] = []
        contador = [0]

        def nova() -> int:
            contador[0] += 1
            return contador[0]

        def visita(no: tuple) -> int:
            op = no[0]
            if op == "var":
                if no[1] not in nomes:
                    nomes[no[1]] = nova()
                return nomes[no[1]]
            if op == "not":
                return -visita(no[1])
            a, b = visita(no[1]), visita(no[2])
            x = nova()
            if op == "and":
                clausulas.extend([[-x, a], [-x, b], [x, -a, -b]])
            elif op == "or":
                clausulas.extend([[-x, a, b], [x, -a], [x, -b]])
            elif op == "imp":
                clausulas.extend([[-x, -a, b], [x, a], [x, -b]])
            elif op == "iff":
                clausulas.extend([[-x, -a, b], [-x, a, -b], [x, a, b], [x, -a, -b]])
            else:
                raise ValueError("Operação lógica desconhecida")
            return x
        raiz = visita(ast)
        clausulas.append([raiz])
        return clausulas, nomes

    @staticmethod
    def dpll(clausulas: list[list[int]], limite_decisoes: int = 1_000_000) -> dict[str, Any]:
        """DPLL iterativo-recursivo com propagação de unidade e eliminação de literal puro."""
        estat = dict(decisoes=0, propagacoes=0)

        def simplificar(cls, lit):
            out = []
            for c in cls:
                if lit in c:
                    continue
                if -lit in c:
                    c = [x for x in c if x != -lit]
                    if not c:
                        return None
                out.append(c)
            return out

        def resolve(cls, atrib):
            while True:
                unit = next((c[0] for c in cls if len(c) == 1), None)
                if unit is None:
                    break
                estat["propagacoes"] += 1
                atrib[abs(unit)] = unit > 0
                cls = simplificar(cls, unit)
                if cls is None:
                    return None
            literais = {x for c in cls for x in c}
            for lit in [x for x in literais if -x not in literais]:
                atrib[abs(lit)] = lit > 0
                cls = simplificar(cls, lit)
            if not cls:
                return atrib
            estat["decisoes"] += 1
            if estat["decisoes"] > limite_decisoes:
                raise TimeoutError("Limite de decisões do DPLL")
            contagem = collections.Counter(abs(x) for c in cls for x in c)
            v = max(contagem, key=lambda k: (contagem[k], -k))
            for lit in (v, -v):
                c2 = simplificar(cls, lit)
                if c2 is not None:
                    a2 = dict(atrib)
                    a2[v] = lit > 0
                    r = resolve(c2, a2)
                    if r is not None:
                        return r
            return None
        r = resolve([list(c) for c in clausulas], {})
        return dict(satisfativel=r is not None, atribuicao=r or {}, **estat)

    @staticmethod
    def satisfativel(formulas: list[str]) -> dict[str, Any]:
        """Mesmo contrato da Logica.satisfativel da 2.2.0, sem o teto de 16 variáveis."""
        ast = Logica.analisar(formulas[0])
        for f in formulas[1:]:
            ast = ("and", ast, Logica.analisar(f))
        clausulas, nomes = LogicaSAT.tseitin(ast)
        r = LogicaSAT.dpll(clausulas)
        if not r["satisfativel"]:
            return dict(estado="CONTRADITORIO", variaveis=len(nomes), clausulas=len(clausulas))
        test = {n: r["atribuicao"].get(i, False) for n, i in nomes.items()}
        if not Logica.calcular(ast, test):
            raise AssertionError("Testemunha do DPLL não satisfaz a fórmula")
        return dict(estado="CONSISTENTE", testemunha=test, variaveis=len(nomes), clausulas=len(clausulas))

    @staticmethod
    def formula_aleatoria(rng: random.Random, nvar: int, profundidade: int) -> str:
        if profundidade == 0 or rng.random() < .25:
            v = f"x{rng.randrange(nvar)}"
            return ("!" + v) if rng.random() < .5 else v
        op = rng.choice(["&", "|", "->", "<->"])
        return f"({LogicaSAT.formula_aleatoria(rng, nvar, profundidade-1)} {op} " \
               f"{LogicaSAT.formula_aleatoria(rng, nvar, profundidade-1)})"

    @staticmethod
    def pombos(n: int) -> list[list[int]]:
        """Princípio da casa dos pombos: n+1 pombos em n casas (insatisfatível; difícil para resolução)."""
        var = lambda p, c: p * n + c + 1
        cls = [[var(p, c) for c in range(n)] for p in range(n + 1)]
        for c in range(n):
            for p in range(n + 1):
                for q in range(p + 1, n + 1):
                    cls.append([-var(p, c), -var(q, c)])
        return cls

    @staticmethod
    def k_sat_aleatorio(rng: random.Random, nvar: int, ncl: int, k: int = 3) -> list[list[int]]:
        return [[v * rng.choice((1, -1)) for v in rng.sample(range(1, nvar + 1), k)] for _ in range(ncl)]

    @staticmethod
    def transicao_3sat(nvar: int, razoes: list[float], instancias: int, seed: int) -> dict[float, float]:
        """Fração satisfatível do 3-SAT aleatório por razão cláusulas/variáveis (transição perto de 4,27)."""
        rng = random.Random(seed)
        out = {}
        for r in razoes:
            ok = sum(LogicaSAT.dpll(LogicaSAT.k_sat_aleatorio(rng, nvar, round(r * nvar)))["satisfativel"]
                     for _ in range(instancias))
            out[r] = ok / instancias
        return out


class CodificacaoNumerica:
    """Representações numéricas exatas de palavras (todas com ida e volta testadas)."""
    ALFABETO = "abcdefghijklmnopqrstuvwxyz"

    @staticmethod
    def base26_bijetiva(palavra: str) -> int:
        n = 0
        for c in palavra.lower():
            i = CodificacaoNumerica.ALFABETO.find(c)
            if i < 0:
                raise ValueError("Só letras a-z")
            n = n * 26 + i + 1
        return n

    @staticmethod
    def de_base26(n: int) -> str:
        if n < 0:
            raise ValueError("Inteiro não negativo")
        out = []
        while n:
            n, r = divmod(n - 1, 26)
            out.append(CodificacaoNumerica.ALFABETO[r])
        return "".join(reversed(out))

    @staticmethod
    def hamming74_codificar(nibble: int) -> int:
        """Código de Hamming (7,4): corrige 1 bit. Bits de paridade nas posições 1, 2 e 4."""
        d = [(nibble >> i) & 1 for i in range(4)]
        p1 = d[0] ^ d[1] ^ d[3]
        p2 = d[0] ^ d[2] ^ d[3]
        p3 = d[1] ^ d[2] ^ d[3]
        bits = [p1, p2, d[0], p3, d[1], d[2], d[3]]
        return sum(b << i for i, b in enumerate(bits))

    @staticmethod
    def hamming74_decodificar(palavra: int) -> tuple[int, int]:
        b = [(palavra >> i) & 1 for i in range(7)]
        s = (b[0] ^ b[2] ^ b[4] ^ b[6]) | ((b[1] ^ b[2] ^ b[5] ^ b[6]) << 1) | ((b[3] ^ b[4] ^ b[5] ^ b[6]) << 2)
        if s:
            b[s - 1] ^= 1
        return b[2] | (b[4] << 1) | (b[5] << 2) | (b[6] << 3), s

    @staticmethod
    def crc32(dados: bytes) -> int:
        """CRC-32 (polinômio refletido 0xEDB88320), conferido contra zlib.crc32 nos testes."""
        c = 0xFFFFFFFF
        for byte in dados:
            c ^= byte
            for _ in range(8):
                c = (c >> 1) ^ (0xEDB88320 if c & 1 else 0)
        return c ^ 0xFFFFFFFF

    @staticmethod
    def huffman(texto: str) -> dict[str, Any]:
        """Código de Huffman: comprimento médio entre H e H+1 bits por símbolo (Shannon)."""
        import heapq
        freq = collections.Counter(texto)
        if len(freq) == 1:
            codigos = {next(iter(freq)): "0"}
        else:
            heap = [(f, i, {s: ""}) for i, (s, f) in enumerate(sorted(freq.items()))]
            heapq.heapify(heap)
            k = len(heap)
            while len(heap) > 1:
                f1, _, a = heapq.heappop(heap)
                f2, _, b = heapq.heappop(heap)
                junto = {s: "0" + c for s, c in a.items()}
                junto.update({s: "1" + c for s, c in b.items()})
                heapq.heappush(heap, (f1 + f2, k, junto))
                k += 1
            codigos = heap[0][2]
        n = len(texto)
        media = sum(freq[s] * len(c) for s, c in codigos.items()) / n
        h = -sum(f / n * math.log2(f / n) for f in freq.values())
        bits = "".join(codigos[c] for c in texto)
        return dict(codigos=codigos, bits=bits, media=media, entropia=h)

    @staticmethod
    def huffman_decodificar(bits: str, codigos: dict[str, str]) -> str:
        inverso = {c: s for s, c in codigos.items()}
        out, atual = [], ""
        for b in bits:
            atual += b
            if atual in inverso:
                out.append(inverso[atual])
                atual = ""
        if atual:
            raise ValueError("Bits sobrando")
        return "".join(out)

    @staticmethod
    def lz78(texto: str) -> list[tuple[int, str]]:
        dic, out, w = {"": 0}, [], ""
        for c in texto:
            if w + c in dic:
                w += c
            else:
                out.append((dic[w], c))
                dic[w + c] = len(dic)
                w = ""
        if w:
            out.append((dic[w[:-1]], w[-1]))
        return out

    @staticmethod
    def lz78_decodificar(pares: list[tuple[int, str]]) -> str:
        dic, out = [""], []
        for i, c in pares:
            s = dic[i] + c
            out.append(s)
            dic.append(s)
        return "".join(out)


class ExperimentosCorrigidos:
    """Os experimentos da 2.2.0 refeitos com as correções medidas (Parte 121 da série SYNTHAI):
    o IC do bootstrap pelos quantis da contagem real de réplicas (o código antigo fixava os índices
    24 e 974 e quebrava com 500 réplicas); o qui-quadrado da Mega-Sena com o fator de correção do
    sorteio sem reposição e com p-valor; o veredito do H-M3 por seed E combinado; o H-M7 com o
    arrependimento medido pelas médias verdadeiras, em muitas sementes."""

    @staticmethod
    def megasena(n: int, seed: int, replicas: int = 1000) -> dict[str, Any]:
        rng = random.Random(seed)
        sorteios = [set(rng.sample(range(1, 61), 6)) for _ in range(n)]
        deltas = []
        for pos in range(100, n):
            passado = collections.Counter(x for s in sorteios[pos - 100:pos] for x in s)
            quentes = set(sorted(range(1, 61), key=lambda x: (-passado[x], x))[:6])
            aleatoria = set(rng.sample(range(1, 61), 6))
            deltas.append(len(quentes & sorteios[pos]) - len(aleatoria & sorteios[pos]))
        media, inf, sup = Estatistica.bootstrap_media(deltas, seed + 999, replicas)
        contagem = collections.Counter(x for s in sorteios for x in s)
        # Cada dezena: Binomial(n, 1/10), variância n·0,1·0,9; sem reposição dentro do sorteio as contagens se
        # correlacionam negativamente: Σ(c−e)²/e tem média 60·0,9 = 54 e se distribui como (54/59)·χ²₅₉.
        q = Estatistica.qui2_uniformidade([contagem[x] for x in range(1, 61)], 54 / 59)
        t = Estatistica.media_ic_t(deltas)
        return dict(sorteios=n, media_delta=media, ic95_bootstrap=[inf, sup], ic95_t=[t[1], t[2]],
                    qui2=q["estatistica"], qui2_esperado=54.0, fator=q["fator"], p_valor=q["p_valor"],
                    veredito="ACEITA" if inf > 0 else ("REJEITADA" if sup < 0 else "INCONCLUSIVA (inclui 0)"))

    @staticmethod
    def h_m3(n: int, seeds: list[int], replicas: int = 1000) -> dict[str, Any]:
        por_seed, ganhos = [], []
        for seed in seeds:
            rng = random.Random(seed)
            amostras = [rng.randrange(2) for _ in range(n)]
            amostras = [(x, int(rng.random() < (.15 if x == 0 else .85))) for x in amostras]
            treino, teste = amostras[:int(.6 * n)], amostras[int(.8 * n):]
            glob = BetaBernoulli()
            grupos = {0: BetaBernoulli(), 1: BetaBernoulli()}
            for x, y in treino:
                glob.observar(y)
                grupos[x].observar(y)
            d = [(glob.prever() - y) ** 2 - (grupos[x].prever() - y) ** 2 for x, y in teste]
            m, inf, sup = Estatistica.bootstrap_media(d, seed + 100, replicas)
            ganhos.extend(d)
            por_seed.append(dict(seed=seed, ganho=m, ic=[inf, sup], aceita=inf > 0))
        m, inf, sup = Estatistica.bootstrap_media(ganhos, 12345, replicas)
        return dict(por_seed=por_seed, aceitas=sum(r["aceita"] for r in por_seed), seeds=len(seeds),
                    ganho_combinado=m, ic95_combinado=[inf, sup],
                    veredito_combinado="ACEITA" if inf > 0 else "INCONCLUSIVA")

    @staticmethod
    def h_m7(seeds: int, passos: int = 1000) -> dict[str, Any]:
        """Os dois reforços da 2.2.0 em `seeds` sementes, com o arrependimento pelas médias verdadeiras
        (0,75 e 0,55): sem ruído de avaliação de 200 passos. Teste t pareado e de sinal."""
        arrep = {"ordinario": [], "extraordinario": []}
        travado = {"ordinario": 0, "extraordinario": 0}
        for s in range(seeds):
            for tipo in arrep:
                r = BandidoContextual.simular(s, tipo, passos)
                arrep[tipo].append(0.20 if r["acao_escolhida"] == 1.0 else 0.0)
                travado[tipo] += r["acao_escolhida"] == 1.0
        dif = [a - b for a, b in zip(arrep["ordinario"], arrep["extraordinario"])]
        return dict(seeds=seeds, trava_no_pior={k: v / seeds for k, v in travado.items()},
                    diferenca_media=statistics.fmean(dif),
                    t_pareado=Estatistica.t_pareado(arrep["ordinario"], arrep["extraordinario"]),
                    sinal=Estatistica.sinal(dif))


class TestesNexus(unittest.TestCase):
    """Testes independentes: sem serviços externos e sem downloads."""
    def test_codificacoes_ida_volta(self):
        for palavra in ("logic", "olá", "العربية", "π", "🧠", "", "a\x00b"):
            codigo = Codificador.codificar(palavra)
            self.assertEqual(Codificador.decodificar_hex(codigo["hexadecimal"]), palavra)
            self.assertEqual(Codificador.decodificar_bin(codigo["binario"]), palavra)
            self.assertEqual("".join(map(chr, codigo["unicode"])), palavra)

    def test_lingua_bijetiva_200_mil(self):
        for valor in range(200_000):
            self.assertEqual(LinguaArtificial.decodificar(LinguaArtificial.codificar(valor)), valor)

    def test_geometria_e_identidade(self):
        self.assertLess(Geometria.erro_angulo_duplo(), 1e-12)
        self.assertAlmostEqual(Geometria.cosseno([3,4], [3,4]), 1.)
        self.assertAlmostEqual(Geometria.distancia([1,2], [4,6]), 5.)
        self.assertAlmostEqual(Geometria.projecao([3,4],[1,0])[0], 3.)

    def test_dinamica_nao_linear(self):
        self.assertLess(abs(Geometria.lyapunov_logistico(4.)-math.log(2)), .025)
        self.assertLess(Geometria.lyapunov_logistico(3.2), -.2)

    def test_logica(self):
        casos = ((["A -> B", "B -> C", "A", "!C"], "CONTRADITORIO"),
                 (["A -> B", "!B"], "CONSISTENTE"),
                 (["L <-> !L"], "CONTRADITORIO"),
                 (["B <-> !B"], "CONTRADITORIO"))
        for formulas, esperado in casos:
            self.assertEqual(Logica.satisfativel(formulas)["estado"], esperado)
        self.assertEqual(len(Logica.nucleo_inconsistente(["A","!A","C"])), 2)

    def test_probabilidade(self):
        estimador = BetaBernoulli()
        for acerto in [1]*7+[0]*3: estimador.observar(acerto)
        self.assertAlmostEqual(estimador.prever(), 8/12)
        self.assertEqual(Decisor.escolher(.6), 1)
        self.assertGreater(AvaliadorProbabilistico.pontuar([.5,.5],[0,1])["brier"], 0)

    def test_jogos(self):
        self.assertEqual(valor_velha("."*9), 0)
        self.assertEqual(contar_estados_velha(), 5478)
        self.assertEqual(PokerKuhn.premio((2,0), "bc"), 2)
        self.assertEqual(PokerKuhn.premio((0,2), "bf"), 1)
        self.assertEqual(PokerKuhn.premio((0,2), "kbf"), -1)

    def test_gradiente_diferencas_finitas(self):
        dados = [([.3,.2],1), ([-.5,.4],0), ([.7,-.3],1)]
        modelo = RegressaoLogistica(2)
        modelo.pesos = [.1,.4,-.3]
        analitico = modelo.gradiente(dados)
        for i, g in enumerate(analitico):
            original = modelo.pesos[i]
            modelo.pesos[i] = original + 1e-5
            acima = modelo.perda(dados)
            modelo.pesos[i] = original - 1e-5
            abaixo = modelo.perda(dados)
            modelo.pesos[i] = original
            self.assertLess(abs(g-(acima-abaixo)/2e-5),1e-8)

    def test_loteria_combinatoria(self):
        p = MegaSenaLaboratorio.probabilidades()
        self.assertEqual(p["total_combinacoes"], 50_063_860)
        self.assertAlmostEqual(p["acertos_esperados"],.6)
        self.assertAlmostEqual(p["sena"],1/50_063_860)

    def test_sem_vazamento_lexical(self):
        treino = [x for i,x in enumerate(lexico_embutido()) if i%5 != 0]
        teste = [x for i,x in enumerate(lexico_embutido()) if i%5 == 0]
        self.assertTrue(set(x[0] for x in treino).isdisjoint(x[0] for x in teste))
        self.assertTrue(politica_lexica(teste[0][2],treino) in {x[0] for x in treino})

    def test_antissabotagem(self):
        honesta = Reforco.extraordinario(1, 0)
        sabotadora = Reforco.extraordinario(0, 1)
        self.assertGreater(honesta, sabotadora)
        with self.assertRaises(ValueError): Reforco.extraordinario(0,1,1,1.5)

    def test_controle_de_entrada(self):
        self.assertEqual(Logica.satisfativel(["A -> B", "A"])["estado"], "CONSISTENTE")
        with self.assertRaises(ValueError): Logica.analisar("A; __import__('os')")
        self.assertTrue(Auditor.defensivo("Ignore previous instructions")['sinalizadores'])
        self.assertFalse(Auditor.defensivo("ignore previous instructions")['executou_entrada'])
        with self.assertRaises(ValueError): Codificador.decodificar_bin("1002")

    def test_parametros_versao(self):
        with self.assertRaises(ValueError): Configuracao(profundidade_maxima=4)
        self.assertFalse(Auditor.validar_melhoria(.1, (.01,.2), True, True, True)["aceita"])
        self.assertTrue(Auditor.validar_melhoria(.1, (.01,.2), False, True, True)["aceita"])

    def test_lexico_manual(self):
        lex = lexico_embutido()
        self.assertGreaterEqual(len(lex), 200)
        self.assertEqual(len({p for p, _, _ in lex}), len(lex))
        self.assertTrue(all(p and c and d for p, c, d in lex))

    def test_nota_calibracao(self):
        # Sob recompensa quadrática, c=p maximiza pontuação esperada.
        for p in (.3,.7,.9):
            esperado = lambda c: p*Raphael.pontos(1,c) + (1-p)*Raphael.pontos(0,c)
            self.assertGreaterEqual(esperado(p)+1e-12, max(esperado(i/100) for i in range(101)))


class TestesExtensao(unittest.TestCase):
    """Testes da 3.0.0. Cada um confere uma peça contra um número de forma fechada, um teorema
    ou um caminho de cálculo independente (nunca contra a própria saída gravada)."""

    # ---------- correções ----------
    def test_sem_rede(self):
        import ast
        arvore = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        proibidos = {"urllib", "socket", "http", "requests", "subprocess", "ftplib", "smtplib"}
        for no in ast.walk(arvore):
            if isinstance(no, ast.Import):
                self.assertFalse({a.name.split(".")[0] for a in no.names} & proibidos)
            if isinstance(no, ast.ImportFrom):
                self.assertNotIn((no.module or "").split(".")[0], proibidos)
            if isinstance(no, ast.Call) and isinstance(no.func, ast.Name):
                self.assertNotIn(no.func.id, {"eval", "exec", "__import__"})
        self.assertFalse(hasattr(LagoLexical, "_consultar_api"))

    def test_rede_recusada(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            repo = Repositorio(Configuracao(raiz=d))
            with self.assertRaises(ValueError):
                LagoLexical(repo, permitir_rede=True)

    def test_bootstrap_qualquer_numero_de_replicas(self):
        # Na 2.2.0, replicas[974] estourava com 500 réplicas.
        dados = [float(i % 7) for i in range(50)]
        for r in (10, 500, 1000, 2000):
            m, inf, sup = AvaliadorProbabilistico.bootstrap_ganho(dados, [0.0] * 50, 3, r)
            self.assertLessEqual(inf, m)
            self.assertLessEqual(m, sup)
        m, inf, sup = Estatistica.bootstrap_media(dados, 1, 500)
        self.assertLess(inf, m)
        self.assertLess(m, sup)

    def test_quantil_tipo7(self):
        self.assertEqual(Estatistica.quantil([1, 2, 3, 4], 0.5), 2.5)
        self.assertEqual(Estatistica.quantil([5], 0.9), 5)
        self.assertAlmostEqual(Estatistica.quantil(list(range(101)), 0.025), 2.5)

    def test_qui2_megasena_fator(self):
        # Simulação independente da média de Σ(c−e)²/e: o fator 54/59 vem de 60·(1 − 6/60).
        rng = random.Random(11)
        valores = []
        for _ in range(300):
            c = collections.Counter(x for _ in range(200) for x in rng.sample(range(1, 61), 6))
            valores.append(sum((c[x] - 20) ** 2 / 20 for x in range(1, 61)))
        m = statistics.fmean(valores)
        dp = statistics.stdev(valores) / math.sqrt(len(valores))
        self.assertLess(abs(m - 54) / dp, 3.5)
        self.assertGreater(abs(m - 59) / dp, 3.5)

    def test_megasena_corrigida(self):
        r = ExperimentosCorrigidos.megasena(1200, 42, 500)
        self.assertTrue(0 < r["p_valor"] < 1)
        self.assertLessEqual(r["ic95_bootstrap"][0], r["media_delta"])
        self.assertLessEqual(r["media_delta"], r["ic95_bootstrap"][1])
        self.assertTrue(r["ic95_bootstrap"][0] < 0 < r["ic95_bootstrap"][1])
        self.assertTrue(r["veredito"].startswith("INCONCLUSIVA"))

    def test_beta_intervalo_exato(self):
        b = BetaBernoulli()
        b.observar(1)
        b.observar(1)
        lo, hi = b.intervalo_exato()
        # Beta(3,1): F(x) = x³, logo os quantis são 0,025^(1/3) e 0,975^(1/3).
        self.assertAlmostEqual(lo, 0.025 ** (1 / 3), places=9)
        self.assertAlmostEqual(hi, 0.975 ** (1 / 3), places=9)
        self.assertLess(hi, 1.0)

    def test_h_m3_combinado(self):
        r = ExperimentosCorrigidos.h_m3(1500, [0, 1, 2], 300)
        self.assertEqual(r["seeds"], 3)
        lo, hi = r["ic95_combinado"]
        self.assertTrue(lo < r["ganho_combinado"] < hi)
        # Ganho de Brier teórico: Var global − Var condicional = 0,25 − 0,1275 = 0,1225.
        self.assertTrue(lo < 0.1225 < hi + 0.01)

    def test_h_m7_muitas_sementes(self):
        r = ExperimentosCorrigidos.h_m7(60)
        self.assertEqual(r["seeds"], 60)
        self.assertGreater(r["t_pareado"]["p_bilateral"], 0.01)

    # ---------- estatística ----------
    def test_distribuicoes(self):
        self.assertAlmostEqual(Estatistica.qui2_sf(3.841458820694124, 1), 0.05, places=10)
        self.assertAlmostEqual(Estatistica.t_quantil(0.975, 10), 2.2281388519649, places=8)
        self.assertAlmostEqual(Estatistica.normal_quantil(0.975), 1.959963984540054, places=9)
        self.assertAlmostEqual(Estatistica.gama_inferior_regularizada(1, 2), 1 - math.exp(-2), places=12)
        # Beta(2,5) em 0,3: I = Σ_{j=2}^{6} C(6,j) 0,3^j 0,7^(6−j).
        exato = sum(math.comb(6, j) * .3 ** j * .7 ** (6 - j) for j in range(2, 7))
        self.assertAlmostEqual(Estatistica.beta_regularizada(.3, 2, 5), exato, places=12)
        self.assertAlmostEqual(Estatistica.t_cdf(0.0, 7), 0.5, places=12)

    def test_intervalos_binomiais(self):
        lo, hi = Estatistica.clopper_pearson(0, 10)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 1 - 0.025 ** 0.1, places=9)
        lo, hi = Estatistica.wilson(7, 10)
        self.assertTrue(lo < 0.7 < hi)
        lo2, hi2 = Estatistica.clopper_pearson(7, 10)
        self.assertLess(lo2, lo)  # o exato é conservador
        self.assertGreater(hi2, hi)

    def test_testes_de_hipotese(self):
        self.assertEqual(Estatistica.binomial_exato(5, 10), 1.0)
        self.assertAlmostEqual(Estatistica.binomial_exato(0, 10), 2 / 1024)
        r = Estatistica.t_pareado([1, 2, 3, 4], [0, 1, 2, 3.5])
        self.assertAlmostEqual(r["media"], 0.875)
        self.assertEqual(Estatistica.holm({"a": .01, "b": .04, "c": .03}), {"a": True, "c": False, "b": False})
        # Doze diferenças iguais: só os 2 sinais uniformes de 2¹² empatam com o observado (p exato 1/2048).
        p = Estatistica.permutacao_pareada([1.0] * 12, [0.0] * 12, 2, 2000)
        self.assertLess(p, 0.01)
        self.assertEqual(Estatistica.sinal([1, -1, 0, 2])["empates"], 1)
        q = Estatistica.qui2_uniformidade([10, 10, 10, 10])
        self.assertEqual(q["estatistica"], 0.0)
        self.assertAlmostEqual(q["p_valor"], 1.0)

    # ---------- álgebra linear ----------
    def test_algebra(self):
        a = [[2, 1, 0], [1, 3, 1], [0, 1, 4]]
        self.assertAlmostEqual(AlgebraLinear.determinante(a), 18.0)
        inv = AlgebraLinear.inversa(a)
        prod = AlgebraLinear.produto(a, inv)
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(prod[i][j], float(i == j), places=12)
        x = AlgebraLinear.resolver(a, [1, 2, 3])
        self.assertTrue(all(abs(u - v) < 1e-12 for u, v in zip(AlgebraLinear.aplicar(a, x), [1, 2, 3])))
        coef = AlgebraLinear.minimos_quadrados([[1, t] for t in range(5)], [1 + 2 * t for t in range(5)])
        self.assertAlmostEqual(coef[0], 1.0)
        self.assertAlmostEqual(coef[1], 2.0)
        ridge = AlgebraLinear.minimos_quadrados([[1, t] for t in range(5)], [1 + 2 * t for t in range(5)], 10.0)
        self.assertLess(abs(ridge[1]), 2.0)

    def test_autovalores(self):
        valores, _ = AlgebraLinear.jacobi([[2, 1], [1, 2]])
        self.assertEqual([round(v, 12) for v in sorted(valores)], [1.0, 3.0])
        self.assertAlmostEqual(AlgebraLinear.potencia([[2, 1], [1, 2]])[0], 3.0)
        # [[3,0],[4,5]]: AᵀA = [[25,20],[20,25]], autovalores 45 e 5.
        sv = AlgebraLinear.valores_singulares([[3, 0], [4, 5]])
        self.assertAlmostEqual(sv[0], math.sqrt(45))
        self.assertAlmostEqual(sv[1], math.sqrt(5))
        q, r = AlgebraLinear.gram_schmidt([[1, 1], [1, 0], [0, 1]])
        qtq = AlgebraLinear.produto(AlgebraLinear.transposta(q), q)
        self.assertAlmostEqual(qtq[0][1], 0.0)
        self.assertAlmostEqual(qtq[1][1], 1.0)

    def test_pca(self):
        rng = random.Random(4)
        dados = []
        for _ in range(400):
            t = rng.gauss(0, 3)
            dados.append([t, 2 * t + rng.gauss(0, .1), rng.gauss(0, .1)])
        r = AlgebraLinear.componentes_principais(dados, 1)
        self.assertGreater(r["fracao_explicada"], 0.99)
        d = r["direcoes"][0]
        self.assertAlmostEqual(abs(d[1] / d[0]), 2.0, places=2)

    # ---------- calibração, bandidos, informação, texto, dinâmica ----------
    def test_calibracao(self):
        r = Calibracao.experimento()
        self.assertLess(r["ece_isotonica"], r["ece_antes"] / 3)
        self.assertLess(r["ece_platt"], r["ece_antes"] / 3)
        self.assertLess(r["brier_isotonica"], r["brier_antes"])
        degraus = Calibracao.isotonica([.1, .2, .3, .4], [0, 1, 0, 1])
        valores = [v for _, v in degraus]
        self.assertEqual(valores, sorted(valores))

    def test_bandidos(self):
        r = Bandidos.comparar(sementes=range(12), passos=1500)
        m = r["medias_arrependimento"]
        self.assertLess(m["thompson"], m["epsilon"])
        self.assertLess(m["thompson"], m["ucb1"])
        # c = Σ Δ/KL para (0,75; 0,55; 0,50): conta de Lai–Robbins.
        kl = lambda p, q: p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))
        self.assertAlmostEqual(Bandidos.lai_robbins([.75, .55, .5]), .2 / kl(.55, .75) + .25 / kl(.5, .75))

    def test_informacao(self):
        self.assertAlmostEqual(Informacao.entropia([.5, .5]), 1.0)
        self.assertAlmostEqual(Informacao.kl([.3, .7], [.3, .7]), 0.0)
        self.assertGreater(Informacao.kl([.3, .7], [.5, .5]), 0)
        self.assertEqual(Informacao.levenshtein("kitten", "sitting"), 3)
        pares = [(i % 2, i % 2) for i in range(100)]
        self.assertAlmostEqual(Informacao.informacao_mutua(pares), 1.0)
        self.assertAlmostEqual(Informacao.informacao_mutua([(i % 2, i // 2 % 2) for i in range(100)]), 0.0, places=2)
        self.assertEqual(Informacao.jaccard({1, 2}, {2, 3}), 1 / 3)

    def test_modelo_de_caracteres(self):
        texto = " ".join(d for _, _, d in lexico_embutido())
        corte = len(texto) * 4 // 5
        m = ModeloCaracteres(3).treinar(texto[:corte])
        bpc = m.bits_por_caractere(texto[corte:])
        self.assertLess(bpc, math.log2(len(set(texto))) - 1)  # aprende alguma coisa fora da amostra
        self.assertGreater(bpc, 1.0)
        # A uniforme da base reparte a massa entre o alfabeto e UM símbolo não visto: soma exata 1.
        self.assertNotIn("\x00", m.alfabeto)
        self.assertAlmostEqual(sum(m.prob("the", c) for c in m.alfabeto) + m.prob("the", "\x00"), 1.0, places=12)
        self.assertEqual(len(m.gerar(50, 1)), 50)

    def test_dinamica(self):
        x = Dinamica.rk4(lambda v: [-v[0]], [1.0], 0.01, 100)[-1][0]
        self.assertLess(abs(x - math.exp(-1)), 1e-9)
        self.assertEqual([Dinamica.periodo_logistico(r) for r in (2.8, 3.2, 3.5, 3.55)], [1, 2, 4, 8])
        self.assertIsNone(Dinamica.periodo_logistico(3.9))
        dobras = Dinamica.feigenbaum()
        self.assertAlmostEqual(dobras[0], 3.0, places=2)
        self.assertAlmostEqual(dobras[1], 1 + math.sqrt(6), places=2)
        self.assertTrue(4.3 < (dobras[1] - dobras[0]) / (dobras[2] - dobras[1]) < 5.0)
        lam = Dinamica.lyapunov_benettin(Dinamica.lorenz(), [1.0, 1.0, 1.0], passos=5000)
        self.assertTrue(0.75 < lam < 1.05)  # literatura: 0,9056

    # ---------- jogos ----------
    def test_regras_kuhn_e_leduc(self):
        self.assertEqual(AnaliseJogo.conjuntos(JogoKuhn), (6, 6))
        self.assertEqual(AnaliseJogo.conjuntos(JogoLeduc), (144, 144))
        self.assertEqual(len(JogoLeduc.DISTRIBUICOES), 120)
        self.assertEqual(JogoLeduc.terminal("rf", 0, 1, 2), 1.0)
        self.assertEqual(JogoLeduc.terminal("cc/rc", 0, 1, 0), 5.0)  # o jogador 1 pareou com a pública
        self.assertEqual(JogoLeduc.terminal("cc/cc", 1, 1, 0), 0.0)
        self.assertEqual(JogoLeduc.contribuicoes("rrc/rrc"), [13, 13])  # 1 + 2 + 2 + 4 + 4
        for c in range(3):
            for d in range(3):
                if c != d:
                    self.assertEqual(JogoKuhn.terminal("pbb", c, d), PokerKuhn.premio((c, d), "kbc"))

    def test_kuhn_cfr_equilibrio(self):
        cfr = CFR(JogoKuhn).vanilla(2000)
        perfil = cfr.media()
        self.assertLess(abs(AnaliseJogo.valor(JogoKuhn, perfil) + 1 / 18), 2e-3)
        self.assertLess(AnaliseJogo.explorabilidade(JogoKuhn, perfil), 0.02)
        # Jogador 2 único em Kuhn: com a dama paga 1/3 da aposta; com o valete blefa 1/3 após passe.
        self.assertAlmostEqual(perfil[(1, "b")][1], 1 / 3, delta=0.03)
        self.assertAlmostEqual(perfil[(0, "p")][1], 1 / 3, delta=0.03)

    def test_kuhn_mccfr(self):
        externo = CFR(JogoKuhn).amostragem_externa(20000, 1)
        acaso = CFR(JogoKuhn).acaso_amostrado(20000, 1)
        self.assertLess(AnaliseJogo.explorabilidade(JogoKuhn, externo.media()), 0.03)
        self.assertLess(AnaliseJogo.explorabilidade(JogoKuhn, acaso.media()), 0.03)
        self.assertEqual(acaso.nos, 20000 * 9)  # 9 nós por árvore de uma distribuição

    def test_estrategia_fixa_2_2_0_e_exploravel(self):
        fixa = AnaliseJogo.estrategia_fixa_kuhn_2_2_0()
        self.assertGreater(AnaliseJogo.explorabilidade(JogoKuhn, fixa), 0.3)
        self.assertAlmostEqual(AnaliseJogo.explorabilidade(JogoKuhn, {}), 11 / 12)

    def test_simplex(self):
        r = Simplex.resolver_jogo([[1, -1], [-2, 3]])
        from fractions import Fraction as F
        self.assertEqual(r["valor"], F(1, 7))
        self.assertEqual(r["linhas"], [F(5, 7), F(2, 7)])
        self.assertEqual(r["colunas"], [F(4, 7), F(3, 7)])
        valor, x, _ = Simplex.maximizar([[1, 1], [1, 3]], [4, 6], [3, 2])
        self.assertEqual((valor, x), (F(12), [F(4), F(0)]))
        self.assertEqual(Simplex.resolver_jogo(Simplex.kuhn_forma_normal())["valor"], F(-1, 18))

    def test_leduc_cfr_melhora(self):
        uniforme = AnaliseJogo.explorabilidade(JogoLeduc, {})
        cfr = CFR(JogoLeduc).vanilla(20)
        depois = AnaliseJogo.explorabilidade(JogoLeduc, cfr.media())
        self.assertLess(depois, uniforme / 5)
        self.assertEqual(cfr.nos, 20 * 10200)

    def test_velha(self):
        self.assertEqual(VelhaAvancada.alfa_beta(), valor_velha("." * 9))
        self.assertEqual(VelhaAvancada.estados_por_camadas(), contar_estados_velha())
        aprendida = VelhaAvancada.treinar_q(20000, 3)
        livres = lambda t: [i for i, c in enumerate(t) if c == "."]
        rng = random.Random(9)
        aleatoria = VelhaAvancada.avaliar(lambda t: rng.choice(livres(t)), 1000, 4)
        self.assertGreater(aprendida["vitorias"], aleatoria["vitorias"] + 0.15)
        self.assertLess(aprendida["derrotas"], 0.05)

    # ---------- lógica e codificação ----------
    def test_dpll_concorda_com_tabela_verdade(self):
        rng = random.Random(5)
        contagem = collections.Counter()
        for _ in range(150):
            fs = [LogicaSAT.formula_aleatoria(rng, 4, 3) for _ in range(3)]
            a = Logica.satisfativel(fs)["estado"]
            self.assertEqual(LogicaSAT.satisfativel(fs)["estado"], a)
            contagem[a] += 1
        self.assertGreater(contagem["CONSISTENTE"], 10)
        self.assertGreater(contagem["CONTRADITORIO"], 10)

    def test_sat_alem_de_16_variaveis(self):
        cadeia = " & ".join(f"(x{i} -> x{i + 1})" for i in range(40))
        self.assertEqual(Logica.satisfativel([cadeia, "x0"])["estado"], "INCONCLUSIVO")
        self.assertEqual(LogicaSAT.satisfativel([cadeia, "x0"])["estado"], "CONSISTENTE")
        self.assertEqual(LogicaSAT.satisfativel([cadeia, "x0", "!x40"])["estado"], "CONTRADITORIO")
        for n in (3, 4, 5):
            self.assertFalse(LogicaSAT.dpll(LogicaSAT.pombos(n))["satisfativel"])
        self.assertTrue(LogicaSAT.dpll([[1, 2], [-1, 2], [-2, 3]])["satisfativel"])

    def test_transicao_3sat(self):
        r = LogicaSAT.transicao_3sat(25, [2.0, 8.0], 20, 1)
        self.assertEqual(r[2.0], 1.0)
        self.assertEqual(r[8.0], 0.0)

    def test_codificacoes_numericas(self):
        import zlib
        for palavra in ("a", "z", "aa", "logic", "zz", "dictionary"):
            self.assertEqual(CodificacaoNumerica.de_base26(CodificacaoNumerica.base26_bijetiva(palavra)), palavra)
        self.assertEqual(CodificacaoNumerica.base26_bijetiva("aa"), 27)
        self.assertEqual([CodificacaoNumerica.de_base26(n) for n in range(1, 30)],
                         sorted([CodificacaoNumerica.de_base26(n) for n in range(1, 30)], key=lambda s: (len(s), s)))
        for dados in (b"", b"123456789", "olá".encode()):
            self.assertEqual(CodificacaoNumerica.crc32(dados), zlib.crc32(dados))

    def test_hamming_corrige_um_bit(self):
        for n in range(16):
            w = CodificacaoNumerica.hamming74_codificar(n)
            self.assertEqual(CodificacaoNumerica.hamming74_decodificar(w), (n, 0))
            for b in range(7):
                self.assertEqual(CodificacaoNumerica.hamming74_decodificar(w ^ (1 << b)), (n, b + 1))

    def test_compressao(self):
        texto = " ".join(d for _, _, d in lexico_embutido())
        h = CodificacaoNumerica.huffman(texto)
        self.assertTrue(h["entropia"] <= h["media"] < h["entropia"] + 1)
        self.assertEqual(CodificacaoNumerica.huffman_decodificar(h["bits"], h["codigos"]), texto)
        pares = CodificacaoNumerica.lz78(texto)
        self.assertEqual(CodificacaoNumerica.lz78_decodificar(pares), texto)
        self.assertLess(len(pares), len(texto) / 3)


def _cmd_kuhn(modo: str) -> dict[str, Any]:
    n = {"rapido": 2000, "padrao": 10000, "intensivo": 50000}[modo]
    from fractions import Fraction as F
    saida = dict(versao=VERSAO, valor_exato_simplex=str(Simplex.resolver_jogo(Simplex.kuhn_forma_normal())["valor"]),
                 explorabilidade_estrategia_2_2_0=AnaliseJogo.explorabilidade(JogoKuhn, AnaliseJogo.estrategia_fixa_kuhn_2_2_0()))
    for nome, cfr in (("vanilla", CFR(JogoKuhn).vanilla(n)),
                      ("acaso", CFR(JogoKuhn).acaso_amostrado(n * 6, 1)),
                      ("externo", CFR(JogoKuhn).amostragem_externa(n * 3, 1))):
        p = cfr.media()
        saida[nome] = dict(nos=cfr.nos, valor=AnaliseJogo.valor(JogoKuhn, p),
                           explorabilidade=AnaliseJogo.explorabilidade(JogoKuhn, p),
                           dama_paga=p[(1, "b")][1], valete_blefa=p[(0, "p")][1])
    saida["valor_teorico"] = float(F(-1, 18))
    saida["rotulo"] = "[MEDIDO]"
    return saida


def _cmd_leduc(modo: str) -> dict[str, Any]:
    n = {"rapido": 30, "padrao": 200, "intensivo": 1000}[modo]
    cfr = CFR(JogoLeduc).vanilla(n)
    p = cfr.media()
    return dict(versao=VERSAO, iteracoes=n, nos=cfr.nos, conjuntos=AnaliseJogo.conjuntos(JogoLeduc),
                explorabilidade_uniforme=AnaliseJogo.explorabilidade(JogoLeduc, {}),
                explorabilidade=AnaliseJogo.explorabilidade(JogoLeduc, p),
                valor_jogador_1=AnaliseJogo.valor(JogoLeduc, p), rotulo="[MEDIDO]")


def _cmd_velha(modo: str) -> dict[str, Any]:
    n = {"rapido": 20000, "padrao": 100000, "intensivo": 400000}[modo]
    return dict(versao=VERSAO, valor_alfa_beta=VelhaAvancada.alfa_beta(),
                estados=VelhaAvancada.estados_por_camadas(), q_learning=VelhaAvancada.treinar_q(n, 3),
                rotulo="[MEDIDO]")


def _cmd_sat(modo: str) -> dict[str, Any]:
    nvar = {"rapido": 25, "padrao": 40, "intensivo": 60}[modo]
    razoes = [2.0, 3.0, 3.5, 4.0, 4.27, 4.5, 5.0, 6.0, 8.0]
    pombos = {n: LogicaSAT.dpll(LogicaSAT.pombos(n))["decisoes"] for n in range(2, 7)}
    return dict(versao=VERSAO, variaveis=nvar, fracao_satisfativel=LogicaSAT.transicao_3sat(nvar, razoes, 30, 1),
                decisoes_casa_dos_pombos=pombos, rotulo="[MEDIDO]")


def _cmd_calibracao(modo: str) -> dict[str, Any]:
    return dict(versao=VERSAO, **Calibracao.experimento(n={"rapido": 3000, "padrao": 20000, "intensivo": 100000}[modo]))


def _cmd_bandidos(modo: str) -> dict[str, Any]:
    s = {"rapido": 30, "padrao": 100, "intensivo": 300}[modo]
    r = Bandidos.comparar(sementes=range(s))
    r["lai_robbins_c"] = Bandidos.lai_robbins([.75, .55, .5])
    r["cota_assintotica_2000"] = r["lai_robbins_c"] * math.log(2000)
    return dict(versao=VERSAO, **r)


def _cmd_megasena3(modo: str) -> dict[str, Any]:
    n = {"rapido": 1200, "padrao": 2900, "intensivo": 10000}[modo]
    return dict(versao=VERSAO, origem="[SINTÉTICO]", **ExperimentosCorrigidos.megasena(n, 42, 2000),
                h_m3=ExperimentosCorrigidos.h_m3(1500, list(range(5))),
                h_m7=ExperimentosCorrigidos.h_m7({"rapido": 200, "padrao": 1000, "intensivo": 5000}[modo]))


def _cmd_caos(modo: str) -> dict[str, Any]:
    passos = {"rapido": 5000, "padrao": 20000, "intensivo": 100000}[modo]
    dobras = Dinamica.feigenbaum()
    razoes = [(dobras[i + 1] - dobras[i]) / (dobras[i + 2] - dobras[i + 1]) for i in range(len(dobras) - 2)]
    return dict(versao=VERSAO, lyapunov_lorenz=Dinamica.lyapunov_benettin(Dinamica.lorenz(), [1.0, 1.0, 1.0], passos=passos),
                lyapunov_logistico_r4=Geometria.lyapunov_logistico(4.0), ln2=math.log(2),
                dobras_de_periodo=dobras, razoes_feigenbaum=razoes, rotulo="[MEDIDO]")


COMANDOS_3 = dict(kuhn=_cmd_kuhn, leduc=_cmd_leduc, velha=_cmd_velha, sat=_cmd_sat, calibracao=_cmd_calibracao,
                  bandidos=_cmd_bandidos, megasena3=_cmd_megasena3, caos=_cmd_caos)


def executar_testes() -> dict[str, Any]:
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(TestesNexus),
                                unittest.defaultTestLoader.loadTestsFromTestCase(TestesExtensao)])
    inicio = time.perf_counter()
    import io
    fluxo = io.StringIO()
    resultado = unittest.TextTestRunner(stream=fluxo, verbosity=2).run(suite)
    return dict(versao=VERSAO, testes_executados=resultado.testsRun,
                falhas=len(resultado.failures), erros=len(resultado.errors),
                aprovados=resultado.testsRun-len(resultado.failures)-len(resultado.errors),
                sucesso=resultado.wasSuccessful(), duracao_s=round(time.perf_counter()-inicio, 5),
                detalhe=fluxo.getvalue(), rotulo="[MEDIDO]")


def inventario() -> dict[str, Any]:
    import importlib.util
    import platform
    modulos = ("numpy", "scipy", "sklearn", "torch", "nltk", "chess", "pytest", "requests", "yfinance")
    return dict(python=sys.version.split()[0], plataforma=platform.platform(),
                bibliotecas={p: bool(importlib.util.find_spec(p)) for p in modulos},
                rede_no_codigo="ausente (sem urllib/socket; conferido por TestesExtensao.test_sem_rede)",
                modo="B - offline", versao=VERSAO)


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NEXUS–RAPHAEL: laboratório auditável e offline")
    parser.add_argument("comando", nargs="?", default="teste",
                        choices=("teste", "inventario", "experimento", "angulo", "reforco", "megasena",
                                 "ciclo", "jogo", "lexico", "estado", "kuhn", "leduc", "velha", "sat",
                                 "calibracao", "bandidos", "megasena3", "caos"))
    parser.add_argument("--modo", choices=("rapido", "padrao", "intensivo"), default="rapido")
    parser.add_argument("--raiz", default="nexus_raphael", help="Pasta de saída do projeto")
    parser.add_argument("--texto", default="logic evidence learning uncertainty")
    parser.add_argument("--palavra", default="logic")
    parser.add_argument("--partidas", type=int, default=5)
    return parser.parse_args()


def principal() -> int:
    args = argumentos()
    if args.comando == "inventario":
        print(serie_json(inventario()))
        return 0
    cfg = Configuracao(raiz=args.raiz)
    repo = Repositorio(cfg)
    if args.comando == "teste":
        resultado = executar_testes()
        repo.salvar_json("testes.json", {k:v for k,v in resultado.items() if k != "detalhe"})
        repo.evento("testes", {k:v for k,v in resultado.items() if k != "detalhe"})
        print(resultado["detalhe"])
        print(serie_json({k:v for k,v in resultado.items() if k != "detalhe"}))
        return 0 if resultado["sucesso"] else 1
    if args.comando in COMANDOS_3:
        resultado = COMANDOS_3[args.comando](args.modo)
        repo.salvar_json(f"{args.comando}.json", resultado)
        print(serie_json(resultado))
        return 0
    lexico = LagoLexical(repo, cfg.permitir_rede)
    lexico.instalar_offline()
    if args.comando == "experimento":
        resultado = Experimentos.probabilidade(cfg, repo, args.modo)
    elif args.comando == "angulo":
        resultado = experimento_angulo(cfg, repo, args.modo)
    elif args.comando == "reforco":
        resultado = BandidoContextual.comparar(cfg, repo)
    elif args.comando == "megasena":
        resultado = MegaSenaLaboratorio.realizar(cfg, repo, args.modo)
    elif args.comando == "ciclo":
        msg = Nucleo(cfg, repo).executar(args.texto)
        resultado = asdict(msg)
        repo.salvar_json("ultimo_ciclo.json", resultado)
    elif args.comando == "jogo":
        if not 1 <= args.partidas <= 1000:
            raise ValueError("O número de partidas deve estar entre 1 e 1000")
        partidas = [Raphael.simular(seed, lexico, repo) for seed in range(args.partidas)]
        resultado = dict(versao=VERSAO, partidas=args.partidas,
                         media_pontos=statistics.fmean(x["total"] for x in partidas),
                         historico=partidas, rotulo="[SINTÉTICO]")
        repo.salvar_json("jogo_raphael.json", resultado)
    elif args.comando == "lexico":
        resultado = dict(palavra=args.palavra, sentidos=lexico.procurar(args.palavra),
                         tamanho_mini_lexico=len(lexico_embutido()))
    else:
        with repo.conexao() as con:
            registros = con.execute("SELECT tipo,COUNT(*) FROM registro GROUP BY tipo").fetchall()
            palavras = con.execute("SELECT COUNT(*) FROM palavra").fetchone()[0]
        resultado = dict(versao=VERSAO, registros=dict(registros), palavras_offline=palavras,
                         raiz=str(repo.raiz), inventario=inventario())
    print(serie_json(resultado))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(principal())
    except (ValueError, OSError, sqlite3.Error, TimeoutError) as erro:
        print(serie_json({"erro": str(erro), "tipo": type(erro).__name__, "rotulo": "[MEDIDO]"}),
              file=sys.stderr)
        sys.exit(2)
