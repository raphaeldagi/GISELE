"""NEXUS-RAPHAEL anexado à SYNTHAI (Parte 109). Reescrita do zero, só biblioteca padrão e OFFLINE, do código NEXUS-RAPHAEL v0.1.0 que
o usuário colou ("Anexe tudo ao nosso código"); a cópia verbatim fica em externos/nexus_raphael/nexus_raphael_v0_1_0_colado.py e
nunca é importada (regra da Parte 72: código vindo de texto é auditado pela árvore sintática e reescrito, com um teste por defeito).

Mesma API e mesmos números do original, com quatro mudanças, cada uma com o seu teste (synthai/testes_parte109.py):
  1. REDE FORA. DictionaryClient só consulta o léxico offline. O original tinha urllib e as URLs de dictionaryapi.dev e DuckDuckGo,
     desligadas por padrão; aqui o caminho de rede não existe (11ª recusa da família, Partes 84/93/102/103).
  2. AUDITORIA POR AST. A security_audit original procurava o TEXTO "exec(" e "eval(" e se acusava a si mesma, porque o próprio texto
     contém essas strings dentro da checagem; o original, rodado, sairia com código 1. Aqui contam-se CHAMADAS reais (ast.Call).
  3. O JOGO RAPHAEL SEPARA QUEM DESVIA. No original os DOIS jogadores desviam (o lance t de qualquer paridade), o que confunde a
     hipótese "o desvio DO JOGADOR 0 aumenta as vitórias". `quem_desvia=None` reproduz o original; `quem_desvia=0` testa a hipótese.
  4. SEM DISCO. run_all não grava nexus_state/last_report.json, a menos que se passe `salvar=`.
Acrescentado: kuhn_exato (o valor do Kuhn simplificado por enumeração, sem simular)."""

from __future__ import annotations

import ast
import hashlib
import inspect
import math
import random
import re
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from fractions import Fraction

VERSION = "0.1.0-synthai"
SYSTEM_NAME = "NEXUS-RAPHAEL (anexado à SYNTHAI)"
STATUS = {"agi": False, "asi": False, "phenomenal_consciousness": "inconclusive", "functional_self_model": True}

_D = lambda pos, d, lang="en": {"pos": pos, "def": d, "lang": lang}
OFFLINE_LEXICON = {
    "nexus": _D("noun", "ponto de ligação entre partes de um sistema", "pt"),
    "raphael": _D("name", "nome do ambiente de jogo deste projeto", "pt"),
    "word": _D("noun", "unidade lexical com forma e sentido"),
    "number": _D("noun", "objeto matemático usado para contar ou medir"),
    "mind": _D("noun", "conjunto de processos cognitivos, não um módulo mágico"),
    "doubt": _D("noun", "estado de incerteza que pode gerar hipóteses"),
    "proof": _D("noun", "argumento ou medição que sustenta uma afirmação"),
    "error": _D("noun", "desvio entre previsão e observação"),
    "game": _D("noun", "sistema de regras, jogadas e critérios de vitória"),
    "rule": _D("noun", "restrição explícita sobre ações permitidas"),
    "logic": _D("noun", "estudo da consequência formal entre premissas"),
    "chance": _D("noun", "incerteza quantificável por probabilidade"),
    "memory": _D("noun", "registro recuperável de estados anteriores"),
    "future": _D("noun", "estado ainda não observado, alvo de previsão"),
    "past": _D("noun", "histórico já registrado pelo sistema"),
    "agent": _D("noun", "processo que escolhe ações segundo uma estratégia"),
    "graph": _D("noun", "conjunto de nós ligados por arestas"),
    "vector": _D("noun", "lista ordenada de números"),
    "language": _D("noun", "sistema de sinais convencionais"),
    "test": _D("noun", "procedimento que pode falhar e assim informar"),
    "learn": _D("verb", "atualizar parâmetros com base em observações"),
    "predict": _D("verb", "emitir uma estimativa antes da observação"),
    "audit": _D("verb", "verificar consistência, segurança e reprodutibilidade"),
    "play": _D("verb", "executar jogadas dentro de regras"),
    "draw": _D("verb", "selecionar um resultado de uma distribuição"),
    "win": _D("verb", "satisfazer o critério de vitória"),
    "lose": _D("verb", "falhar o critério de vitória"),
    "true": _D("adj", "conforme a observação ou a regra adotada"),
    "false": _D("adj", "em conflito com a observação ou a regra"),
    "open": _D("adj", "ainda sem conclusão suficiente"),
}


