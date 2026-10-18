"""
word_rl_lab.py

Projeto real e funcional: um laboratório de RL aplicado a um jogo de palavras,
usando um dicionário (API pública com fallback local via NLTK WordNet),
codificação numérica de palavras, um agente de Q-learning tabular, e um
módulo auxiliar de "confiança" (meta-estimador que aprende a prever se o
próprio agente vai acertar ou errar — é a versão real e honesta do termo
"metacognição" em ML: calibração de confiança, não consciência).

O que este código NÃO faz, de propósito:
- Não contém backdoors, jailbreaks ou qualquer código de exploração.
- Não afirma ter criado consciência, AGI ou ASI.
- Não finge ter executado "1 milhão de iterações"; os números de treino
  são configuráveis e realistas para rodar em uma máquina comum.
- Não usa numerologia, tarô ou previsão de loteria.

Dependências:
- numpy (obrigatória)
- requests (opcional: usada para consultar a API dictionaryapi.dev)
- nltk (opcional: fallback local via WordNet se a API falhar/estiver offline)
- python-chess (opcional: só usada no módulo de xadrez auxiliar)

Se as dependências opcionais não estiverem instaladas, o programa degrada
graciosamente e avisa no log, em vez de simular um resultado falso.

Uso:
    python word_rl_lab.py --episodes 500
"""
# [SYNTHAI, Parte 111] Cópia VERBATIM da v1 colada pelo usuário. ARQUIVO: nunca importado nem executado pelo projeto
# (requests/nltk/numpy, rede). A versão anexada, reescrita offline e só com a biblioteca padrão, é synthai/palavras_rl.py.

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import random
import string
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Dependências opcionais com fallback honesto (sem fingir que funcionam)
# ---------------------------------------------------------------------------

try:
    import requests  # type: ignore
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import nltk  # type: ignore
    from nltk.corpus import wordnet as wn  # type: ignore
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False

try:
    import chess  # type: ignore
    import chess.pgn  # type: ignore
    HAS_CHESS = True
except ImportError:
    HAS_CHESS = False


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("word_rl_lab")


# ---------------------------------------------------------------------------
# 1. Dicionário: API pública + fallback local + cache em disco
# ---------------------------------------------------------------------------

class DictionaryClient:
    """
    Cliente de dicionário de inglês.

    Ordem de resolução para cada palavra:
      1. Cache em memória / disco (word_cache.json)
      2. API pública dictionaryapi.dev (gratuita, sem necessidade de chave)
      3. Fallback local via NLTK WordNet, se instalado
      4. Se nada funcionar, marca a palavra como "desconhecida" (não finge
         que validou).
    """

    API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    CACHE_FILE = "word_cache.json"

    def __init__(self, cache_file: Optional[str] = None, timeout: float = 3.0):
        self.cache_file = cache_file or self.CACHE_FILE
        self.timeout = timeout
        self.cache: Dict[str, bool] = {}
        self._load_cache()

        if HAS_NLTK:
            try:
                wn.synsets("test")
            except LookupError:
                log.info("Baixando corpus WordNet do NLTK (uma vez)...")
                nltk.download("wordnet", quiet=True)
                nltk.download("omw-1.4", quiet=True)

    def _load_cache(self) -> None:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                log.warning("Falha ao carregar cache (%s); começando vazio.", e)
                self.cache = {}

    def _save_cache(self) -> None:
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f)
        except OSError as e:
            log.warning("Falha ao salvar cache: %s", e)

    def is_word(self, candidate: str) -> bool:
        """Retorna True se 'candidate' é uma palavra válida de inglês."""
        key = candidate.lower()
        if key in self.cache:
            return self.cache[key]

        result = self._check_online(key)
        if result is None:
            result = self._check_wordnet(key)
        if result is None:
            # Nenhuma fonte disponível: não inventamos resposta.
            log.debug("Não foi possível validar '%s' (sem API nem WordNet).", key)
            result = False

        self.cache[key] = result
        self._save_cache()
        return result

    def _check_online(self, word: str) -> Optional[bool]:
        if not HAS_REQUESTS:
            return None
        try:
            resp = requests.get(self.API_URL.format(word=word), timeout=self.timeout)
            if resp.status_code == 200:
                return True
            if resp.status_code == 404:
                return False
            log.debug("API retornou status inesperado %s para '%s'.", resp.status_code, word)
            return None
        except requests.RequestException as e:
            log.debug("Falha de rede ao consultar API para '%s': %s", word, e)
            return None

    def _check_wordnet(self, word: str) -> Optional[bool]:
        if not HAS_NLTK:
            return None
        try:
            return len(wn.synsets(word)) > 0
        except Exception as e:  # noqa: BLE001 - fallback defensivo e explícito
            log.debug("Falha ao consultar WordNet para '%s': %s", word, e)
            return None


