"""O word_rl_lab recebido (Parte 111), reescrito só com a biblioteca padrão e OFFLINE. As cópias verbatim (v1 e v2) ficam em
externos/word_rl_lab/ e nunca são importadas. Q-learning tabular num jogo de palavras numa grade de letras (estilo Boggle), com um
estimador de confiança (regressão logística online) avaliado por Brier, linha de base e ECE, e a avaliação guloso × aleatório.

Fiel à v2 (mesmos números: mesma ordem de sorteios do random, mesmo CRC32 do zlib, mesma recompensa), com três mudanças:
  1. Sem numpy: vetores como listas; o produto interno é somado em laço sequencial (sem o sum() compensado, regra da Parte 34).
  2. Sem rede: o dicionário é a lista EMBUTIDA da v2 ou o DATA LAKE do projeto (os lemas do WordNet 3.0 em dados/, regra da
     Parte 30), nunca a API. O backend "api" da v2 não existe aqui.
  3. O desenho da v1 entra como BRAÇO DE COMPARAÇÃO (ação = DIREÇÃO, estado = últimas 3 letras), para medir a afirmação da v2:
     "como a ação é a letra, o que se aprende vale em qualquer grade".
Mais uma auditoria AST v2 (security_audit_ast_v2): a da Parte 109 lia NOMES de módulo e errou nos dois sentidos aqui."""

import ast
import gzip
import math
import os
import random
import zlib
from collections import Counter

STOP = "<PARAR>"
FAIL_REWARD = -1.0
STEP_REWARD = 0.0

LETTER_FREQ = {
    "E": 12.7, "T": 9.1, "A": 8.2, "O": 7.5, "I": 7.0, "N": 6.7, "S": 6.3,
    "H": 6.1, "R": 6.0, "D": 4.3, "L": 4.0, "C": 2.8, "U": 2.8, "M": 2.4,
    "W": 2.4, "F": 2.2, "G": 2.0, "Y": 2.0, "P": 1.9, "B": 1.5, "V": 1.0,
    "K": 0.8, "J": 0.15, "X": 0.15, "Q": 0.10, "Z": 0.07,
}
SCRABBLE = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3,
    "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10,
}


def _palavras_embutidas():
    """A lista EMBUTIDA da v2, lida da cópia verbatim pela AST (sem importar nem executar o arquivo)."""
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(raiz, "externos", "word_rl_lab", "word_rl_lab_v2_recebido.py"), encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    for n in arvore.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "EMBEDDED_WORDS":
            return frozenset(n.value.args[0].func.value.value.split())
    raise LookupError("EMBEDDED_WORDS não encontrado")


EMBEDDED_WORDS = _palavras_embutidas()


def lemas_wordnet():
    """O DATA LAKE: os lemas do WordNet 3.0 (dados/wordnet30_sinsets.tsv.gz), só os formados por letras a-z, em minúsculas."""
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = set()
    with gzip.open(os.path.join(raiz, "dados", "wordnet30_sinsets.tsv.gz"), "rt", encoding="utf-8") as f:
        for linha in f:
            for lema in linha.split("\t")[2].split(","):
                lema = lema.lower()
                if lema.isascii() and lema.isalpha():
                    out.add(lema)
    return frozenset(out)


class Dicionario:
    def __init__(self, palavras):
        self.palavras = palavras

    def is_word(self, w):
        return w.lower() in self.palavras


def word_score(word):
    return sum(SCRABBLE.get(c, 0) for c in word.upper()) * len(word)


def word_to_vector(word, dim=16):
    """Igual à v2: unigramas por slot + bigramas por CRC32, normalizado (L2)."""
    vec = [0.0] * dim
    letters = [c for c in word.upper() if "A" <= c <= "Z"]
    for ch in letters:
        vec[(ord(ch) - 65) % dim] += 1.0
    for a, b in zip(letters, letters[1:]):
        vec[zlib.crc32((a + b).encode("ascii")) % dim] += 0.5
    s = 0.0
    for v in vec:
        s += v * v
    n = math.sqrt(s)
    return [v / n for v in vec] if n > 0 else vec