@dataclass
class Config:
    seed: int = 7
    graph_nodes: int = 910
    graph_layers: int = 10
    demo_graph_nodes: int = 910
    raphael_games: int = 60
    raphael_turns: int = 12
    learning_steps: int = 80
    prob_trials: int = 200
    max_ops: int = 20000
    ewc_lambda: float = 8.0


class AuditLog:
    def __init__(self):
        self.records = []

    def add(self, kind, payload):
        rec = {"n": len(self.records), "kind": kind, "payload": payload}   # contador no lugar de time.time(): reprodutível
        self.records.append(rec)
        return rec


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def softmax(xs):
    if not xs:
        return []
    m = max(xs)
    ex = [math.exp(x - m) for x in xs]
    s = sum(ex) or 1.0
    return [e / s for e in ex]


def entropy(ps):
    return -sum(p * math.log(p) for p in ps if p > 0)


def kl_divergence(p, q, eps=1e-12):
    return sum((pi + eps) * math.log((pi + eps) / (qi + eps)) for pi, qi in zip(p, q))


def brier(ps, ys):
    if not ps:
        return 1.0
    return sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ps)


def calibration_error(ps, ys, bins=5):
    if not ps:
        return 1.0
    buckets = [[] for _ in range(bins)]
    for p, y in zip(ps, ys):
        buckets[min(bins - 1, int(clamp(p, 0, 0.999) * bins))].append((p, y))
    err = n = 0
    for b in buckets:
        if b:
            err += len(b) * abs(sum(p for p, _ in b) / len(b) - sum(y for _, y in b) / len(b))
            n += len(b)
    return err / n if n else 1.0


def cosine_double(theta):
    direct = math.cos(2 * theta)
    identity = 2 * math.cos(theta) ** 2 - 1
    return direct, identity, abs(direct - identity)


def double_angle_similarity(v, w):
    dot = sum(a * b for a, b in zip(v, w))
    nv = math.sqrt(sum(a * a for a in v)) or 1.0
    nw = math.sqrt(sum(b * b for b in w)) or 1.0
    c = clamp(dot / (nv * nw), -1.0, 1.0)
    return 2 * c * c - 1


# --- representação ---

def a1z26_encode(text):
    return [ord(ch) - 96 for ch in text.lower() if "a" <= ch <= "z"]


def a1z26_decode(nums):
    if any(not 1 <= int(n) <= 26 for n in nums):
        return None
    return "".join(chr(int(n) + 96) for n in nums)


def utf8_encode(text):
    return list(text.encode("utf-8"))


def utf8_decode(nums):
    return bytes(int(n) for n in nums).decode("utf-8")


def stable_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_trick(text, dim=16):
    vec = [0.0] * dim
    for tok in re.findall(r"[a-z0-9]+", text.lower()) or [text.lower()]:
        dg = hashlib.sha256(tok.encode()).digest()
        vec[int.from_bytes(dg[:2], "big") % dim] += 1.0 if dg[2] % 2 == 0 else -1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def experimental_numerology(text):
    """Interpretativo, não validado (o próprio original diz isso); fica marcado sem alegação preditiva."""
    total = sum(a1z26_encode(text))
    digital = total
    while digital > 9:
        digital = sum(int(d) for d in str(digital))
    return {"status": "EXPERIMENTAL_NON_VALIDATED", "sum": total, "digital_root": digital, "predictive_claim": False}


