"""O NEXUS-RAPHAEL "v2" recebido na Parte 116 (externos/nexus_raphael/nexus_raphael_v2_colado.txt), reescrito offline e só com a biblioteca padrão.

O texto recebido não fecha como Python: está truncado em dois pontos e faltam GameState, RaphaelGame e AdversarialLayer. Ele também tem
urllib.request (rede) e sqlite3 gravando em disco. Nada dele é importado nem executado. Este módulo é escrito do zero (regra da Parte 72) e tem
duas metades:
- `recebido_*`: as funções PURAS do texto, transcritas com o mesmo comportamento, para medir o que o código faz de fato (regra da Parte 88:
  comparar o texto com o SEU PRÓPRIO código);
- as versões corrigidas: o dicionário offline (WordNet local, no lugar da API), o vetor da palavra sem tocar no gerador global, a confiança e
  o intervalo pela t de Student, a avaliação por diferenças pareadas, uma auditoria de entrada que PODE falhar e a memória SQLite em
  ':memory:' (sem disco)."""

import functools
import gzip
import hashlib
import json
import math
import os
import random
import sqlite3


# --- 1. as funções do texto recebido, transcritas ---

def recebido_alfanumerico(palavra):
    """NumericRepresentationLayer.alphanumeric_value: soma A=1..Z=26 (anagramas e muito mais colidem)."""
    return sum(ord(c) - ord("A") + 1 for c in palavra.upper() if c.isalpha())


def recebido_posicional(palavra, base=26):
    """NumericRepresentationLayer.positional_encoding: base 26 com A = 0. NÃO é bijetiva: 'a' à esquerda é um zero à esquerda."""
    valor = 0
    for c in palavra.upper():
        if c.isalpha():
            valor = valor * base + (ord(c) - ord("A"))
    return valor


def recebido_numerologico(palavra):
    """NumericRepresentationLayer.numerological_reduction: soma dos códigos, reduzida a um algarismo."""
    total = sum(ord(c) for c in palavra)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total


def recebido_vetor(palavra, gerador, dimensao=10):
    """GeometricLayer.word_to_vector. O texto chama random.seed(md5) no gerador GLOBAL; aqui o gerador global é passado como `gerador`,
    para medir o efeito colateral sem mexer no random do processo."""
    gerador.seed(int(hashlib.md5(palavra.encode()).hexdigest(), 16))
    return [gerador.gauss(0, 1) for _ in range(dimensao)]


def cosseno(u, v):
    nu = math.sqrt(sum(x * x for x in u))
    nv = math.sqrt(sum(x * x for x in v))
    if nu * nv == 0:
        return 0.0
    return sum(a * b for a, b in zip(u, v)) / (nu * nv)


def recebido_confianca(valores):
    """MetacognitiveEvaluator._calculate_confidence: degraus pelo coeficiente de variação desvio/média. Com média NEGATIVA o CV é negativo
    (< 0,1) e a confiança é a máxima, 0,9, qualquer que seja a variância."""
    if len(valores) < 2:
        return 0.3
    media = sum(valores) / len(valores)
    desvio = math.sqrt(sum((v - media) ** 2 for v in valores) / len(valores))
    cv = desvio / media if media != 0 else float("inf")
    if cv < 0.1:
        return 0.9
    if cv < 0.3:
        return 0.7
    if cv < 0.5:
        return 0.5
    return 0.3


def recebido_ic(dados, confianca=0.95):
    """ProbabilisticInferenceEngine.confidence_interval: variância populacional, z = 1,96 se confianca == 0,95 e 2,576 em QUALQUER outro caso."""
    if not dados:
        return (0.0, 0.0)
    media = sum(dados) / len(dados)
    desvio = math.sqrt(sum((x - media) ** 2 for x in dados) / len(dados))
    z = 1.96 if confianca == 0.95 else 2.576
    margem = z * desvio / math.sqrt(len(dados))
    return (media - margem, media + margem)


def recebido_melhoria(valor, linha_de_base):
    """ExperimentResult.improvement_over_baseline."""
    if linha_de_base is not None and linha_de_base != 0:
        return (valor - linha_de_base) / abs(linha_de_base)
    return None


def recebido_status(pares):
    """O status de MetacognitiveEvaluator.evaluate_hypothesis a partir de [(valor, linha_de_base)]: a melhoria média contra ±0,1, sem variância."""
    if not pares:
        return "insufficient_data"
    melhorias = [m for m in (recebido_melhoria(v, b) for v, b in pares) if m is not None]
    media = sum(melhorias) / len(melhorias) if melhorias else 0.0
    if media > 0.1:
        return "confirmed"
    if media < -0.1:
        return "rejected"
    return "inconclusive"