# --- ambiente ---

class WordGridEnv:
    def __init__(self, size=5, min_len=3, max_len=5, rng=None, uniforme=False):
        self.size, self.min_len, self.max_len = size, min_len, max_len
        self.rng = rng or random.Random(0)
        self.uniforme = uniforme      # True: letras uniformes, como na v1 (string.ascii_uppercase)
        self.grid = []

    def reset(self):
        if self.uniforme:
            self.grid = [[self.rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(self.size)] for _ in range(self.size)]
        else:
            letters, weights = list(LETTER_FREQ), list(LETTER_FREQ.values())
            self.grid = [self.rng.choices(letters, weights=weights, k=self.size) for _ in range(self.size)]
        return self.grid

    def letter(self, pos):
        return self.grid[pos[0]][pos[1]]

    def neighbors(self, pos):
        r, c = pos
        return [(r + dr, c + dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                if (dr or dc) and 0 <= r + dr < self.size and 0 <= c + dc < self.size]

    def path_is_legal(self, path):
        if not path or len(set(path)) != len(path):
            return False
        if any(not (0 <= r < self.size and 0 <= c < self.size) for r, c in path):
            return False
        return all(b in self.neighbors(a) for a, b in zip(path, path[1:]))


def valid_actions(env, path):
    acts = {}
    if len(path) < env.max_len:
        visited = set(path)
        for pos in env.neighbors(path[-1]):
            if pos not in visited:
                acts.setdefault(env.letter(pos), pos)
    if len(path) >= env.min_len:
        acts[STOP] = None
    return acts


# --- agente (igual à v2) ---

class QAgent:
    def __init__(self, alpha=0.2, gamma=0.95, epsilon=0.3, seed=0):
        self.alpha, self.gamma, self.epsilon = alpha, gamma, epsilon
        self.rng = random.Random(seed)
        self.q = {}

    def value(self, s, a):
        return self.q.get((s, a), 0.0)

    def choose(self, s, actions, mode):
        if mode == "random" or (mode == "epsilon" and self.rng.random() < self.epsilon):
            return self.rng.choice(actions)
        best = max(self.value(s, a) for a in actions)
        return self.rng.choice([a for a in actions if self.value(s, a) == best])

    def update(self, s, a, r, next_s, next_actions):
        future = 0.0
        if next_s is not None and next_actions:
            future = max(self.value(next_s, b) for b in next_actions)
        old = self.value(s, a)
        self.q[(s, a)] = old + self.alpha * (r + self.gamma * future - old)


# --- estimador de confiança e métricas (iguais à v2, sem numpy) ---

class ConfidenceEstimator:
    def __init__(self, dim=16, lr=0.1):
        self.dim, self.lr = dim, lr
        self.w = [0.0] * (dim + 2)
        self.b = 0.0

    def features(self, word, q_stop, max_len):
        return word_to_vector(word, self.dim) + [math.tanh(q_stop / 20.0), len(word) / max_len]

    def predict(self, x):
        z = self.b
        for wi, xi in zip(self.w, x):
            z += wi * xi
        z = max(-30.0, min(30.0, z))
        return 1.0 / (1.0 + math.exp(-z))

    def update(self, x, y):
        g = y - self.predict(x)
        self.w = [wi + self.lr * g * xi for wi, xi in zip(self.w, x)]
        self.b += self.lr * g


def brier(ps, ys):
    return sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ps) if ps else float("nan")


def ece(ps, ys, bins=10):
    n = len(ps)
    if n == 0:
        return float("nan")
    total = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, p in enumerate(ps) if lo <= p < hi or (b == bins - 1 and p >= 1.0)]
        if idx:
            total += len(idx) / n * abs(sum(ps[i] for i in idx) / len(idx) - sum(ys[i] for i in idx) / len(idx))
    return total