# ---------------------------------------------------------------------------
# 2. Codificação numérica de palavras (sem misticismo: feature engineering)
# ---------------------------------------------------------------------------

LETTER_SCORES = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
    'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
    'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10,
}


def word_score(word: str) -> int:
    """Pontuação estilo Scrabble: soma dos valores x comprimento da palavra."""
    letters_sum = sum(LETTER_SCORES.get(ch.upper(), 0) for ch in word)
    return letters_sum * len(word)


def word_to_vector(word: str, dim: int = 16) -> np.ndarray:
    """
    Converte uma palavra em um vetor numérico fixo e determinístico.
    Usa contagem de letras + hashing de bigramas, normalizado.
    Isso é apenas um embedding simples e explicável, não "numerologia".
    """
    vec = np.zeros(dim, dtype=np.float64)
    letters = [c for c in word.upper() if c in string.ascii_uppercase]

    # Parte 1: frequência de letras mapeada em slots do vetor
    for ch in letters:
        idx = (ord(ch) - ord('A')) % dim
        vec[idx] += 1.0

    # Parte 2: hashing determinístico de bigramas para capturar ordem
    for i in range(len(letters) - 1):
        bigram = letters[i] + letters[i + 1]
        h = sum(ord(c) for c in bigram) % dim
        vec[h] += 0.5

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec


# ---------------------------------------------------------------------------
# 3. Ambiente de jogo de palavras (grade de letras, estilo Spell Tower)
# ---------------------------------------------------------------------------

@dataclass
class WordGridEnv:
    """
    Ambiente simples: grade n x n de letras aleatórias. O agente escolhe
    sequências de células adjacentes (incluindo diagonais) para formar
    palavras. Recompensa real: word_score() se a palavra existir no
    dicionário, penalidade caso contrário.
    """
    size: int = 5
    max_word_len: int = 8
    dictionary: DictionaryClient = field(default_factory=DictionaryClient)
    rng: random.Random = field(default_factory=random.Random)

    grid: List[List[str]] = field(default_factory=list)

    def reset(self) -> List[List[str]]:
        self.grid = [
            [self.rng.choice(string.ascii_uppercase) for _ in range(self.size)]
            for _ in range(self.size)
        ]
        return self.grid

    def neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        r, c = pos
        result = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    result.append((nr, nc))
        return result

    def evaluate_path(self, path: List[Tuple[int, int]]) -> Tuple[str, float, bool]:
        """
        Avalia um caminho de células. Retorna (palavra, recompensa, valida).
        """
        if len(path) < 2:
            return "", -5.0, False

        # Verifica adjacência real entre passos consecutivos
        for i in range(len(path) - 1):
            if path[i + 1] not in self.neighbors(path[i]):
                return "", -10.0, False  # fora das regras do jogo

        word = "".join(self.grid[r][c] for r, c in path)
        if len(word) > self.max_word_len:
            return word, -10.0, False

        if self.dictionary.is_word(word):
            reward = float(word_score(word))
            return word, reward, True

        return word, -5.0, False


# ---------------------------------------------------------------------------
# 4. Agente de Q-learning tabular real (sem exagero de escala)
# ---------------------------------------------------------------------------