class Representation:
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.cooc = defaultdict(Counter)

    def observe_sentence(self, text):
        toks = re.findall(r"[a-zA-Z]+", text.lower())
        for i, tok in enumerate(toks):
            for j in range(max(0, i - 2), min(len(toks), i + 3)):
                if i != j:
                    self.cooc[tok][toks[j]] += 1

    def encode(self, text):
        letters = re.sub(r"[^a-zA-Z]", "", text).lower()
        return {
            "raw": text, "a1z26": a1z26_encode(letters), "utf8": utf8_encode(text), "hash": stable_hash(text),
            "vector": hash_trick(text),
            "known_tokens": [t for t in re.findall(r"[a-zA-Z]+", text.lower()) if t in self.lexicon],
            "reversible_a1z26": a1z26_decode(a1z26_encode(letters)) == letters,
            "numerology": experimental_numerology(letters),
        }

    def nearest(self, text, k=3):
        q = hash_trick(text)
        sc = sorted(((w, double_angle_similarity(q, hash_trick(w))) for w in self.lexicon), key=lambda x: x[1], reverse=True)
        return sc[:k]


def generate_nonce(rng, lexicon):
    syl = ["nex", "ra", "pha", "el", "ium", "qua", "lor", "ven", "tor", "sis"]
    for _ in range(30):
        w = "".join(rng.choice(syl) for _ in range(rng.randint(2, 3)))
        if w not in lexicon and 4 <= len(w) <= 16:
            return w
    return "nexelium"