def prequential_base_rate(ys):
    out, s = [], 0.0
    for t, y in enumerate(ys):
        out.append((1.0 + s) / (2.0 + t))
        s += y
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


# --- episódio, treino, avaliação (v2) ---

def run_episode(env, dic, agent, mode, learn, estimator=None, learn_estimator=False):
    """Devolve (palavra, válida, recompensa, confiança)."""
    env.reset()
    start = (env.rng.randrange(env.size), env.rng.randrange(env.size))
    path, prefix, prev = [start], env.letter(start), None
    while True:
        acts = valid_actions(env, path)
        s = prefix
        if not acts:
            if learn and prev:
                agent.update(prev[0], prev[1], FAIL_REWARD, None, ())
            return prefix, False, FAIL_REWARD, None
        names = list(acts)
        if learn and prev:
            agent.update(prev[0], prev[1], STEP_REWARD, s, names)
        a = agent.choose(s, names, mode)
        if a == STOP:
            conf = x = None
            if estimator is not None:
                x = estimator.features(prefix, agent.value(s, STOP), env.max_len)
                conf = estimator.predict(x)
            valid = dic.is_word(prefix)
            reward = float(word_score(prefix)) if valid else FAIL_REWARD
            if learn:
                agent.update(s, STOP, reward, None, ())
            if estimator is not None and learn_estimator and x is not None:
                estimator.update(x, 1.0 if valid else 0.0)
            return prefix, valid, reward, conf
        path.append(acts[a])
        prefix += a
        prev = (s, a)


class Config:
    def __init__(self, episodios=5000, avaliacao=1000, tamanho=5, min_len=3, max_len=5, alpha=0.2, gamma=0.95,
                 eps_ini=0.3, eps_fim=0.05, seed=42):
        self.episodios, self.avaliacao, self.tamanho = episodios, avaliacao, tamanho
        self.min_len, self.max_len, self.alpha, self.gamma = min_len, max_len, alpha, gamma
        self.eps_ini, self.eps_fim, self.seed = eps_ini, eps_fim, seed


def train(cfg, dic):
    env = WordGridEnv(cfg.tamanho, cfg.min_len, cfg.max_len, rng=random.Random(cfg.seed))
    agent = QAgent(cfg.alpha, cfg.gamma, cfg.eps_ini, seed=cfg.seed + 1)
    est = ConfidenceEstimator()
    ps, ys, rewards, found = [], [], [], Counter()
    for ep in range(1, cfg.episodios + 1):
        frac = (ep - 1) / max(1, cfg.episodios - 1)
        agent.epsilon = cfg.eps_ini + (cfg.eps_fim - cfg.eps_ini) * frac
        w, valid, r, conf = run_episode(env, dic, agent, "epsilon", learn=True, estimator=est, learn_estimator=True)
        rewards.append(r)
        if conf is not None:
            ps.append(conf)
            ys.append(1.0 if valid else 0.0)
        if valid:
            found[w] += 1
    base = prequential_base_rate(ys)
    return agent, est, {
        "recompensa_media": sum(rewards) / len(rewards), "tentativas": len(ys), "validas": int(sum(ys)),
        "distintas": len(found), "top": found.most_common(10),
        "brier_estimador": brier(ps, ys), "brier_base": brier(base, ys), "ece": ece(ps, ys), "tabela_q": len(agent.q),
    }


def evaluate(cfg, dic, agent):
    """Guloso × aleatório nas MESMAS grades e inícios (mesma semente do ambiente). Devolve {nome: (taxa, (lo, hi), recompensa)}."""
    out = {}
    for nome, pol, mode in (("guloso", agent, "greedy"), ("aleatorio", QAgent(seed=cfg.seed + 2), "random")):
        env = WordGridEnv(cfg.tamanho, cfg.min_len, cfg.max_len, rng=random.Random(cfg.seed + 100_000))
        res = [run_episode(env, dic, pol, mode, learn=False) for _ in range(cfg.avaliacao)]
        k = sum(r[1] for r in res)
        out[nome] = (k / len(res), wilson(k, len(res)), sum(r[2] for r in res) / len(res))
    return out