CASOS_DE_ENTRADA = [("", "empty_string"), ("a" * 10000, "very_long_string"), ("'; DROP TABLE--", "sql_injection_attempt"),
                    ("<script>alert('xss')</script>", "xss_attempt"), ("../../../etc/passwd", "path_traversal"),
                    ("\x00\x01\x02", "binary_data"), ("😀🎉🔥", "unicode_emoji")]


def recebido_auditoria_de_entrada(tratador):
    """SecurityAuditor.audit_input_validation: os DOIS ramos (devolveu ou levantou exceção) somam 'passed'. 'failed' nunca sai de 0."""
    r = {"total_tests": len(CASOS_DE_ENTRADA), "passed": 0, "failed": 0}
    for entrada, _ in CASOS_DE_ENTRADA:
        try:
            tratador(entrada)
            r["passed"] += 1
        except Exception:
            r["passed"] += 1
    return r


# --- 2. as versões corrigidas ---

def _raiz():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dicionario_offline():
    """No lugar da API dictionaryapi.dev (rede): {lema minúsculo: [(classe, glosa), ...]} do WordNet 3.0 em dados/."""
    d = {}
    with gzip.open(os.path.join(_raiz(), "dados", "wordnet30_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        for linha in f:
            c = linha.rstrip("\n").split("\t")
            for lema in c[2].split(","):
                d.setdefault(lema.lower(), []).append((c[0], c[4]))
    return d


def vetor_da_palavra(palavra, dimensao=10):
    """O mesmo vetor do texto recebido (random.Random(int) e random.seed(int) geram a mesma sequência), mas num gerador LOCAL: não reinicia o
    gerador global de quem chama."""
    g = random.Random(int(hashlib.md5(palavra.encode()).hexdigest(), 16))
    return [g.gauss(0, 1) for _ in range(dimensao)]


def _tpdf(t, gl):
    c = math.exp(math.lgamma((gl + 1) / 2) - math.lgamma(gl / 2)) / math.sqrt(gl * math.pi)
    return c * (1 + t * t / gl) ** (-(gl + 1) / 2)


def t_cdf(x, gl, passos=4000):
    """P(T ≤ x) da t de Student com gl graus de liberdade, por Simpson de 0 a |x| (passos par)."""
    a = abs(x)
    h = a / passos
    s = _tpdf(0.0, gl) + _tpdf(a, gl)
    for i in range(1, passos):
        s += (4 if i % 2 else 2) * _tpdf(i * h, gl)
    meia = s * h / 3
    return 0.5 + meia if x >= 0 else 0.5 - meia


@functools.lru_cache(maxsize=None)
def t_quantil(p, gl):
    """O quantil p (0,5 < p < 1) da t de Student, por bisseção sobre t_cdf."""
    lo, hi = 0.0, 50.0
    for _ in range(60):
        meio = (lo + hi) / 2
        if t_cdf(meio, gl) < p:
            lo = meio
        else:
            hi = meio
    return (lo + hi) / 2


def ic_t(dados, confianca=0.95):
    """O intervalo de confiança da média pela t de Student, com a variância amostral (n − 1) e o quantil da confiança PEDIDA."""
    n = len(dados)
    media = sum(dados) / n
    s = math.sqrt(sum((x - media) ** 2 for x in dados) / (n - 1))
    m = t_quantil(0.5 + confianca / 2, n - 1) * s / math.sqrt(n)
    return (media - m, media + m)


def confianca_corrigida(valores):
    """O erro-padrão RELATIVO da média, s/(|média|·√n) (com |média|: o sinal não compra confiança). inf com média 0 ou n < 2."""
    n = len(valores)
    if n < 2:
        return float("inf")
    media = sum(valores) / n
    if media == 0:
        return float("inf")
    s = math.sqrt(sum((v - media) ** 2 for v in valores) / (n - 1))
    return s / (abs(media) * math.sqrt(n))


def avaliar_pareado(valores, linhas_de_base, t_critico):
    """A avaliação por DIFERENÇAS PAREADAS: d = valor − linha de base, t = média(d)/(s_d/√n). 'confirmed' se t > t_crítico, 'rejected' se
    t < −t_crítico, senão 'inconclusive'. Só +, −, ×, ÷ e √ (traduzido bit a bit na rodada 83). Devolve (status, t)."""
    n = len(valores)
    d = [v - b for v, b in zip(valores, linhas_de_base)]
    soma = 0.0
    for x in d:
        soma += x
    media = soma / n
    q = 0.0
    for x in d:
        q += (x - media) * (x - media)
    s = math.sqrt(q / (n - 1))
    t = media / (s / math.sqrt(n))
    if t > t_critico:
        return "confirmed", t
    if t < -t_critico:
        return "rejected", t
    return "inconclusive", t


def oraculo_de_saida(entrada, saida):
    """O que a auditoria recebida não tinha: um critério que a saída PODE violar. Uma saída que devolve sem escapar um marcador perigoso da
    entrada ('<script', '..', a aspa simples) falha."""
    s = str(saida)
    return not any(m in entrada and m in s for m in ("<script", "..", "'"))


def auditoria_com_oraculo(tratador):
    """A auditoria corrigida: passa só se o tratador levanta exceção OU devolve uma saída que o oráculo aceita. Devolve (passou, falhou)."""
    p = f = 0
    for entrada, _ in CASOS_DE_ENTRADA:
        try:
            ok = oraculo_de_saida(entrada, tratador(entrada))
        except Exception:
            ok = True
        p, f = (p + 1, f) if ok else (p, f + 1)
    return p, f


class Memoria:
    """A MemorySystem recebida, em ':memory:' (o texto gravava nexus_raphael_memory.db no diretório corrente ao ser construído)."""

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("CREATE TABLE hipoteses (id TEXT PRIMARY KEY, descricao TEXT, status TEXT, confianca REAL)")
        self.conn.execute("CREATE TABLE experimentos (id INTEGER PRIMARY KEY AUTOINCREMENT, hipotese TEXT, valor REAL, base REAL, meta TEXT)")

    def guardar_hipotese(self, hid, descricao, status="untested", confianca=0.5):
        self.conn.execute("INSERT OR REPLACE INTO hipoteses VALUES (?, ?, ?, ?)", (hid, descricao, status, confianca))

    def guardar_experimento(self, hid, valor, base, meta=None):
        self.conn.execute("INSERT INTO experimentos (hipotese, valor, base, meta) VALUES (?, ?, ?, ?)", (hid, valor, base, json.dumps(meta or {})))

    def fechar(self):
        self.conn.close()

    def experimentos(self, hid):
        return [(v, b) for v, b in self.conn.execute("SELECT valor, base FROM experimentos WHERE hipotese = ? ORDER BY id", (hid,))]


# --- 3. as fixtures dos experimentos da Parte 116 ---

def pares_de_sinonimos(quantos, semente=1160):
    """Pares de lemas a-z do MESMO sinset do WordNet (sinônimos), sorteados com semente."""
    grupos = []
    with gzip.open(os.path.join(_raiz(), "dados", "wordnet30_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        for linha in f:
            ls = sorted({l.lower() for l in linha.split("\t")[2].split(",") if l.isascii() and l.isalpha()})
            if len(ls) >= 2:
                grupos.append(ls)
    rng = random.Random(semente)
    out = []
    for _ in range(quantos):
        g = rng.choice(grupos)
        a, b = rng.sample(g, 2)
        out.append((a, b))
    return out


def pares_aleatorios(palavras, quantos, semente=1161):
    rng = random.Random(semente)
    ps = sorted(palavras)
    return [tuple(rng.sample(ps, 2)) for _ in range(quantos)]


def contaminacao(palavra, vezes=1000, corrigido=False):
    """Quantos valores DISTINTOS o gerador 'global' dá na próxima chamada depois de cada vetor de `palavra`. O texto recebido reinicia o gerador:
    1 valor. O corrigido não toca nele: `vezes` valores."""
    g = random.Random(1162)
    vistos = set()
    for _ in range(vezes):
        if corrigido:
            vetor_da_palavra(palavra)
        else:
            recebido_vetor(palavra, g)
        vistos.add(g.random())
    return len(vistos)


def avaliacao_nula(tentativas=20000, semente=1163, mu=10.0, sigma=2.0):
    """Sob a hipótese NULA (valor e linha de base iid N(mu, sigma)), a fração de 'confirmed' e de 'rejected' do status recebido com 1 experimento."""
    rng = random.Random(semente)
    c = r = 0
    for _ in range(tentativas):
        s = recebido_status([(rng.gauss(mu, sigma), rng.gauss(mu, sigma))])
        c += s == "confirmed"
        r += s == "rejected"
    return c / tentativas, r / tentativas


def avaliacao_nula_pareada(tentativas=20000, n=5, semente=1164, mu=10.0, sigma=2.0):
    """A mesma nula na avaliação pareada, n = 5 experimentos, t crítico unilateral de 95% com 4 graus de liberdade. Devolve a fração de 'confirmed'."""
    rng = random.Random(semente)
    tc = t_quantil(0.95, n - 1)
    c = 0
    for _ in range(tentativas):
        v = [rng.gauss(mu, sigma) for _ in range(n)]
        b = [rng.gauss(mu, sigma) for _ in range(n)]
        c += avaliar_pareado(v, b, tc)[0] == "confirmed"
    return c / tentativas


def cobertura(funcao_ic, confianca, tentativas=20000, n=30, semente=1165):
    """A fração das amostras normais N(0, 1) de tamanho n cujo intervalo contém a média verdadeira 0."""
    rng = random.Random(semente)
    dentro = 0
    for _ in range(tentativas):
        lo, hi = funcao_ic([rng.gauss(0, 1) for _ in range(n)], confianca)
        dentro += lo <= 0.0 <= hi
    return dentro / tentativas