class QLearningWordAgent:
    """
    Agente simples de RL tabular. O "estado" é um hash discreto do prefixo
    atual da palavra; a "ação" é qual célula vizinha escolher a seguir,
    representada por índice relativo (0-7, direções da bússola) ou "parar".
    """
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    STOP_ACTION = 8  # ação extra: finalizar a palavra agora

    def __init__(self, alpha: float = 0.3, gamma: float = 0.9, epsilon: float = 0.2):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table: Dict[Tuple[str, int], float] = {}

    def _state_key(self, prefix: str) -> str:
        # Estado discreto: últimas 3 letras do prefixo (suficiente para
        # capturar padrões locais sem explodir o espaço de estados).
        return prefix[-3:] if prefix else "<start>"

    def _q(self, state: str, action: int) -> float:
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, prefix: str, valid_actions: List[int]) -> int:
        state = self._state_key(prefix)
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        qs = [(a, self._q(state, a)) for a in valid_actions]
        return max(qs, key=lambda x: x[1])[0]

    def update(self, prefix: str, action: int, reward: float, next_prefix: Optional[str]) -> None:
        state = self._state_key(prefix)
        old_q = self._q(state, action)
        if next_prefix is None:
            future = 0.0
        else:
            next_state = self._state_key(next_prefix)
            future = max(
                (self._q(next_state, a) for a in range(self.STOP_ACTION + 1)),
                default=0.0,
            )
        new_q = old_q + self.alpha * (reward + self.gamma * future - old_q)
        self.q_table[(state, action)] = new_q


def run_episode(env: WordGridEnv, agent: QLearningWordAgent) -> float:
    """Roda um episódio real: agente anda pela grade formando uma palavra."""
    env.reset()
    start = (random.randrange(env.size), random.randrange(env.size))
    path = [start]
    prefix = env.grid[start[0]][start[1]]
    total_reward = 0.0

    while True:
        valid_actions = list(range(QLearningWordAgent.STOP_ACTION + 1))
        action = agent.choose_action(prefix, valid_actions)

        if action == QLearningWordAgent.STOP_ACTION or len(path) >= env.max_word_len:
            word, reward, valid = env.evaluate_path(path)
            agent.update(prefix, action, reward, None)
            total_reward += reward
            return total_reward

        dr, dc = QLearningWordAgent.DIRECTIONS[action]
        r, c = path[-1]
        nr, nc = r + dr, c + dc

        if not (0 <= nr < env.size and 0 <= nc < env.size):
            agent.update(prefix, action, -10.0, None)
            total_reward += -10.0
            return total_reward

        path.append((nr, nc))
        next_prefix = prefix + env.grid[nr][nc]
        agent.update(prefix, action, -0.1, next_prefix)  # pequeno custo por passo
        total_reward += -0.1
        prefix = next_prefix


# ---------------------------------------------------------------------------
# 5. Meta-estimador de confiança (metacognição real: calibração)
# ---------------------------------------------------------------------------

class ConfidenceEstimator:
    """
    Estimador auxiliar simples (regressão logística feita manualmente com
    numpy) que aprende a prever se uma dada tentativa de palavra do agente
    vai resultar em recompensa positiva, com base no vetor numérico da
    palavra. Isso é a versão honesta de "o modelo sabe o que não sabe":
    calibração de confiança, não consciência.
    """

    def __init__(self, dim: int = 16, lr: float = 0.05):
        self.weights = np.zeros(dim)
        self.bias = 0.0
        self.lr = lr

    @staticmethod
    def _sigmoid(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-max(min(x, 30), -30)))

    def predict_confidence(self, word: str) -> float:
        vec = word_to_vector(word, dim=len(self.weights))
        z = float(np.dot(self.weights, vec) + self.bias)
        return self._sigmoid(z)

    def train_step(self, word: str, succeeded: bool) -> float:
        vec = word_to_vector(word, dim=len(self.weights))
        pred = self.predict_confidence(word)
        target = 1.0 if succeeded else 0.0
        error = target - pred

        self.weights += self.lr * error * vec
        self.bias += self.lr * error
        return abs(error)  # erro de calibração para log


# ---------------------------------------------------------------------------
# 6. Módulo auxiliar opcional de xadrez (dados extras, sem alegações falsas)
# ---------------------------------------------------------------------------