# --- o desenho da v1 como braço de comparação ---

DIRECOES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def episodio_v1(env, dic, agent, mode, learn, max_len=8):
    """As regras da v1: ação = DIREÇÃO (0-7) ou PARAR (8); estado = últimas 3 letras; pode revisitar casas; sair da grade = −10;
    PARAR com 1 letra = −5; palavra inválida = −5; válida = pontuação; passo = −0,1. A grade e o início vêm do rng do ambiente.
    Devolve (palavra, válida)."""
    env.reset()
    pos = (env.rng.randrange(env.size), env.rng.randrange(env.size))
    path, prefix = [pos], env.letter(pos)
    acoes = list(range(9))
    while True:
        s = prefix[-3:]
        a = agent.choose(s, acoes, mode)
        if a == 8 or len(path) >= max_len:
            if len(path) < 2:
                r, w, ok = -5.0, "", False
            else:
                w = prefix
                ok = dic.is_word(w)
                r = float(word_score(w)) if ok else -5.0
            if learn:
                agent.update(s, a, r, None, ())
            return w, ok
        dr, dc = DIRECOES[a]
        nr, nc = path[-1][0] + dr, path[-1][1] + dc
        if not (0 <= nr < env.size and 0 <= nc < env.size):
            if learn:
                agent.update(s, a, -10.0, None, ())
            return prefix, False
        path.append((nr, nc))
        nxt = prefix + env.letter((nr, nc))
        if learn:
            agent.update(s, a, -0.1, nxt[-3:], acoes)
        prefix = nxt


def treinar_e_avaliar_v1(cfg, dic, uniforme=True):
    """Treina o desenho da v1 (α=0,3, γ=0,9, ε=0,2 fixo, como na v1) e avalia guloso × aleatório nas mesmas grades."""
    env = WordGridEnv(cfg.tamanho, rng=random.Random(cfg.seed), uniforme=uniforme)
    agent = QAgent(0.3, 0.9, 0.2, seed=cfg.seed + 1)
    for _ in range(cfg.episodios):
        episodio_v1(env, dic, agent, "epsilon", learn=True)
    out = {}
    for nome, pol, mode in (("guloso", agent, "greedy"), ("aleatorio", QAgent(seed=cfg.seed + 2), "random")):
        env = WordGridEnv(cfg.tamanho, rng=random.Random(cfg.seed + 100_000), uniforme=uniforme)
        k = sum(episodio_v1(env, dic, pol, mode, learn=False)[1] for _ in range(cfg.avaliacao))
        out[nome] = (k / cfg.avaliacao, wilson(k, cfg.avaliacao))
    return out


# --- auditoria AST v2: capacidade, não nome ---

_REDE_CHAMADAS = {"urlopen", "get", "post", "put", "request", "download", "connect", "urlretrieve", "create_connection"}
_REDE_BASES = {"requests", "urllib", "httpx", "aiohttp", "socket", "nltk", "http", "ftplib", "smtplib"}
_REDE_IMPORTS = {"requests", "httpx", "aiohttp", "socket", "http", "ftplib", "smtplib", "urllib.request"}


def security_audit_ast_v2(source):
    """A auditoria da Parte 109 lia NOMES de módulo: acusava `from urllib.parse import quote` (formatação, sem rede) e não via
    `requests.get` nem `nltk.download` (rede de verdade). Esta conta CAPACIDADES: um import de módulo de rede (urllib.request sim,
    urllib.parse não) e uma CHAMADA cujo atributo é de rede sobre uma base de rede (requests.get, nltk.download, urllib.request.urlopen).
    Devolve a lista ordenada de achados."""
    achados = set()
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.Import):
            for a in n.names:
                if a.name in _REDE_IMPORTS or a.name.split(".")[0] in _REDE_IMPORTS - {"urllib.request"}:
                    achados.add("import:" + a.name)
        elif isinstance(n, ast.ImportFrom):
            mod = n.module or ""
            if mod in _REDE_IMPORTS or mod.split(".")[0] in _REDE_IMPORTS - {"urllib.request"}:
                achados.add("import:" + mod)
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in _REDE_CHAMADAS:
            base = n.func.value
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name) and base.id in _REDE_BASES:
                achados.add("rede:" + ast.unparse(n.func))
    return sorted(achados)


