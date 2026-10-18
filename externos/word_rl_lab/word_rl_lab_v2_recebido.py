#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
word_rl_lab.py — v2

Laboratório de RL em um jogo de palavras (grade de letras, estilo Boggle).

- Agente Q-learning tabular: estado = prefixo formado; ação = letra de uma
  célula vizinha ainda não visitada, ou PARAR. Como a ação é a *letra*,
  o que se aprende vale em qualquer grade (na prática, uma árvore de palavras).
- Dicionário com três fontes: lista embutida (offline, reproduzível),
  WordNet (nltk) ou API dictionaryapi.dev. Apenas respostas definitivas
  vão para o cache.
- Estimador de confiança: prevê, ANTES de consultar o dicionário, se a
  palavra será válida, usando o vetor da palavra e o valor Q do próprio
  agente. Avaliado por Brier, linha de base e ECE. Calibração não é consciência.
- Avaliação final: agente guloso vs. política aleatória nas MESMAS grades.

Uso:
    python word_rl_lab.py                          # treino + avaliação
    python word_rl_lab.py --episodios 20000 --seed 7
    python word_rl_lab.py --dicionario wordnet --baixar-wordnet
    python word_rl_lab.py --autoteste

Dependências: numpy (obrigatória); nltk, requests, python-chess (opcionais).
"""
# [SYNTHAI, Parte 111] Cópia VERBATIM da v2 colada pelo usuário. ARQUIVO: nunca importado nem executado pelo projeto
# (numpy; requests/nltk opcionais). A versão anexada, reescrita offline e só com a biblioteca padrão, é synthai/palavras_rl.py.
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import random
import sys
import zlib
from collections import Counter
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Sequence, Tuple
from urllib.parse import quote

import numpy as np

try:
    import requests  # type: ignore
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from nltk.corpus import wordnet as wn  # type: ignore
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False

try:
    import chess  # type: ignore
    HAS_CHESS = True
except ImportError:
    HAS_CHESS = False

logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("word_rl_lab")

VERSAO = "2.0.0"
STOP = "<PARAR>"
FAIL_REWARD = -1.0
STEP_REWARD = 0.0

# ---------------------------------------------------------------------------
# 1. Dados fixos
# ---------------------------------------------------------------------------

# Frequência aproximada de letras em inglês (%): torna palavras encontráveis.
LETTER_FREQ = {
    "E": 12.7, "T": 9.1, "A": 8.2, "O": 7.5, "I": 7.0, "N": 6.7, "S": 6.3,
    "H": 6.1, "R": 6.0, "D": 4.3, "L": 4.0, "C": 2.8, "U": 2.8, "M": 2.4,
    "W": 2.4, "F": 2.2, "G": 2.0, "Y": 2.0, "P": 1.9, "B": 1.5, "V": 1.0,
    "K": 0.8, "J": 0.15, "X": 0.15, "Q": 0.10, "Z": 0.07,
}

SCRABBLE = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10,
}

EMBEDDED_WORDS = frozenset("""
the and for are but not you all any can had her was one our out day get has
him his how man new now old see two way who boy did its let put say she too
use art bat bed big box bus car cat cow cry cup cut dad dog dry ear eat egg
end eye fan far fat few fit fly fox fun gas god gun hat hen hit hot ice ink
jam job joy key kid lap law leg lid lie lip log low mad map mat men mix mom
mud net nut oil pan pen pet pie pig pin pot rat red rid rod row run sad sat
sea set sit six sky son sun tag tan tap tea ten tie tin toe top toy try van
war wet win yes yet zoo ate tee tot net ion ore ash hoe eon dot rot nod
able also area army away baby back ball band bank base bear beat bird blue
boat body bone book born both cake call calm card care case cash cast cell
chat city coat cold cool cost dark data date dead deal dear deep door down
draw drop dust each earn east easy edge else even face fact fair fall farm
fast fear feel file fill film find fine fire fish five flat food foot form
four free from game gate gift girl give goal gold good hair half hall hand
hard hate have head hear heat help here hero high hill hold hole home hope
horn host hour idea iron item join just keep kind king lake land last late
lead left less life line lion list live long look lord lose loss love made
main make male many mark meal mean meat meet mind miss moon more most move
much name near neck need news next nice nine none nose note once only open
over pain pair park part pass past path pick plan play poem pool poor rain
rate read real rest rice rich ride ring rise risk road rock role roof room
root rose rule safe sail salt same sand save seat seed seen sell send ship
shoe shop shot show side sign sing site size skin slow snow soft soil song
soon sort soul star stay step stop such sure tail take tale talk tall tank
team tear tell tend term test than that them then they thin this time tone
tree trip true turn type unit vast very view vote wait walk wall want warm
wash wave weak wear week well west what when wide wife wild will wind wine
wing wire wise wish with wood word work yard year your zero zone note rite
tone toes tens tide tied seat sent nest rent tent heat hint
about after again earth heart house later light might never other place
right small sound still story table their there these thing think three
water where which world would write stone notes tones heats hints
""".split())


def word_score(word: str) -> int:
    """Pontuação estilo Scrabble × comprimento."""
    return sum(SCRABBLE.get(c, 0) for c in word.upper()) * len(word)


def word_to_vector(word: str, dim: int = 16) -> np.ndarray:
    """Unigramas por slot + bigramas com hash CRC32 (sensível à ordem). Normalizado."""
    vec = np.zeros(dim, dtype=np.float64)
    letters = [c for c in word.upper() if "A" <= c <= "Z"]
    for ch in letters:
        vec[(ord(ch) - 65) % dim] += 1.0
    for a, b in zip(letters, letters[1:]):
        vec[zlib.crc32((a + b).encode("ascii")) % dim] += 0.5
    n = np.linalg.norm(vec)
    return vec / n if n > 0 else vec


# ---------------------------------------------------------------------------
# 2. Dicionário (só resposta definitiva vai para o cache)
# ---------------------------------------------------------------------------

class Dictionary:
    API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    def __init__(self, backend: str = "auto", cache_file: Optional[str] = "word_cache_api.json",
                 timeout: float = 3.0, allow_download: bool = False):
        self.backend = self._resolve(backend, allow_download)
        self.timeout = timeout
        self.cache: Dict[str, bool] = {}
        self.unknown = 0          # consultas sem resposta definitiva
        self._new = 0
        self.cache_file = cache_file if self.backend == "api" else None
        if self.cache_file:
            self._load()
        log.info("Dicionário: %s", self.backend)

    @staticmethod
    def _wordnet_ready(allow_download: bool) -> bool:
        if not HAS_NLTK:
            return False
        try:
            wn.synsets("dog")
            return True
        except LookupError:
            if not allow_download:
                return False
            try:
                import nltk  # type: ignore
                nltk.download("wordnet", quiet=True)
                wn.synsets("dog")
                return True
            except Exception as exc:  # noqa: BLE001
                log.warning("Falha ao baixar WordNet: %s", exc)
                return False

    def _resolve(self, backend: str, allow_download: bool) -> str:
        if backend == "auto":
            return "wordnet" if self._wordnet_ready(allow_download) else "embedded"
        if backend == "embedded":
            return backend
        if backend == "wordnet":
            if not self._wordnet_ready(allow_download):
                raise RuntimeError("WordNet indisponível (instale nltk e use --baixar-wordnet).")
            return backend
        if backend == "api":
            if not HAS_REQUESTS:
                raise RuntimeError("Backend 'api' exige o pacote requests.")
            return backend
        raise ValueError(f"backend desconhecido: {backend}")

    def _load(self) -> None:
        if self.cache_file and os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.cache = {str(k): bool(v) for k, v in data.items()}
            except (OSError, json.JSONDecodeError) as exc:
                log.warning("Cache ilegível (%s); começando vazio.", exc)

    def save(self) -> None:
        if not self.cache_file or self._new == 0:
            return
        tmp = self.cache_file + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.cache, f)
            os.replace(tmp, self.cache_file)
            self._new = 0
        except OSError as exc:
            log.warning("Falha ao salvar cache: %s", exc)

    def lookup(self, word: str) -> Optional[bool]:
        """True/False se houver resposta definitiva; None se nenhuma fonte respondeu."""
        key = word.lower()
        if key in self.cache:
            return self.cache[key]
        if self.backend == "embedded":
            return key in EMBEDDED_WORDS
        res = self._wordnet(key) if self.backend == "wordnet" else self._api(key)
        if res is None:
            self.unknown += 1
            return None                     # NÃO entra no cache
        self.cache[key] = res
        self._new += 1
        if self._new >= 50:
            self.save()
        return res

    def is_word(self, word: str) -> bool:
        return bool(self.lookup(word))

    def _wordnet(self, word: str) -> Optional[bool]:
        try:
            return len(wn.synsets(word)) > 0
        except Exception:  # noqa: BLE001
            return None

    def _api(self, word: str) -> Optional[bool]:
        try:
            r = requests.get(self.API_URL.format(word=quote(word)), timeout=self.timeout)
        except requests.RequestException:
            return None
        if r.status_code == 200:
            return True
        if r.status_code == 404:
            return False
        return None


# ---------------------------------------------------------------------------
# 3. Ambiente
# ---------------------------------------------------------------------------

Pos = Tuple[int, int]


@dataclass
class WordGridEnv:
    size: int = 5
    min_len: int = 3
    max_len: int = 5
    rng: random.Random = field(default_factory=lambda: random.Random(0))
    grid: List[List[str]] = field(default_factory=list)

    def reset(self) -> List[List[str]]:
        letters, weights = list(LETTER_FREQ), list(LETTER_FREQ.values())
        self.grid = [self.rng.choices(letters, weights=weights, k=self.size)
                     for _ in range(self.size)]
        return self.grid

    def letter(self, pos: Pos) -> str:
        return self.grid[pos[0]][pos[1]]

    def neighbors(self, pos: Pos) -> List[Pos]:
        r, c = pos
        return [(r + dr, c + dc)
                for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                if (dr or dc) and 0 <= r + dr < self.size and 0 <= c + dc < self.size]

    def path_is_legal(self, path: Sequence[Pos]) -> bool:
        if not path or len(set(path)) != len(path):
            return False
        if any(not (0 <= r < self.size and 0 <= c < self.size) for r, c in path):
            return False
        return all(b in self.neighbors(a) for a, b in zip(path, path[1:]))


def valid_actions(env: WordGridEnv, path: Sequence[Pos]) -> Dict[str, Optional[Pos]]:
    """Letras de vizinhos não visitados (uma célula por letra) + PARAR se len >= min_len."""
    acts: Dict[str, Optional[Pos]] = {}
    if len(path) < env.max_len:
        visited = set(path)
        for pos in env.neighbors(path[-1]):
            if pos not in visited:
                acts.setdefault(env.letter(pos), pos)
    if len(path) >= env.min_len:
        acts[STOP] = None
    return acts


# ---------------------------------------------------------------------------
# 4. Agente
# ---------------------------------------------------------------------------

class QAgent:
    def __init__(self, alpha: float = 0.2, gamma: float = 0.95,
                 epsilon: float = 0.3, seed: int = 0):
        self.alpha, self.gamma, self.epsilon = alpha, gamma, epsilon
        self.rng = random.Random(seed)
        self.q: Dict[Tuple[str, str], float] = {}

    def value(self, s: str, a: str) -> float:
        return self.q.get((s, a), 0.0)

    def choose(self, s: str, actions: List[str], mode: str) -> str:
        if mode == "random" or (mode == "epsilon" and self.rng.random() < self.epsilon):
            return self.rng.choice(actions)
        best = max(self.value(s, a) for a in actions)
        return self.rng.choice([a for a in actions if self.value(s, a) == best])

    def update(self, s: str, a: str, r: float,
               next_s: Optional[str], next_actions: Sequence[str]) -> None:
        future = 0.0
        if next_s is not None and next_actions:
            future = max(self.value(next_s, b) for b in next_actions)
        old = self.value(s, a)
        self.q[(s, a)] = old + self.alpha * (r + self.gamma * future - old)


# ---------------------------------------------------------------------------
# 5. Estimador de confiança + métricas
# ---------------------------------------------------------------------------

class ConfidenceEstimator:
    """Regressão logística online. Usa o vetor da palavra e o Q(PARAR) do agente."""

    def __init__(self, dim: int = 16, lr: float = 0.1):
        self.dim, self.lr = dim, lr
        self.w = np.zeros(dim + 2)
        self.b = 0.0

    def features(self, word: str, q_stop: float, max_len: int) -> np.ndarray:
        extra = np.array([math.tanh(q_stop / 20.0), len(word) / max_len])
        return np.concatenate([word_to_vector(word, self.dim), extra])

    def predict(self, x: np.ndarray) -> float:
        z = max(-30.0, min(30.0, float(self.w @ x + self.b)))
        return 1.0 / (1.0 + math.exp(-z))

    def update(self, x: np.ndarray, y: float) -> None:
        g = y - self.predict(x)
        self.w += self.lr * g * x
        self.b += self.lr * g


def brier(ps: Sequence[float], ys: Sequence[float]) -> float:
    return sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ps) if ps else float("nan")


def ece(ps: Sequence[float], ys: Sequence[float], bins: int = 10) -> float:
    n = len(ps)
    if n == 0:
        return float("nan")
    total = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, p in enumerate(ps) if lo <= p < hi or (b == bins - 1 and p >= 1.0)]
        if idx:
            conf = sum(ps[i] for i in idx) / len(idx)
            acc = sum(ys[i] for i in idx) / len(idx)
            total += len(idx) / n * abs(conf - acc)
    return total


def prequential_base_rate(ys: Sequence[float]) -> List[float]:
    """Linha de base: prevê a taxa observada até t-1 (Laplace)."""
    out, s = [], 0.0
    for t, y in enumerate(ys):
        out.append((1.0 + s) / (2.0 + t))
        s += y
    return out


def wilson(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


# ---------------------------------------------------------------------------
# 6. Episódio, treino, avaliação
# ---------------------------------------------------------------------------

@dataclass
class EpisodeResult:
    word: str
    valid: bool
    reward: float
    confidence: Optional[float]


def run_episode(env: WordGridEnv, dic: Dictionary, agent: QAgent, mode: str,
                learn: bool, estimator: Optional[ConfidenceEstimator] = None,
                learn_estimator: bool = False) -> EpisodeResult:
    env.reset()
    start = (env.rng.randrange(env.size), env.rng.randrange(env.size))
    path, prefix = [start], env.letter(start)
    prev: Optional[Tuple[str, str]] = None

    while True:
        acts = valid_actions(env, path)
        s = prefix
        if not acts:                                   # beco sem saída antes de min_len
            if learn and prev:
                agent.update(prev[0], prev[1], FAIL_REWARD, None, ())
            return EpisodeResult(prefix, False, FAIL_REWARD, None)

        names = list(acts)
        if learn and prev:
            agent.update(prev[0], prev[1], STEP_REWARD, s, names)

        a = agent.choose(s, names, mode)
        if a == STOP:
            conf, x = None, None
            if estimator is not None:                  # previsão ANTES do dicionário
                x = estimator.features(prefix, agent.value(s, STOP), env.max_len)
                conf = estimator.predict(x)
            valid = dic.is_word(prefix)
            reward = float(word_score(prefix)) if valid else FAIL_REWARD
            if learn:
                agent.update(s, STOP, reward, None, ())
            if estimator is not None and learn_estimator and x is not None:
                estimator.update(x, 1.0 if valid else 0.0)
            return EpisodeResult(prefix, valid, reward, conf)

        path.append(acts[a])                           # type: ignore[arg-type]
        prefix += a
        prev = (s, a)


@dataclass
class Config:
    episodios: int = 5000
    avaliacao: int = 1000
    tamanho: int = 5
    min_len: int = 3
    max_len: int = 5
    alpha: float = 0.2
    gamma: float = 0.95
    eps_ini: float = 0.3
    eps_fim: float = 0.05
    seed: int = 42


def train(cfg: Config, dic: Dictionary) -> Tuple[QAgent, ConfidenceEstimator, dict]:
    env = WordGridEnv(cfg.tamanho, cfg.min_len, cfg.max_len, rng=random.Random(cfg.seed))
    agent = QAgent(cfg.alpha, cfg.gamma, cfg.eps_ini, seed=cfg.seed + 1)
    est = ConfidenceEstimator()
    ps: List[float] = []
    ys: List[float] = []
    rewards: List[float] = []
    found: Counter = Counter()
    passo = max(1, cfg.episodios // 10)

    for ep in range(1, cfg.episodios + 1):
        frac = (ep - 1) / max(1, cfg.episodios - 1)
        agent.epsilon = cfg.eps_ini + (cfg.eps_fim - cfg.eps_ini) * frac
        r = run_episode(env, dic, agent, "epsilon", learn=True,
                        estimator=est, learn_estimator=True)
        rewards.append(r.reward)
        if r.confidence is not None:
            ps.append(r.confidence)
            ys.append(1.0 if r.valid else 0.0)
        if r.valid:
            found[r.word] += 1
        if ep % passo == 0:
            rec = rewards[-passo:]
            log.info("ep %d/%d | recompensa média %.2f | eps %.3f | palavras distintas %d",
                     ep, cfg.episodios, sum(rec) / len(rec), agent.epsilon, len(found))

    base = prequential_base_rate(ys)
    stats = {
        "episodios": cfg.episodios,
        "recompensa_media": round(sum(rewards) / len(rewards), 4) if rewards else None,
        "tentativas_avaliadas": len(ys),
        "palavras_validas": int(sum(ys)),
        "palavras_distintas": len(found),
        "top_palavras": found.most_common(15),
        "confianca": {
            "brier_estimador": round(brier(ps, ys), 4),
            "brier_linha_base": round(brier(base, ys), 4),
            "ece_estimador": round(ece(ps, ys), 4),
            "supera_linha_base": bool(ps) and brier(ps, ys) < brier(base, ys),
        },
        "tamanho_tabela_q": len(agent.q),
    }
    return agent, est, stats


def evaluate(cfg: Config, dic: Dictionary, agent: QAgent) -> dict:
    """Guloso vs. aleatório nas mesmas grades e posições iniciais."""
    out = {}
    for nome, pol, mode in (("agente_guloso", agent, "greedy"),
                            ("aleatorio", QAgent(seed=cfg.seed + 2), "random")):
        env = WordGridEnv(cfg.tamanho, cfg.min_len, cfg.max_len,
                          rng=random.Random(cfg.seed + 100_000))
        res = [run_episode(env, dic, pol, mode, learn=False) for _ in range(cfg.avaliacao)]
        k = sum(r.valid for r in res)
        lo, hi = wilson(k, len(res))
        out[nome] = {
            "taxa_palavra_valida": round(k / len(res), 4),
            "ic95_wilson": [round(lo, 4), round(hi, 4)],
            "recompensa_media": round(sum(r.reward for r in res) / len(res), 4),
        }
    g, a = out["agente_guloso"], out["aleatorio"]
    out["conclusao"] = ("agente supera o aleatório (ICs não se sobrepõem)"
                        if g["ic95_wilson"][0] > a["ic95_wilson"][1]
                        else "sem evidência de superioridade (ICs se sobrepõem)")
    return out


def chess_features(n: int, max_moves: int, seed: int) -> List[dict]:
    """Partidas com lances legais aleatórios — só dados estruturados."""
    if not HAS_CHESS or n <= 0:
        return []
    rng = random.Random(seed)
    vals = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}
    out = []
    for _ in range(n):
        board, m = chess.Board(), 0
        while not board.is_game_over() and m < max_moves:
            board.push(rng.choice(list(board.legal_moves)))
            m += 1
        mat = sum((len(board.pieces(p, chess.WHITE)) - len(board.pieces(p, chess.BLACK))) * v
                  for p, v in vals.items())
        out.append({"lances": m, "material": mat, "fim_de_jogo": board.is_game_over()})
    return out


# ---------------------------------------------------------------------------
# 7. Autotestes
# ---------------------------------------------------------------------------

def run_selftests() -> int:
    falhas: List[str] = []

    def check(cond: bool, nome: str) -> None:
        print(("  OK   " if cond else "  FALHA ") + nome)
        if not cond:
            falhas.append(nome)

    pares = ["AB", "CA", "TO", "NO", "ST", "HE"]
    check(any(not np.allclose(word_to_vector(p), word_to_vector(p[::-1])) for p in pares),
          "vetor sensível à ordem")
    check(abs(np.linalg.norm(word_to_vector("CAT")) - 1.0) < 1e-9, "vetor normalizado")
    check(word_score("CAT") == 15, "pontuação Scrabble (CAT = 5×3)")

    env = WordGridEnv(size=4, rng=random.Random(1))
    env.reset()
    check(env.path_is_legal([(0, 0), (0, 1), (1, 2)]), "caminho adjacente é legal")
    check(not env.path_is_legal([(0, 0), (0, 1), (0, 0)]), "reuso de célula é ilegal")
    check(not env.path_is_legal([(0, 0), (2, 2)]), "salto não adjacente é ilegal")
    check(len(env.neighbors((0, 0))) == 3 and len(env.neighbors((1, 1))) == 8, "vizinhança")

    path = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]  # len == max_len (5)
    check(list(valid_actions(env, path)) == [STOP], "em max_len só PARAR")
    check(STOP not in valid_actions(env, [(0, 0)]), "PARAR bloqueado antes de min_len")

    d = Dictionary("embedded")
    check(d.is_word("cat") and not d.is_word("xqz"), "dicionário embutido")

    d2 = Dictionary("embedded")
    d2.backend, d2.cache_file = "api", None
    d2._api = lambda w: None  # type: ignore[assignment]   # simula rede fora do ar
    check(d2.lookup("cat") is None and "cat" not in d2.cache, "desconhecido não entra no cache")

    check(brier([1.0, 0.0], [1.0, 0.0]) == 0.0 and ece([1.0, 0.0], [1.0, 0.0]) == 0.0,
          "métricas: previsão perfeita = 0")
    lo, hi = wilson(3, 10)
    check(0.0 <= lo < 0.3 < hi <= 1.0, "intervalo de Wilson")

    cfg = Config(episodios=300, avaliacao=50, seed=3)
    logging.disable(logging.INFO)
    a1, _, s1 = train(cfg, Dictionary("embedded"))
    a2, _, s2 = train(cfg, Dictionary("embedded"))
    logging.disable(logging.NOTSET)
    check(a1.q == a2.q and s1 == s2, "determinismo com mesma seed")

    print(f"\n{len(falhas)} falha(s).")
    return 1 if falhas else 0


# ---------------------------------------------------------------------------
# 8. CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Word RL Lab v2")
    ap.add_argument("--episodios", type=int, default=5000)
    ap.add_argument("--avaliacao", type=int, default=1000)
    ap.add_argument("--tamanho", type=int, default=5)
    ap.add_argument("--min-len", type=int, default=3)
    ap.add_argument("--max-len", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--dicionario", choices=["auto", "embedded", "wordnet", "api"],
                    default="embedded")
    ap.add_argument("--baixar-wordnet", action="store_true")
    ap.add_argument("--xadrez", type=int, default=0, help="partidas aleatórias auxiliares")
    ap.add_argument("--saida", help="grava o relatório JSON neste arquivo")
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args(argv)

    if a.autoteste:
        return run_selftests()
    if not (2 <= a.min_len <= a.max_len) or a.tamanho < 2 or a.episodios < 1 or a.avaliacao < 1:
        print("Parâmetros inválidos.", file=sys.stderr)
        return 2

    cfg = Config(episodios=a.episodios, avaliacao=a.avaliacao, tamanho=a.tamanho,
                 min_len=a.min_len, max_len=a.max_len, seed=a.seed)
    try:
        dic = Dictionary(a.dicionario, allow_download=a.baixar_wordnet)
    except (RuntimeError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2

    agent, _, treino = train(cfg, dic)
    avaliacao = evaluate(cfg, dic, agent)
    dic.save()

    relatorio = {
        "versao": VERSAO,
        "config": asdict(cfg),
        "dicionario": dic.backend,
        "consultas_sem_resposta": dic.unknown,
        "treino": treino,
        "avaliacao": avaliacao,
        "xadrez": chess_features(a.xadrez, 40, a.seed),
        "nota": "Calibração de confiança mede previsão, não consciência. Não é AGI/ASI.",
    }
    texto = json.dumps(relatorio, ensure_ascii=False, indent=2)
    print(texto)
    if a.saida:
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