def propose_meaning(word):
    morf = {"nex": "ligação", "raph": "nome do jogo", "el": "agente", "ium": "domínio", "qua": "quatro", "lor": "padrão",
            "ven": "vinda", "tor": "agente", "sis": "processo"}
    hits = [m for m in morf if m in word]
    return {"word": word, "proposed_meaning": " + ".join(morf[m] for m in hits) if hits else "sem morfema conhecido",
            "consistency": round(len(hits) / max(1, len(word) // 3), 3), "external_occurrences_checked": False, "status": "hypothesis"}


# --- cognição e metacognição ---

class Cognition:
    def __init__(self):
        self.rules = [
            ("double_minus_one", lambda xs: all(xs[i + 1] == 2 * xs[i] - 1 for i in range(len(xs) - 1))),
            ("times_two", lambda xs: all(xs[i + 1] == 2 * xs[i] for i in range(len(xs) - 1))),
            ("constant_second_diff", self._second_diff),
        ]

    @staticmethod
    def _second_diff(xs):
        if len(xs) < 4:
            return False
        d1 = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
        d2 = [d1[i + 1] - d1[i] for i in range(len(d1) - 1)]
        return all(abs(d - d2[0]) < 1e-9 for d in d2)

    def infer_sequence(self, xs):
        hits = [nome for nome, fn in self.rules if fn(xs)]
        used = hits[0] if hits else None
        pred = None
        if used == "double_minus_one":
            pred = 2 * xs[-1] - 1
        elif used == "times_two":
            pred = 2 * xs[-1]
        elif used == "constant_second_diff":
            pred = xs[-1] + (xs[-1] - xs[-2]) + ((xs[-1] - xs[-2]) - (xs[-2] - xs[-3]))
        return {"hypotheses": hits, "used": used, "prediction": pred, "input": list(xs)}


class MetaCognition:
    def __init__(self, log):
        self.log = log

    def evaluate(self, result, truth=None):
        pred = result.get("prediction")
        covered = pred is not None
        error = None if truth is None or pred is None else abs(float(pred) - float(truth))
        rc = 0.55 if covered else 0.15
        if error is not None:
            rc = clamp(1.0 - error / (abs(float(truth)) + 1.0), 0.01, 0.99)
        levels = {
            "linear": rc,
            "logarithmic": clamp(-math.log(max(1e-6, 1 - rc)) / 5, 0, 1),
            "geometric": math.sqrt(rc * (0.5 + 0.5 * rc)),
            "algebraic": clamp(rc ** 2 * (3 - 2 * rc), 0, 1),
            "homologous": rc,
            "heterologous": 1.0 - calibration_error([rc], [1.0 if error == 0 else 0.0]),
        }
        rec = {"response": pred, "confidence": rc, "hypotheses": result.get("hypotheses", []), "error": error, "levels": levels,
               "overconfidence": rc > 0.8 and error not in (0, None)}
        self.log.add("metacognition", rec)
        return rec


class RecursiveMeta:
    def evaluate(self, meta):
        spread = max(meta["levels"].values()) - min(meta["levels"].values())
        return {"strategy_stable": spread < 0.35, "spread": spread, "does_not_prove_consciousness": True}


# --- probabilidade ---

class AdaptiveEstimator:
    def __init__(self):
        self.a = self.b = 1.0
        self.ps, self.ys = [], []

    def predict(self):
        return self.a / (self.a + self.b)

    def update(self, y):
        self.ps.append(self.predict())
        self.ys.append(y)
        self.a += y
        self.b += 1 - y

    def interval(self):
        n, p = self.a + self.b, self.predict()
        se = math.sqrt(max(p * (1 - p), 1e-12) / n)
        return clamp(p - 1.96 * se, 0, 1), clamp(p + 1.96 * se, 0, 1)


def probability_experiment(cfg):
    """Igual ao original: Bernoulli p=0,72, 200 ensaios; Beta(1,1) sequencial contra a referência constante 0,5."""
    rng = random.Random(cfg.seed)
    true_p = 0.72
    ad = AdaptiveEstimator()
    ref_ps, ys = [], []
    for _ in range(cfg.prob_trials):
        y = 1.0 if rng.random() < true_p else 0.0
        ref_ps.append(0.5)
        ad.update(y)
        ys.append(y)
    ba, br = brier(ad.ps, ad.ys), brier(ref_ps, ys)
    return {"true_p": true_p, "adaptive_p": ad.predict(), "interval": ad.interval(), "brier_adaptive": ba, "brier_reference": br,
            "kl_to_truth": kl_divergence([ad.predict(), 1 - ad.predict()], [true_p, 1 - true_p]),
            "calibration_error": calibration_error(ad.ps, ad.ys), "supported": ba < br}


# --- agentes ---

AGENTS = ["criativo", "logico", "cetico", "socratico", "probabilistico", "matematico", "linguistico", "adversarial", "metacognitivo", "auditor"]


def agent_vote(name, xs):
    inf = Cognition().infer_sequence(xs)
    especiais = {
        "criativo": ("padrão poético *2", 2 * xs[-1]),
        "probabilistico": ("média dos incrementos", xs[-1] + (xs[-1] - xs[0]) / (len(xs) - 1)),
        "linguistico": ("sequência não é enunciado", None),
        "adversarial": ("hipótese oposta: último valor + 1", xs[-1] + 1),
    }
    claim, pred = especiais.get(name, (inf["used"] or "nenhuma regra", inf["prediction"]))
    return {"agent": name, "claim": claim, "prediction": pred}


def debate(xs, truth):
    votes = [agent_vote(n, xs) for n in AGENTS]
    preds = [v["prediction"] for v in votes if isinstance(v["prediction"], (int, float))]
    majority = Counter(round(p, 6) for p in preds).most_common(1)[0][0] if preds else None
    return {"votes": votes, "majority": majority, "majority_correct": majority is not None and abs(majority - truth) < 1e-9,
            "any_correct": any(v["prediction"] is not None and abs(v["prediction"] - truth) < 1e-9 for v in votes),
            "consensus_is_not_truth": True, "truth": truth}


# --- aprendizado contínuo (EWC) ---

class OnlineLogistic:
    def __init__(self, dim, lr=0.08, l2=1e-3, ewc=0.0):
        self.w, self.b = [0.0] * dim, 0.0
        self.lr, self.l2, self.ewc = lr, l2, ewc
        self.fisher, self.anchor = [0.0] * dim, [0.0] * dim

    def proba(self, x):
        z = clamp(self.b + sum(wi * xi for wi, xi in zip(self.w, x)), -20, 20)
        return 1 / (1 + math.exp(-z))

    def update(self, x, y):
        p = self.proba(x)
        g = p - y
        nw = []
        for i, (wi, xi) in enumerate(zip(self.w, x)):
            pen = self.l2 * wi + self.ewc * self.fisher[i] * (wi - self.anchor[i])
            nw.append(wi - self.lr * (g * xi + pen))
            self.fisher[i] = 0.95 * self.fisher[i] + 0.05 * (xi * g) ** 2
        self.w = nw
        self.b -= self.lr * g
        return p

    def snapshot(self):
        self.anchor = list(self.w)

    def accuracy(self, data):
        return sum(int((self.proba(x) >= 0.5) == bool(y)) for x, y in data) / len(data) if data else 0.0


def forgetting_experiment(cfg):
    rng = random.Random(cfg.seed + 3)

    def make(n, shift):
        out = []
        for _ in range(n):
            x = [rng.uniform(-1, 1) for _ in range(3)]
            out.append((x, 1.0 if x[0] + 0.2 * x[1] + shift > 0 else 0.0))
        return out

    ta, tb = make(cfg.learning_steps, 0.0), make(cfg.learning_steps, 0.8)
    plain, elastic = OnlineLogistic(3), OnlineLogistic(3, ewc=cfg.ewc_lambda)
    for m in (plain, elastic):
        for x, y in ta:
            m.update(x, y)
        m.snapshot()
    antes = {"plain": plain.accuracy(ta), "ewc": elastic.accuracy(ta)}
    for x, y in tb:
        plain.update(x, y)
        elastic.update(x, y)
    depois = {"plain": plain.accuracy(ta), "ewc": elastic.accuracy(ta)}
    return {"acc_a_before": antes, "acc_a_after": depois, "retention_gap": depois["ewc"] - depois["plain"],
            "supported": depois["ewc"] >= depois["plain"] - 1e-9}


# --- grafo síncrono/assíncrono ---

class ComputeGraph:
    def __init__(self, n, layers, seed, max_ops):
        self.n, self.layers, self.max_ops, self.ops = n, layers, max_ops, 0
        rng = random.Random(seed)
        self.adj = [[] for _ in range(n)]
        span = max(1, n // layers)
        for i in range(n):
            for k in range(2):
                self.adj[i].append((i + 1 + rng.randrange(span) + k) % n)
                self.ops += 1
                if self.ops >= max_ops:
                    break
        self.state = [0.0] * n
        self.lock = threading.Lock()

    def sync_pass(self, steps=1):
        for _ in range(steps):
            nxt = list(self.state)
            for i, vals in enumerate(self.adj):
                if self.ops >= self.max_ops:
                    self.state = nxt
                    return self.ops
                s = math.tanh(self.state[i] + 0.01 * ((i % 5) - 2))
                for j in vals:
                    nxt[j] += s / max(1, len(vals))
                    self.ops += 1
            self.state = nxt
        return self.ops

    def async_increment(self, workers=4, per_worker=25):
        """Threads no MESMO processo, com trava (não é processo novo nem replicação)."""
        def job():
            for _ in range(per_worker):
                with self.lock:
                    self.state[0] += 1
                    self.ops += 1
        with ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(lambda _: job(), range(workers)))
        return int(self.state[0])


# --- jogos ---

def kuhn_poker_value(seed, games=200):
    """O Kuhn simplificado do original, simulado (P0 aposta com K; com Q metade das vezes; nunca com J; P1 paga com Q ou K)."""
    rng = random.Random(seed)
    payout = 0
    for _ in range(games):
        deck = [1, 2, 3]
        rng.shuffle(deck)
        p0, p1 = deck[0], deck[1]
        if not (p0 == 3 or (p0 == 2 and rng.random() < 0.5)):
            payout -= 1
            continue
        payout += (2 if p0 > p1 else -2) if p1 >= 2 else 1
    return {"mean_payout_p0": payout / games, "games": games, "is_full_poker": False}


def kuhn_exato(p_aposta_q=Fraction(1, 2)):
    """O MESMO jogo, por enumeração das 6 distribuições equiprováveis (p0, p1 distintos), sem simular. Valor para o P0."""
    tot = Fraction(0)
    for p0 in (1, 2, 3):
        for p1 in (1, 2, 3):
            if p0 == p1:
                continue
            pa = Fraction(1) if p0 == 3 else (p_aposta_q if p0 == 2 else Fraction(0))
            apostou = (2 if p0 > p1 else -2) if p1 >= 2 else 1
            tot += Fraction(1, 6) * (pa * apostou + (1 - pa) * (-1))
    return tot


class RaphaelGame:
    """Tabuleiro 5×5; valor da casa = (soma a1z26 da palavra mod 13) + carta + 5 no nexo (2,2) − distância ao centro.
    `deviate` liga o desvio (jogar a 2ª melhor casa com prob. `rate`); `quem_desvia` = None (os dois, como no original) ou 0/1."""

    def __init__(self, seed, words, turns, deviate, rate=0.35, quem_desvia=None, agenda="original"):
        self.rng = random.Random(seed)
        self.words, self.turns, self.deviate, self.rate, self.quem = list(words), turns, deviate, rate, quem_desvia
        self.agenda = agenda   # "original": words[t]; "justa": words[t // 2] (a mesma palavra para os dois em cada rodada; P2717)
        self.size, self.nexus = 5, (2, 2)
        self.board, self.scores = {}, [0, 0]

    def card(self):
        return self.rng.choices([-1, 0, 1, 2], weights=[15, 35, 35, 15])[0]

    def value(self, cell, word, card):
        r, c = cell
        lex = sum(ord(ch) - 96 for ch in word if "a" <= ch <= "z") % 13
        return lex + card + (5 if cell == self.nexus else 0) - (abs(r - 2) + abs(c - 2))

    def play(self):
        unexpected = 0
        for t in range(self.turns):
            legal = [(r, c) for r in range(self.size) for c in range(self.size) if (r, c) not in self.board]
            if not legal:
                break
            idx = t if self.agenda == "original" else t // 2
            word, card = self.words[idx % len(self.words)], self.card()
            ranked = sorted(legal, key=lambda cell: self.value(cell, word, card), reverse=True)
            # o sorteio do desvio acontece em TODO lance (como no original), para que o fluxo do gerador seja o mesmo nos dois braços
            sorteio = self.deviate and len(ranked) > 1 and self.rng.random() < self.rate
            dev = sorteio and (self.quem is None or self.quem == t % 2)
            choice = ranked[1] if dev else ranked[0]
            unexpected += int(dev)
            self.board[choice] = t % 2
            self.scores[t % 2] += self.value(choice, word, card)
        s0, s1 = self.scores
        return {"scores": self.scores[:], "winner": 0 if s0 > s1 else (1 if s1 > s0 else -1), "unexpected_moves": unexpected}


def raphael_experiment(cfg, words, quem_desvia=None, agenda="original"):
    g_w = d_w = ties = 0
    for i in range(cfg.raphael_games):
        g = RaphaelGame(cfg.seed + i, words, cfg.raphael_turns, deviate=False, agenda=agenda).play()
        d = RaphaelGame(cfg.seed + i, words, cfg.raphael_turns, deviate=True, quem_desvia=quem_desvia, agenda=agenda).play()
        g_w += int(g["winner"] == 0)
        d_w += int(d["winner"] == 0)
        ties += int(g["winner"] == -1)
    return {"p0_wins_greedy": g_w, "p0_wins_deviant": d_w, "greedy_ties": ties, "diferenca": d_w - g_w, "supported": d_w > g_w}


def chance_minimo_em(H, n=60, k=6):
    """P(o MÍNIMO de um sorteio de k entre 1..n cai no conjunto fixo H) = Σ_{h∈H} C(n−h, k−1)/C(n, k)."""
    return sum(math.comb(n - h, k - 1) for h in H) / math.comb(n, k)


def iid_draw_limitation(seed, draws=300):
    """Sorteio IID 6 de 60, como no original: o alvo é draw[0] (o MÍNIMO do sorteio ordenado) e H são os 6 'quentes'.
    Acrescentado (P2718): a chance EXATA de cada H conter o mínimo, a referência certa no lugar do 6/60 declarado."""
    rng = random.Random(seed)
    hist, hot_hits, trials, chance_exata = [], 0, 0, 0.0
    for _ in range(draws):
        draw = sorted(rng.sample(range(1, 61), 6))
        if len(hist) >= 30:
            trials += 1
            hot = [n for n, _ in Counter(n for past in hist for n in past).most_common(6)]
            hot_hits += int(draw[0] in hot)
            chance_exata += chance_minimo_em(hot)
        hist.append(draw)
    taxa, ref = hot_hits / trials, chance_exata / trials
    z = (taxa - ref) / math.sqrt(ref * (1 - ref) / trials)
    return {"trials": trials, "hot_number_hit_rate": taxa, "chance_reference_6_of_60": 6 / 60, "chance_exata_media": ref, "z": z,
            "supported_prediction_claim": False}


def order_task():
    seqs = [(["a", "b", "c"], 1), (["b", "a", "c"], 0), (["c", "a", "b"], 1), (["a", "c", "b"], 0)]
    bow = lambda s: int("a" in s and "b" in s)
    bigram = lambda s: int(any(s[i] == "a" and s[i + 1] == "b" for i in range(len(s) - 1)))

    def rnn(s):
        st = 0
        for tok in s:
            st = 1 if tok == "a" else (2 if st == 1 and tok == "b" else 0)
        return int(st == 2)
    acc = lambda f: sum(f(s) == y for s, y in seqs) / len(seqs)
    return {"bow_accuracy": acc(bow), "bigram_accuracy": acc(bigram), "rnn_accuracy": acc(rnn)}


def attention(Q, K, V):
    dk = len(K[0])
    out = []
    for q in Q:
        w = softmax([sum(a * b for a, b in zip(q, k)) / math.sqrt(dk) for k in K])
        out.append([sum(w[i] * V[i][j] for i in range(len(V))) for j in range(len(V[0]))])
    return out


# --- dicionário OFFLINE (a rede do original não existe aqui) ---

class DictionaryClient:
    def __init__(self, cfg=None):
        self.cfg = cfg

    def lookup(self, word):
        key = word.lower().strip()
        if key in OFFLINE_LEXICON:
            return {"source": "offline", "entry": OFFLINE_LEXICON[key], "network": False}
        return {"source": "offline-miss", "entry": None, "network": False}


# --- segurança: o original por texto (reproduzido para medir o falso positivo) e a versão por AST ---

_PADROES_TEXTO = {
    "exec": r"\bexec\s*\(", "eval": r"\beval\s*\(", "os_system": r"os\.system\s*\(", "subprocess": r"subprocess\.",
    "hardcoded_secret": r"(api_key|password|secret)\s*=\s*['\"][^'\"]+['\"]", "backdoor_marker": r"BACKDOOR|sandbox_escape",
}


def security_audit_texto(source):
    """A security_audit do ORIGINAL (por regex no texto). Devolve a lista de achados."""
    return [nome for nome, pat in _PADROES_TEXTO.items() if re.search(pat, source)]


def auditores_texto_ok(source):
    """A checagem 'seguranca_sem_exec' dos Auditors do original (por substring)."""
    return "exec(" not in source and "eval(" not in source


_NOMES_PERIGOSOS = {"exec", "eval", "compile", "__import__"}                                 # chamadas por NOME (builtins)
_ATRIBUTOS_PERIGOSOS = {"system", "popen", "Popen", "urlopen", "exec_module", "fork", "run"}  # chamadas por ATRIBUTO (os.system...)
_BASES_DO_RUN = {"subprocess", "_sp", "sp"}   # .run só conta quando a base é o subprocess (asyncio.run não é processo novo)
_IMPORTS_PERIGOSOS = {"subprocess", "socket", "urllib", "http", "multiprocessing", "ctypes", "pickle", "importlib"}


def security_audit_ast(source):
    """Auditoria pela árvore sintática: CHAMADAS reais e IMPORTS, não strings. Devolve a lista ordenada de achados."""
    achados = set()
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name) and f.id in _NOMES_PERIGOSOS:
                achados.add("chamada:" + f.id)
            elif isinstance(f, ast.Attribute) and f.attr in _ATRIBUTOS_PERIGOSOS:
                # re.compile é atributo e não está na lista: a 1ª versão (só pelo nome) acusava re.compile como compile (falso positivo)
                base = f.value.id if isinstance(f.value, ast.Name) else ""
                if f.attr != "run" or base in _BASES_DO_RUN:
                    achados.add("chamada:" + f.attr)
        elif isinstance(n, ast.Import):
            achados |= {"import:" + a.name.split(".")[0] for a in n.names if a.name.split(".")[0] in _IMPORTS_PERIGOSOS}
        elif isinstance(n, ast.ImportFrom) and (n.module or "").split(".")[0] in _IMPORTS_PERIGOSOS:
            achados.add("import:" + n.module.split(".")[0])
    return sorted(achados)


def assert_harness_original(report, source):
    """O assert_harness do original aplicado ao relatório, com a segurança e os auditores pela REGRA DO ORIGINAL (texto)."""
    erros = []
    if report["dynamics"]["cosine_error"] > 1e-9:
        erros.append("identidade do cosseno falhou")
    if report["graph"]["nodes"] != 910:
        erros.append("grafo não tem 910 nós")
    if report["graph"]["async_locked_sum"] != 100:
        erros.append("integridade assíncrona falhou")
    if report["status"]["agi"] or report["status"]["asi"]:
        erros.append("higiene de afirmação violada")
    if security_audit_texto(source):
        erros.append("auditoria de segurança do código falhou")
    if not (auditores_texto_ok(source) and report["probability"]["supported"]):
        erros.append("auditores falharam")
    if report["inference"]["prediction"] != 33:
        erros.append("inferência da sequência falhou")
    return erros


def run_all(cfg=None, salvar=None):
    """Orquestra tudo como o original, sem rede e sem disco (salvar=caminho grava o relatório, se pedido)."""
    cfg = cfg or Config()
    log = AuditLog()
    rep = Representation(OFFLINE_LEXICON)
    rep.observe_sentence("word and number and logic and test")
    enc = rep.encode("nexus raphael")
    th = 0.7
    direct, ident, err = cosine_double(th)
    seq, truth = [2, 3, 5, 9, 17], 33
    inferred = Cognition().infer_sequence(seq)
    meta = MetaCognition(log).evaluate(inferred, truth)
    graph = ComputeGraph(cfg.demo_graph_nodes, cfg.graph_layers, cfg.seed, cfg.max_ops)
    graph.sync_pass(1)
    asum = graph.async_increment()
    report = {
        "system": SYSTEM_NAME, "version": VERSION, "status": STATUS,
        "encoding": {"roundtrip_a1z26": a1z26_decode(a1z26_encode("nexus")) == "nexus", "reversible": enc["reversible_a1z26"],
                     "nearest": rep.nearest("word"), "nonce": propose_meaning(generate_nonce(random.Random(cfg.seed), OFFLINE_LEXICON))},
        "dynamics": {"cosine_error": err},
        "inference": inferred, "metacognition": meta, "recursive": RecursiveMeta().evaluate(meta),
        "probability": probability_experiment(cfg), "debate": debate(seq, truth), "forgetting": forgetting_experiment(cfg),
        "graph": {"nodes": graph.n, "ops": graph.ops, "async_locked_sum": asum},
        "games": {"raphael": raphael_experiment(cfg, list(OFFLINE_LEXICON)),
                  "raphael_so_p0": raphael_experiment(cfg, list(OFFLINE_LEXICON), quem_desvia=0),
                  "kuhn": kuhn_poker_value(cfg.seed), "kuhn_exato": float(kuhn_exato()), "order": order_task()},
        "draws": iid_draw_limitation(cfg.seed),
        "dictionary": DictionaryClient(cfg).lookup("nexus"),
        "security_ast": security_audit_ast(inspect.getsource(inspect.getmodule(run_all))),
    }
    if salvar is not None:
        import json
        with open(salvar, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    return report