# --- os mecanismos de (a) e (f), postos à prova (P2777/P2778) ---

class EstimadorSemQ(ConfidenceEstimator):
    """A ablação de (n): o mesmo estimador com a variável Q(PARAR) fixa em 0 (tanh(0) = 0); sobra só o vetor da palavra e o comprimento."""

    def features(self, word, q_stop, max_len):
        return super().features(word, 0.0, max_len)


def treinar_com_estimador(cfg, dic, classe):
    """O `train` da v2 com outra classe de estimador; devolve (razão Brier estimador/base, Brier estimador, Brier base)."""
    env = WordGridEnv(cfg.tamanho, cfg.min_len, cfg.max_len, rng=random.Random(cfg.seed))
    agent = QAgent(cfg.alpha, cfg.gamma, cfg.eps_ini, seed=cfg.seed + 1)
    est = classe()
    ps, ys = [], []
    for ep in range(1, cfg.episodios + 1):
        agent.epsilon = cfg.eps_ini + (cfg.eps_fim - cfg.eps_ini) * ((ep - 1) / max(1, cfg.episodios - 1))
        _, valid, _, conf = run_episode(env, dic, agent, "epsilon", learn=True, estimator=est, learn_estimator=True)
        if conf is not None:
            ps.append(conf)
            ys.append(1.0 if valid else 0.0)
    be, bb = brier(ps, ys), brier(prequential_base_rate(ys), ys)
    return be / bb, be, bb


def palavras_distintas_gulosas(cfg, dic, agent):
    """(o): as palavras válidas DISTINTAS que o guloso forma na avaliação (as mesmas grades de `evaluate`)."""
    env = WordGridEnv(cfg.tamanho, cfg.min_len, cfg.max_len, rng=random.Random(cfg.seed + 100_000))
    achadas = Counter()
    for _ in range(cfg.avaliacao):
        w, ok, _, _ = run_episode(env, dic, agent, "greedy", learn=False)
        if ok:
            achadas[w] += 1
    return achadas


class EstimadorSoLetras(ConfidenceEstimator):
    """A ablação de (p): Q(PARAR) e comprimento fixos em 0; sobra só o vetor normalizado das letras (que não carrega o comprimento)."""

    def features(self, word, q_stop, max_len):
        return word_to_vector(word, self.dim) + [0.0, 0.0]


# --- a hipótese do REPERTÓRIO (Parte 112) ---

def estimador_sob_politica_aleatoria(cfg, dic, classe):
    """O estimador de confiança treinado sobre as palavras de uma política ALEATÓRIA (sem repertório: um agente que nunca aprende, Q = 0).
    Se o estimador da Parte 111 aprende os HÁBITOS do agente, aqui ele não tem hábito a aprender. Devolve (razão Brier estimador/base,
    número de tentativas avaliadas, número de válidas)."""
    env = WordGridEnv(cfg.tamanho, cfg.min_len, cfg.max_len, rng=random.Random(cfg.seed))
    agent = QAgent(seed=cfg.seed + 1)
    est = classe()
    ps, ys = [], []
    for _ in range(cfg.episodios):
        _, valid, _, conf = run_episode(env, dic, agent, "random", learn=False, estimator=est, learn_estimator=True)
        if conf is not None:
            ps.append(conf)
            ys.append(1.0 if valid else 0.0)
    return brier(ps, ys) / brier(prequential_base_rate(ys), ys), len(ys), int(sum(ys))