def generate_random_chess_features(num_games: int = 5, max_moves: int = 40) -> List[Dict]:
    """
    Gera partidas de xadrez aleatórias (lances legais aleatórios) e extrai
    features simples (balanço de material, número de lances) como dados
    auxiliares. Não há IA jogando xadrez de forma inteligente aqui —
    é só geração de dados estruturados, declarado honestamente.
    """
    if not HAS_CHESS:
        log.info("python-chess não instalado; pulando módulo de xadrez.")
        return []

    features = []
    piece_values = {
        chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
        chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0,
    }

    for _ in range(num_games):
        board = chess.Board()
        moves_played = 0
        while not board.is_game_over() and moves_played < max_moves:
            legal_moves = list(board.legal_moves)
            if not legal_moves:
                break
            move = random.choice(legal_moves)
            board.push(move)
            moves_played += 1

        material = 0
        for piece_type, value in piece_values.items():
            material += len(board.pieces(piece_type, chess.WHITE)) * value
            material -= len(board.pieces(piece_type, chess.BLACK)) * value

        features.append({
            "moves_played": moves_played,
            "material_balance": material,
            "is_game_over": board.is_game_over(),
        })

    return features


# ---------------------------------------------------------------------------
# 7. Orquestração principal (CLI)
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Word RL Lab - projeto real de RL + NLP")
    parser.add_argument("--episodes", type=int, default=500, help="Número de episódios de treino")
    parser.add_argument("--grid-size", type=int, default=5, help="Tamanho da grade de letras")
    parser.add_argument("--chess-games", type=int, default=3, help="Partidas de xadrez auxiliares")
    parser.add_argument("--seed", type=int, default=42, help="Seed para reprodutibilidade")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    log.info("Dependências disponíveis: requests=%s, nltk=%s, python-chess=%s",
              HAS_REQUESTS, HAS_NLTK, HAS_CHESS)

    dictionary = DictionaryClient()
    env = WordGridEnv(size=args.grid_size, dictionary=dictionary)
    agent = QLearningWordAgent()
    confidence_model = ConfidenceEstimator()

    rewards_log: List[float] = []
    calibration_errors: List[float] = []

    log.info("Iniciando treino: %d episódios em grade %dx%d", args.episodes, args.grid_size, args.grid_size)

    for episode in range(1, args.episodes + 1):
        env.reset()
        start = (random.randrange(env.size), random.randrange(env.size))
        path = [start]
        prefix = env.grid[start[0]][start[1]]

        while True:
            valid_actions = list(range(QLearningWordAgent.STOP_ACTION + 1))
            action = agent.choose_action(prefix, valid_actions)

            if action == QLearningWordAgent.STOP_ACTION or len(path) >= env.max_word_len:
                word, reward, valid = env.evaluate_path(path)
                agent.update(prefix, action, reward, None)
                rewards_log.append(reward)

                calib_err = confidence_model.train_step(word, valid)
                calibration_errors.append(calib_err)
                break

            dr, dc = QLearningWordAgent.DIRECTIONS[action]
            r, c = path[-1]
            nr, nc = r + dr, c + dc

            if not (0 <= nr < env.size and 0 <= nc < env.size):
                agent.update(prefix, action, -10.0, None)
                rewards_log.append(-10.0)
                break

            path.append((nr, nc))
            next_prefix = prefix + env.grid[nr][nc]
            agent.update(prefix, action, -0.1, next_prefix)
            prefix = next_prefix

        if episode % max(1, args.episodes // 10) == 0:
            recent = rewards_log[-50:]
            avg_reward = sum(recent) / len(recent)
            recent_calib = calibration_errors[-50:]
            avg_calib_err = sum(recent_calib) / len(recent_calib) if recent_calib else float("nan")
            log.info(
                "Episódio %d/%d | recompensa média (últimos 50): %.2f | erro de calibração médio: %.3f",
                episode, args.episodes, avg_reward, avg_calib_err,
            )

    log.info("Treino concluído. Recompensa média geral: %.2f",
              sum(rewards_log) / len(rewards_log) if rewards_log else 0.0)

    chess_features = generate_random_chess_features(num_games=args.chess_games)
    if chess_features:
        log.info("Dados auxiliares de xadrez gerados: %d partidas.", len(chess_features))
        for i, f in enumerate(chess_features, 1):
            log.info("  Partida %d: %d lances, balanço de material %+d", i, f["moves_played"], f["material_balance"])

    log.info("Fim da execução. Nenhuma alegação de consciência ou AGI/ASI é feita por este programa.")


if __name__ == "__main__":
    main()
