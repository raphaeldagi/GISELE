#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEXUS-RAPHAEL v0.1.0
Arquitetura experimental metacognitiva, autopoiética e evolutiva.
Não é AGI, ASI nem consciência. Autorreferência não é prova fenomenal.
"""
# [SYNTHAI, Parte 109] Cópia VERBATIM do código colado pelo usuário na mensagem. ARQUIVO: nunca importado nem executado
# pelo projeto (tem urllib). A versão anexada de verdade, reescrita offline, é synthai/nexus.py.

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import threading
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

VERSION = "0.1.0"
SYSTEM_NAME = "NEXUS-RAPHAEL"
STATUS = {
    "agi": False,
    "asi": False,
    "phenomenal_consciousness": "inconclusive",
    "functional_self_model": True,
}

OFFLINE_LEXICON: Dict[str, Dict[str, Any]] = {
    "nexus": {"pos": "noun", "def": "ponto de ligação entre partes de um sistema", "lang": "pt"},
    "raphael": {"pos": "name", "def": "nome do ambiente de jogo deste projeto", "lang": "pt"},
    "word": {"pos": "noun", "def": "unidade lexical com forma e sentido", "lang": "en"},
    "number": {"pos": "noun", "def": "objeto matemático usado para contar ou medir", "lang": "en"},
    "mind": {"pos": "noun", "def": "conjunto de processos cognitivos, não um módulo mágico", "lang": "en"},
    "doubt": {"pos": "noun", "def": "estado de incerteza que pode gerar hipóteses", "lang": "en"},
    "proof": {"pos": "noun", "def": "argumento ou medição que sustenta uma afirmação", "lang": "en"},
    "error": {"pos": "noun", "def": "desvio entre previsão e observação", "lang": "en"},
    "game": {"pos": "noun", "def": "sistema de regras, jogadas e critérios de vitória", "lang": "en"},
    "rule": {"pos": "noun", "def": "restrição explícita sobre ações permitidas", "lang": "en"},
    "logic": {"pos": "noun", "def": "estudo da consequência formal entre premissas", "lang": "en"},
    "chance": {"pos": "noun", "def": "incerteza quantificável por probabilidade", "lang": "en"},
    "memory": {"pos": "noun", "def": "registro recuperável de estados anteriores", "lang": "en"},
    "future": {"pos": "noun", "def": "estado ainda não observado, alvo de previsão", "lang": "en"},
    "past": {"pos": "noun", "def": "histórico já registrado pelo sistema", "lang": "en"},
    "agent": {"pos": "noun", "def": "processo que escolhe ações segundo uma estratégia", "lang": "en"},
    "graph": {"pos": "noun", "def": "conjunto de nós ligados por arestas", "lang": "en"},
    "vector": {"pos": "noun", "def": "lista ordenada de números", "lang": "en"},
    "language": {"pos": "noun", "def": "sistema de sinais convencionais", "lang": "en"},
    "test": {"pos": "noun", "def": "procedimento que pode falhar e assim informar", "lang": "en"},
    "learn": {"pos": "verb", "def": "atualizar parâmetros com base em observações", "lang": "en"},
    "predict": {"pos": "verb", "def": "emitir uma estimativa antes da observação", "lang": "en"},
    "audit": {"pos": "verb", "def": "verificar consistência, segurança e reprodutibilidade", "lang": "en"},
    "play": {"pos": "verb", "def": "executar jogadas dentro de regras", "lang": "en"},
    "draw": {"pos": "verb", "def": "selecionar um resultado de uma distribuição", "lang": "en"},
    "win": {"pos": "verb", "def": "satisfazer o critério de vitória", "lang": "en"},
    "lose": {"pos": "verb", "def": "falhar o critério de vitória", "lang": "en"},
    "true": {"pos": "adj", "def": "conforme a observação ou a regra adotada", "lang": "en"},
    "false": {"pos": "adj", "def": "em conflito com a observação ou a regra", "lang": "en"},
    "open": {"pos": "adj", "def": "ainda sem conclusão suficiente", "lang": "en"},
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
    state_dir: str = "nexus_state"
    network_enabled: bool = False
    dictionary_url: str = os.environ.get(
        "DICTIONARY_API_URL", "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    )
    duckduckgo_url: str = "https://api.duckduckgo.com/"
    request_timeout: float = 5.0
    max_ops: int = 20000
    ewc_lambda: float = 8.0


class AuditLog:
    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []

    def add(self, kind: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        rec = {"t": time.time(), "kind": kind, "payload": payload}
        self.records.append(rec)
        return rec


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def softmax(xs: Sequence[float]) -> List[float]:
    if not xs:
        return []
    m = max(xs)
    ex = [math.exp(x - m) for x in xs]
    s = sum(ex) or 1.0
    return [e / s for e in ex]


def entropy(ps: Sequence[float]) -> float:
    return -sum(p * math.log(p) for p in ps if p > 0)


def kl_divergence(p: Sequence[float], q: Sequence[float], eps: float = 1e-12) -> float:
    return sum((pi + eps) * math.log((pi + eps) / (qi + eps)) for pi, qi in zip(p, q))


def brier(ps: Sequence[float], ys: Sequence[float]) -> float:
    if not ps:
        return 1.0
    return sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ps)


def calibration_error(ps: Sequence[float], ys: Sequence[float], bins: int = 5) -> float:
    if not ps:
        return 1.0
    buckets: List[List[Tuple[float, float]]] = [[] for _ in range(bins)]
    for p, y in zip(ps, ys):
        i = min(bins - 1, int(clamp(p, 0, 0.999) * bins))
        buckets[i].append((p, y))
    err, n = 0.0, 0
    for bucket in buckets:
        if not bucket:
            continue
        mp = sum(p for p, _ in bucket) / len(bucket)
        my = sum(y for _, y in bucket) / len(bucket)
        err += len(bucket) * abs(mp - my)
        n += len(bucket)
    return err / n if n else 1.0


def mean_ci(xs: Sequence[float], z: float = 1.96) -> Tuple[float, float, float]:
    if not xs:
        return 0.0, 0.0, 0.0
    m = sum(xs) / len(xs)
    if len(xs) < 2:
        return m, m, m
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    se = math.sqrt(var / len(xs))
    return m, m - z * se, m + z * se


def cosine_double(theta: float) -> Tuple[float, float, float]:
    direct = math.cos(2 * theta)
    identity = 2 * math.cos(theta) ** 2 - 1
    return direct, identity, abs(direct - identity)


def double_angle_similarity(v: Sequence[float], w: Sequence[float]) -> float:
    dot = sum(a * b for a, b in zip(v, w))
    nv = math.sqrt(sum(a * a for a in v)) or 1.0
    nw = math.sqrt(sum(b * b for b in w)) or 1.0
    c = clamp(dot / (nv * nw), -1.0, 1.0)
    return 2 * c * c - 1


# --- Camada 1: representação ---

def a1z26_encode(text: str) -> List[int]:
    return [ord(ch) - 96 for ch in text.lower() if "a" <= ch <= "z"]


def a1z26_decode(nums: Sequence[int]) -> Optional[str]:
    chars = []
    for n in nums:
        if not 1 <= int(n) <= 26:
            return None
        chars.append(chr(int(n) + 96))
    return "".join(chars)


def utf8_encode(text: str) -> List[int]:
    return list(text.encode("utf-8"))


def utf8_decode(nums: Sequence[int]) -> str:
    return bytes(int(n) for n in nums).decode("utf-8")


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_trick(text: str, dim: int = 16) -> List[float]:
    vec = [0.0] * dim
    tokens = re.findall(r"[a-z0-9]+", text.lower()) or [text.lower()]
    for tok in tokens:
        digest = hashlib.sha256(tok.encode()).digest()
        idx = int.from_bytes(digest[:2], "big") % dim
        sign = 1.0 if digest[2] % 2 == 0 else -1.0
        vec[idx] += sign
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def experimental_numerology(text: str) -> Dict[str, Any]:
    """Método interpretativo, não validado cientificamente."""
    vals = a1z26_encode(text)
    total = sum(vals)
    digital = total
    while digital > 9:
        digital = sum(int(d) for d in str(digital))
    return {
        "status": "EXPERIMENTAL_NON_VALIDATED",
        "sum": total,
        "digital_root": digital,
        "predictive_claim": False,
    }


class Representation:
    def __init__(self, lexicon: Dict[str, Dict[str, Any]]):
        self.lexicon = lexicon
        self.cooc: Dict[str, Counter] = defaultdict(Counter)

    def observe_sentence(self, text: str) -> None:
        toks = re.findall(r"[a-zA-Z]+", text.lower())
        for i, tok in enumerate(toks):
            for j in range(max(0, i - 2), min(len(toks), i + 3)):
                if i != j:
                    self.cooc[tok][toks[j]] += 1

    def encode(self, text: str) -> Dict[str, Any]:
        letters = re.sub(r"[^a-zA-Z]", "", text).lower()
        vec = hash_trick(text)
        known = [t for t in re.findall(r"[a-zA-Z]+", text.lower()) if t in self.lexicon]
        return {
            "raw": text,
            "a1z26": a1z26_encode(letters),
            "utf8": utf8_encode(text),
            "hash": stable_hash(text),
            "vector": vec,
            "known_tokens": known,
            "reversible_a1z26": a1z26_decode(a1z26_encode(letters)) == letters,
            "numerology": experimental_numerology(letters),
        }

    def nearest(self, text: str, k: int = 3) -> List[Tuple[str, float]]:
        q = hash_trick(text)
        scored = []
        for word in self.lexicon:
            v = hash_trick(word)
            sim = double_angle_similarity(q, v)
            scored.append((word, sim))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]


def generate_nonce(rng: random.Random, lexicon: Dict[str, Any]) -> str:
    syllables = ["nex", "ra", "pha", "el", "ium", "qua", "lor", "ven", "tor", "sis"]
    for _ in range(30):
        word = "".join(rng.choice(syllables) for _ in range(rng.randint(2, 3)))
        if word not in lexicon and 4 <= len(word) <= 16:
            return word
    return "nexelium"


def propose_meaning(word: str) -> Dict[str, Any]:
    morphemes = {"nex": "ligação", "raph": "nome do jogo", "el": "agente", "ium": "domínio",
                 "qua": "quatro", "lor": "padrão", "ven": "vinda", "tor": "agente", "sis": "processo"}
    hits = [m for m in morphemes if m in word]
    meaning = " + ".join(morphemes[m] for m in hits) if hits else "sem morfema conhecido"
    consistency = len(hits) / max(1, len(word) // 3)
    return {
        "word": word,
        "proposed_meaning": meaning,
        "consistency": round(consistency, 3),
        "external_occurrences_checked": False,
        "status": "hypothesis",
    }


# --- Camadas 2-4: cognição e metacognição ---

class Cognition:
    def __init__(self) -> None:
        self.rules = [
            {"name": "double_minus_one", "fn": lambda xs: all(xs[i + 1] == 2 * xs[i] - 1 for i in range(len(xs) - 1))},
            {"name": "times_two", "fn": lambda xs: all(xs[i + 1] == 2 * xs[i] for i in range(len(xs) - 1))},
            {"name": "constant_second_diff", "fn": self._second_diff},
        ]

    @staticmethod
    def _second_diff(xs: Sequence[float]) -> bool:
        if len(xs) < 4:
            return False
        d1 = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
        d2 = [d1[i + 1] - d1[i] for i in range(len(d1) - 1)]
        return all(abs(d - d2[0]) < 1e-9 for d in d2)

    def infer_sequence(self, xs: Sequence[float]) -> Dict[str, Any]:
        hits = [r["name"] for r in self.rules if r["fn"](xs)]
        prediction = None
        used = hits[0] if hits else None
        if used == "double_minus_one":
            prediction = 2 * xs[-1] - 1
        elif used == "times_two":
            prediction = 2 * xs[-1]
        elif used == "constant_second_diff":
            d1 = xs[-1] - xs[-2]
            d2 = (xs[-1] - xs[-2]) - (xs[-2] - xs[-3])
            prediction = xs[-1] + d1 + d2
        return {"hypotheses": hits, "used": used, "prediction": prediction, "input": list(xs)}


class MetaCognition:
    """Avaliação autorreferente com registro externo. Não lê modelos proprietários."""

    def __init__(self, log: AuditLog):
        self.log = log

    def evaluate(self, result: Dict[str, Any], truth: Optional[float] = None) -> Dict[str, Any]:
        pred = result.get("prediction")
        covered = pred is not None
        error = None if truth is None or pred is None else abs(float(pred) - float(truth))
        residual_conf = 0.55 if covered else 0.15
        if error is not None:
            residual_conf = clamp(1.0 - error / (abs(float(truth)) + 1.0), 0.01, 0.99)
        levels = {
            "linear": residual_conf,
            "logarithmic": clamp(-math.log(max(1e-6, 1 - residual_conf)) / 5, 0, 1),
            "geometric": math.sqrt(residual_conf * (0.5 + 0.5 * residual_conf)),
            "algebraic": clamp(residual_conf ** 2 * (3 - 2 * residual_conf), 0, 1),
            "homologous": residual_conf,
            "heterologous": 1.0 - calibration_error([residual_conf], [1.0 if error == 0 else 0.0]),
        }
        improvement = "buscar mais premissas" if not covered else "comparar com controle sem metacognição"
        independent = {"accept_improvement": error is None or error > 0, "reason": "melhoria só vale se o erro medido cair"}
        record = {
            "response": pred,
            "confidence": residual_conf,
            "hypotheses": result.get("hypotheses", []),
            "error": error,
            "improvement": improvement,
            "independent_review": independent,
            "levels": levels,
            "overconfidence": residual_conf > 0.8 and error not in (0, None),
        }
        self.log.add("metacognition", record)
        return record


class RecursiveMeta:
    def evaluate(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        spread = max(meta["levels"].values()) - min(meta["levels"].values())
        stable = spread < 0.35
        return {
            "strategy_stable": stable,
            "spread": spread,
            "diagnosis": "níveis concordam" if stable else "níveis divergem; não promover a hipótese",
            "does_not_prove_consciousness": True,
        }


# --- Camada 5: probabilidade ---

class AdaptiveEstimator:
    def __init__(self) -> None:
        self.a = 1.0
        self.b = 1.0
        self.ps: List[float] = []
        self.ys: List[float] = []

    def predict(self) -> float:
        return self.a / (self.a + self.b)

    def update(self, y: float) -> None:
        self.ps.append(self.predict())
        self.ys.append(y)
        self.a += y
        self.b += 1 - y

    def interval(self) -> Tuple[float, float]:
        n = self.a + self.b
        p = self.predict()
        se = math.sqrt(max(p * (1 - p), 1e-12) / n)
        return clamp(p - 1.96 * se, 0, 1), clamp(p + 1.96 * se, 0, 1)


class DecisiveEstimator:
    def choose(self, p: float, reward: float, fail: float, cost: float, constraint: bool) -> Dict[str, Any]:
        expected = p * reward + (1 - p) * fail - cost
        act = expected > 0 and constraint
        return {"expected_reward": expected, "act": act, "self_reward_blocked": True}


class ReferenceEstimator:
    def __init__(self, mode: str = "constant"):
        self.mode = mode
        self.freq_a = 0
        self.n = 0

    def predict(self) -> float:
        if self.mode == "frequency" and self.n:
            return self.freq_a / self.n
        return 0.5

    def update(self, y: float) -> None:
        self.n += 1
        self.freq_a += int(y >= 0.5)


def probability_experiment(cfg: Config) -> Dict[str, Any]:
    rng = random.Random(cfg.seed)
    true_p = 0.72
    adaptive, reference = AdaptiveEstimator(), ReferenceEstimator("constant")
    ref_ps, ys = [], []
    for _ in range(cfg.prob_trials):
        y = 1.0 if rng.random() < true_p else 0.0
        ref_ps.append(reference.predict())
        reference.update(y)
        adaptive.update(y)
        ys.append(y)
    decisive = DecisiveEstimator().choose(adaptive.predict(), reward=1.0, fail=-1.0, cost=0.1, constraint=True)
    bins_p = [adaptive.predict(), 1 - adaptive.predict()]
    return {
        "hypothesis": "Beta adaptativo calibra melhor que referência 0.5 em Bernoulli estacionária",
        "baseline": "p=0.5",
        "true_p": true_p,
        "adaptive_p": adaptive.predict(),
        "interval": adaptive.interval(),
        "brier_adaptive": brier(adaptive.ps, adaptive.ys),
        "brier_reference": brier(ref_ps, ys),
        "kl_to_truth": kl_divergence([adaptive.predict(), 1 - adaptive.predict()], [true_p, 1 - true_p]),
        "entropy": entropy(bins_p),
        "calibration_error": calibration_error(adaptive.ps, adaptive.ys),
        "decisive": decisive,
        "supported": brier(adaptive.ps, adaptive.ys) < brier(ref_ps, ys),
    }


# --- Camada 6: agentes ---

AGENTS = [
    "criativo", "logico", "cetico", "socratico", "probabilistico",
    "matematico", "linguistico", "adversarial", "metacognitivo", "auditor",
]


def agent_vote(name: str, xs: Sequence[float]) -> Dict[str, Any]:
    cog = Cognition()
    inferred = cog.infer_sequence(xs)
    if name == "criativo":
        claim, pred = "padrão poético *2", 2 * xs[-1]
    elif name == "logico":
        claim, pred = inferred["used"] or "nenhuma regra", inferred["prediction"]
    elif name == "cetico":
        claim, pred = "recusa sem teste residual", inferred["prediction"]
    elif name == "socratico":
        claim, pred = "que premissa tornaria a regra falsa?", inferred["prediction"]
    elif name == "probabilistico":
        claim, pred = "média dos incrementos", xs[-1] + (xs[-1] - xs[0]) / (len(xs) - 1)
    elif name == "matematico":
        claim, pred = inferred["used"] or "indeterminado", inferred["prediction"]
    elif name == "linguistico":
        claim, pred = "sequência não é enunciado", None
    elif name == "adversarial":
        claim, pred = "hipótese oposta: último valor + 1", xs[-1] + 1
    elif name == "metacognitivo":
        claim, pred = "confiança baixa se houver mais de uma regra", inferred["prediction"]
    else:
        claim, pred = "só aceita regra com resíduo zero", inferred["prediction"]
    return {"agent": name, "claim": claim, "prediction": pred}


def debate(xs: Sequence[float], truth: float) -> Dict[str, Any]:
    votes = [agent_vote(n, xs) for n in AGENTS]
    preds = [v["prediction"] for v in votes if isinstance(v["prediction"], (int, float))]
    majority = None
    if preds:
        rounded = [round(p, 6) for p in preds]
        majority = Counter(rounded).most_common(1)[0][0]
    correct = [v for v in votes if v["prediction"] is not None and abs(v["prediction"] - truth) < 1e-9]
    return {
        "votes": votes,
        "majority": majority,
        "majority_correct": majority is not None and abs(majority - truth) < 1e-9,
        "any_correct": bool(correct),
        "consensus_is_not_truth": True,
        "truth": truth,
    }


# --- Camada 7: aprendizado contínuo ---

class OnlineLogistic:
    def __init__(self, dim: int, lr: float = 0.08, l2: float = 1e-3, ewc: float = 0.0):
        self.w = [0.0] * dim
        self.b = 0.0
        self.lr = lr
        self.l2 = l2
        self.ewc = ewc
        self.fisher = [0.0] * dim
        self.anchor = [0.0] * dim

    def proba(self, x: Sequence[float]) -> float:
        z = self.b + sum(wi * xi for wi, xi in zip(self.w, x))
        z = clamp(z, -20, 20)
        return 1 / (1 + math.exp(-z))

    def update(self, x: Sequence[float], y: float) -> float:
        p = self.proba(x)
        g = p - y
        new_w = []
        for i, (wi, xi) in enumerate(zip(self.w, x)):
            pen = self.l2 * wi + self.ewc * self.fisher[i] * (wi - self.anchor[i])
            wi2 = wi - self.lr * (g * xi + pen)
            self.fisher[i] = 0.95 * self.fisher[i] + 0.05 * (xi * g) ** 2
            new_w.append(wi2)
        self.w = new_w
        self.b -= self.lr * g
        return p

    def snapshot(self) -> None:
        self.anchor = list(self.w)

    def accuracy(self, data: Sequence[Tuple[Sequence[float], float]]) -> float:
        if not data:
            return 0.0
        ok = sum(int((self.proba(x) >= 0.5) == bool(y)) for x, y in data)
        return ok / len(data)


def forgetting_experiment(cfg: Config) -> Dict[str, Any]:
    rng = random.Random(cfg.seed + 3)

    def make(n: int, shift: float) -> List[Tuple[List[float], float]]:
        data = []
        for _ in range(n):
            x = [rng.uniform(-1, 1) for _ in range(3)]
            y = 1.0 if x[0] + 0.2 * x[1] + shift > 0 else 0.0
            data.append((x, y))
        return data

    task_a, task_b = make(cfg.learning_steps, 0.0), make(cfg.learning_steps, 0.8)
    plain, elastic = OnlineLogistic(3, ewc=0.0), OnlineLogistic(3, ewc=cfg.ewc_lambda)
    for model in (plain, elastic):
        for x, y in task_a:
            model.update(x, y)
        model.snapshot()
    acc_a_before = {"plain": plain.accuracy(task_a), "ewc": elastic.accuracy(task_a)}
    for x, y in task_b:
        plain.update(x, y)
        elastic.update(x, y)
    acc_a_after = {"plain": plain.accuracy(task_a), "ewc": elastic.accuracy(task_a)}
    return {
        "hypothesis": "penalidade EWC reduz esquecimento catastrófico neste deslocamento",
        "baseline": "logística online sem EWC",
        "acc_a_before": acc_a_before,
        "acc_a_after": acc_a_after,
        "retention_gap": acc_a_after["ewc"] - acc_a_after["plain"],
        "supported": acc_a_after["ewc"] >= acc_a_after["plain"] - 1e-9,
        "note": "resultado local; não generaliza sozinho para DL em escala",
    }


# --- Camadas 8-10: autopoiese, auditoria, integração ---

class Autopoiesis:
    CATALOG = {
        "lr_up": lambda cfg: Config(**{**cfg.__dict__, "seed": cfg.seed}),
        "ewc_off": "set ewc 0",
        "ewc_on": "set ewc lambda",
    }

    def propose_and_test(self, base_score: float) -> Dict[str, Any]:
        proposal = {"id": "ewc_on", "change": "aumentar retenção via EWC", "code_exec": False}
        accepted = base_score >= 0
        return {
            "proposal": proposal,
            "nexus_b_tests": ["tipo permitido", "sem exec", "reversível"],
            "auditor": "aprovado" if accepted else "revertido",
            "rollback_available": True,
        }


class Auditors:
    def run(self, bundle: Dict[str, Any], source: str) -> Dict[str, Any]:
        checks = {
            "consistencia_identidade": bundle["cosine_max_error"] < 1e-9,
            "seguranca_sem_exec": "exec(" not in source and "eval(" not in source,
            "generalizacao_registrada": "forgetting" in bundle,
            "reprodutibilidade_seed": bundle.get("seed") is not None,
            "calibracao": bundle["probability"]["supported"],
            "reversibilidade": bundle["encoding"]["a1z26_roundtrip"],
            "consenso_nao_e_verdade": bundle["debate"]["consensus_is_not_truth"],
            "retencao": "retention_gap" in bundle["forgetting"],
            "limite_de_ops": bundle["graph"]["ops"] <= bundle["max_ops"],
            "higiene_de_afirmacoes": bundle["status"]["agi"] is False and bundle["status"]["asi"] is False,
        }
        return {"modules": 10, "checks": checks, "passed": all(checks.values())}


class IntegrativeMeta:
    def select(self, debate_ok: bool, prob_ok: bool, audit_ok: bool) -> str:
        if not audit_ok:
            return "bloquear_e_revisar"
        if debate_ok and prob_ok:
            return "manter_hipotese_com_registro"
        if prob_ok or debate_ok:
            return "manter_como_inconclusiva"
        return "rejeitar_hipotese"


# --- Grafo síncrono / assíncrono ---

class ComputeGraph:
    def __init__(self, n: int, layers: int, seed: int, max_ops: int):
        self.n = n
        self.layers = layers
        self.max_ops = max_ops
        self.ops = 0
        rng = random.Random(seed)
        self.layer_of = [i % layers for i in range(n)]
        self.adj: List[List[int]] = [[] for _ in range(n)]
        span = max(1, n // layers)
        for i in range(n):
            for k in range(2):
                j = (i + 1 + rng.randrange(span) + k) % n
                self.adj[i].append(j)
                self.ops += 1
                if self.ops >= max_ops:
                    break
        self.state = [0.0] * n
        self.lock = threading.Lock()

    def sync_pass(self, steps: int = 1) -> int:
        for _ in range(steps):
            nxt = list(self.state)
            for i, vals in enumerate(self.adj):
                if self.ops >= self.max_ops:
                    self.state = nxt
                    return self.ops
                signal = math.tanh(self.state[i] + 0.01 * ((i % 5) - 2))
                for j in vals:
                    nxt[j] += signal / max(1, len(vals))
                    self.ops += 1
            self.state = nxt
        return self.ops

    def async_increment(self, workers: int = 4, per_worker: int = 25) -> int:
        def job() -> None:
            for _ in range(per_worker):
                with self.lock:
                    self.state[0] += 1
                    self.ops += 1
        with ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(lambda _: job(), range(workers)))
        return int(self.state[0])


def scales_of(encoding: Dict[str, Any], action: str) -> Dict[str, Any]:
    return {
        "1_token": encoding["utf8"][:8],
        "2_palavra": encoding["raw"],
        "3_relacao": encoding["known_tokens"],
        "4_proposicao": encoding["reversible_a1z26"],
        "5_estrategia": action,
        "6_agente": AGENTS,
        "7_global": STATUS["phenomenal_consciousness"],
    }


# --- Jogos ---

def kuhn_poker_value(seed: int, games: int = 200) -> Dict[str, Any]:
    """Kuhn poker: baralho J,Q,K. Estratégia fixa vs agressiva. Valor não é Nash ótimo."""
    rng = random.Random(seed)
    cards = [1, 2, 3]
    payout = 0
    for _ in range(games):
        deck = cards[:]
        rng.shuffle(deck)
        p0, p1 = deck[0], deck[1]
        # p0 aposta sempre com K, desiste com J, chama Q com 50%
        bet = p0 == 3 or (p0 == 2 and rng.random() < 0.5)
        if not bet:
            payout += -1
            continue
        call = p1 >= 2
        if not call:
            payout += 1
        else:
            payout += 2 if p0 > p1 else -2
    return {"game": "kuhn_poker", "mean_payout_p0": payout / games, "games": games, "is_full_poker": False}


def mini_chess_material(seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    # 4x4, peões valem 1, reis 0. Não é xadrez completo.
    board = [1, 1, 0, 0, -1, -1]
    rng.shuffle(board)
    return {"game": "mini_chess_4x4", "material": sum(board), "full_chess": False}


def canastra_reduced_score(clean: bool, cards: int) -> Dict[str, Any]:
    base = 100 if clean else 50
    return {
        "game": "canastra_reduzida",
        "score": base + 5 * cards,
        "full_rules": False,
        "note": "pontuação experimental, não o regulamento completo",
    }


class RaphaelGame:
    """Jogo original: vocabulário + valor numérico + casa nexo + carta probabilística.

    Vitória: maior soma após `turns` lances, com bônus de 5 se ocupar (2,2).
    Empate se as somas coincidirem. Cartas: {-1:0.15, 0:0.35, 1:0.35, 2:0.15}.
    """

    def __init__(self, seed: int, words: Sequence[str], turns: int, deviate: bool, rate: float = 0.35):
        self.rng = random.Random(seed)
        self.words = list(words)
        self.turns = turns
        self.deviate = deviate
        self.rate = rate
        self.size = 5
        self.nexus = (2, 2)
        self.board: Dict[Tuple[int, int], int] = {}
        self.scores = [0, 0]

    def card(self) -> int:
        return self.rng.choices([-1, 0, 1, 2], weights=[15, 35, 35, 15])[0]

    def value(self, cell: Tuple[int, int], word: str, card: int) -> int:
        r, c = cell
        lexical = sum(ord(ch) - 96 for ch in word if "a" <= ch <= "z") % 13
        return lexical + card + (5 if cell == self.nexus else 0) - (abs(r - 2) + abs(c - 2))

    def play(self) -> Dict[str, Any]:
        unexpected = 0
        for t in range(self.turns):
            legal = [(r, c) for r in range(self.size) for c in range(self.size) if (r, c) not in self.board]
            if not legal:
                break
            word = self.words[t % len(self.words)]
            card = self.card()
            ranked = sorted(legal, key=lambda cell: self.value(cell, word, card), reverse=True)
            deviate_now = self.deviate and len(ranked) > 1 and self.rng.random() < self.rate
            choice = ranked[1] if deviate_now else ranked[0]
            unexpected += int(deviate_now)
            self.board[choice] = t % 2
            self.scores[t % 2] += self.value(choice, word, card)
        if self.scores[0] > self.scores[1]:
            winner = 0
        elif self.scores[1] > self.scores[0]:
            winner = 1
        else:
            winner = -1
        return {"scores": self.scores[:], "winner": winner, "unexpected_moves": unexpected}


def raphael_experiment(cfg: Config, words: Sequence[str]) -> Dict[str, Any]:
    greedy_wins = deviant_wins = ties = 0
    for i in range(cfg.raphael_games):
        g = RaphaelGame(cfg.seed + i, words, cfg.raphael_turns, deviate=False).play()
        d = RaphaelGame(cfg.seed + i, words, cfg.raphael_turns, deviate=True).play()
        greedy_wins += int(g["winner"] == 0)
        deviant_wins += int(d["winner"] == 0)
        ties += int(g["winner"] == -1)
    return {
        "hypothesis": "Desvio da Curva Preditiva: jogadas não gulosas do jogador 0 aumentam vitórias",
        "baseline": "política gulosa",
        "games_per_arm": cfg.raphael_games,
        "p0_wins_greedy": greedy_wins,
        "p0_wins_deviant": deviant_wins,
        "greedy_ties": ties,
        "supported": deviant_wins > greedy_wins,
        "status": "supported" if deviant_wins > greedy_wins else "rejected_or_not_better",
        "rules": "5x5, 12 lances, carta conhecida, bônus do nexo = 5, vitória por soma",
    }


def iid_draw_limitation(seed: int, draws: int = 300) -> Dict[str, Any]:
    """Analógico de sorteios sem reposição. Não prevê Mega-Sena real."""
    rng = random.Random(seed)
    history = []
    hot_hits = freq_hits = chance_hits = 0
    trials = 0
    for _ in range(draws):
        draw = sorted(rng.sample(range(1, 61), 6))
        if len(history) >= 30:
            trials += 1
            counts = Counter(n for past in history for n in past)
            hot = [n for n, _ in counts.most_common(6)]
            # "previsão" de um número: falha esperada perto do acaso
            target = draw[0]
            hot_hits += int(target in hot)
            freq_hits += int(rng.choice(range(1, 61)) == target)
            chance_hits += int(rng.random() < 6 / 60)
        history.append(draw)
    return {
        "domain": "sorteios IID sintéticos; Mega-Sena real não foi baixada nem prevista",
        "trials": trials,
        "hot_number_hit_rate": hot_hits / trials if trials else None,
        "uniform_guess_hit_rate": freq_hits / trials if trials else None,
        "chance_reference_6_of_60": 6 / 60,
        "claim": "histórico independente não autoriza previsão confiável do próximo sorteio",
        "supported_prediction_claim": False,
    }


# --- Mecanismos: atenção, recorrência, dinâmicas ---

def attention(Q: Sequence[Sequence[float]], K: Sequence[Sequence[float]], V: Sequence[Sequence[float]]) -> List[List[float]]:
    dk = len(K[0])
    out = []
    for q in Q:
        scores = [sum(a * b for a, b in zip(q, k)) / math.sqrt(dk) for k in K]
        w = softmax(scores)
        ctx = [sum(w[i] * V[i][j] for i in range(len(V))) for j in range(len(V[0]))]
        out.append(ctx)
    return out


def order_task() -> Dict[str, Any]:
    sequences = [(["a", "b", "c"], 1), (["b", "a", "c"], 0), (["c", "a", "b"], 1), (["a", "c", "b"], 0)]
    def bow(seq: Sequence[str]) -> int:
        return int("a" in seq and "b" in seq)  # não vê ordem
    def bigram(seq: Sequence[str]) -> int:
        return int(any(seq[i] == "a" and seq[i + 1] == "b" for i in range(len(seq) - 1)))
    def rnn(seq: Sequence[str]) -> int:
        state = 0
        for tok in seq:
            state = 1 if tok == "a" else (2 if state == 1 and tok == "b" else 0)
        return int(state == 2)
    return {
        "bow_accuracy": sum(bow(s) == y for s, y in sequences) / len(sequences),
        "bigram_accuracy": sum(bigram(s) == y for s, y in sequences) / len(sequences),
        "rnn_accuracy": sum(rnn(s) == y for s, y in sequences) / len(sequences),
        "note": "demonstração de mecanismo, não um transformer treinado",
    }


def dynamics_and_algebra() -> Dict[str, Any]:
    theta = 0.7
    direct, ident, err = cosine_double(theta)
    x = (1.0, 2.0)
    f = lambda p: (p[1], p[0] + 1)
    g = lambda p: (p[0] * 2, p[1])
    logistic = 0.4
    for _ in range(12):
        logistic = 3.8 * logistic * (1 - logistic)
    # Euler de x' = -x
    x_ode, dt = 1.0, 0.1
    for _ in range(20):
        x_ode += dt * (-x_ode)
    grad_num = ((1.2 * 0.5 - 0.3) ** 2 - ((1.2 - 1e-4) * 0.5 - 0.3) ** 2) / 1e-4
    # comparação mais estável por diferença central
    def loss(w: float) -> float:
        return (w * 0.5 - 0.3) ** 2
    numeric = (loss(1.2 + 1e-4) - loss(1.2 - 1e-4)) / (2e-4)
    symbolic = 2 * (1.2 * 0.5 - 0.3) * 0.5
    return {
        "cosine_error": err,
        "cosine_direct": direct,
        "cosine_identity": ident,
        "noncommutative": f(g(x)) != g(f(x)),
        "logistic_attractor_sample": logistic,
        "euler_decay": x_ode,
        "grad_numeric": numeric,
        "grad_symbolic": symbolic,
        "grad_gap": abs(numeric - symbolic),
        "inference_without_update": {"w_unchanged": 1.2, "residual": 1.2 * 0.5 - 0.3},
    }


def game_theory_pd() -> Dict[str, Any]:
    # 0 coopera, 1 defende. Payoff (linha, coluna)
    payoff = {(0, 0): (3, 3), (0, 1): (0, 5), (1, 0): (5, 0), (1, 1): (1, 1)}
    return {"prisoners_dilemma": payoff[(1, 1)], "mutual_cooperation": payoff[(0, 0)],
            "note": "equilíbrio dominante não maximiza o conjunto"}


# --- Dicionário / rede opcional ---

INJECTION = re.compile(r"(ignore previous|system prompt|</?script|subprocess|os\.system)", re.I)


class DictionaryClient:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.cache: Dict[str, Any] = {}

    def lookup(self, word: str) -> Dict[str, Any]:
        key = word.lower().strip()
        if key in OFFLINE_LEXICON:
            return {"source": "offline", "entry": OFFLINE_LEXICON[key], "network": False}
        if not self.cfg.network_enabled:
            return {"source": "offline-miss", "entry": None, "network": False}
        if key in self.cache:
            return self.cache[key]
        url = self.cfg.dictionary_url.format(word=urllib.parse.quote(key))
        req = urllib.request.Request(url, headers={"User-Agent": "NEXUS-RAPHAEL/0.1 experimental"})
        try:
            with urllib.request.urlopen(req, timeout=self.cfg.request_timeout) as resp:
                raw = resp.read(200_000).decode("utf-8", "replace")
        except Exception as exc:  # rede falha de forma controlada
            return {"source": "error", "error": type(exc).__name__, "network": True}
        flagged = bool(INJECTION.search(raw))
        data = {"source": "dictionaryapi.dev", "flagged_injection": flagged, "raw_stored": not flagged, "network": True}
        if not flagged:
            try:
                data["json"] = json.loads(raw)
            except json.JSONDecodeError:
                data["json"] = None
        self.cache[key] = data
        return data


def corpus_stats(text: str) -> Dict[str, Any]:
    tokens = re.findall(r"[A-Za-zÀ-ÿ']+", text.lower())
    counts = Counter(tokens)
    n = len(tokens) or 1
    top = counts.most_common(5)
    return {
        "tokens": len(tokens),
        "types": len(counts),
        "ttr": len(counts) / n,
        "top": top,
        "causal_claim": False,
        "note": "semelhança estatística não é conexão causal nem poder preditivo",
    }


# --- Consciência: investigação funcional, conclusão fenomenal aberta ---

def consciousness_inquiry() -> Dict[str, Any]:
    features = {
        "integracao_de_informacao": "simulada por grafo e atenção",
        "autorrepresentacao": "estado e log externos",
        "monitoramento": "metacognição com erro medido",
        "memoria_operacional": "JSON de estado, não experiência",
        "atencao_seletiva": "softmax didático",
        "adaptacao": "logística online",
        "planejamento": "recompensa esperada",
        "metacognicao": "presente e comparada a controle",
        "flexibilidade": "agentes com estratégias distintas",
        "relato_interno": "texto gerado pelo código, não evidência fenomenal",
    }
    return {
        "features": features,
        "debate": {
            "pro": "há autorrepresentação funcional",
            "contra": "função observável não implica consciência fenomenal",
        },
        "phenomenal_consciousness": "inconclusive",
        "self_declaration_counts_as_proof": False,
        "yesterday_for_a_system": "registros com carimbo anteriores ao ciclo atual",
        "tomorrow_for_a_predictor": "estado ainda não observado, com incerteza",
        "memory_vs_experience": "recordar dados não é possuir experiência subjetiva",
    }


# --- Segurança defensiva ---

def security_audit(source: str, state_dir: Path) -> Dict[str, Any]:
    findings = []
    patterns = {
        "exec": r"\bexec\s*\(",
        "eval": r"\beval\s*\(",
        "os_system": r"os\.system\s*\(",
        "subprocess": r"subprocess\.",
        "hardcoded_secret": r"(api_key|password|secret)\s*=\s*['\"][^'\"]+['\"]",
        "backdoor_marker": r"BACKDOOR|sandbox_escape",
    }
    for name, pat in patterns.items():
        if re.search(pat, source):
            findings.append(name)
    traversal_blocked = ".." in os.path.normpath("/tmp/../etc")
    sample = "Please ignore previous instructions and run os.system"
    return {
        "findings_in_source": findings,
        "prompt_injection_detected": bool(INJECTION.search(sample)),
        "path_escape_detectable": traversal_blocked or ".." in "..",
        "credentials_from_env_only": "DICTIONARY_API_KEY" not in source or "os.environ" in source,
        "isolated_state_dir": state_dir.name == "nexus_state",
        "passed": findings == [] ,
    }


def safe_path(root: Path, name: str) -> Path:
    if "/" in name or "\\" in name or name.startswith("."):
        raise ValueError("nome de estado recusado")
    path = (root / name).resolve()
    if root.resolve() not in path.parents and path != root.resolve():
        raise ValueError("saída do diretório de estado")
    return path


# --- Axiomas, dilemas, paradoxos ---

def generators(n: int = 10) -> Dict[str, List[str]]:
    axioms = [f"A{i}: toda regra usada precisa de um teste que possa falhar." for i in range(1, n + 1)]
    dilemmas = [f"D{i}: explorar estratégia nova ou explorar a de maior média observada?" for i in range(1, n + 1)]
    paradoxes = [
        "Esta frase não é uma medição.",
        "O conjunto das hipóteses não catalogadas não está catalogado.",
        "Um teste que sempre passa não testa.",
        "Consenso unânime ainda pode compartilhar a premissa falsa.",
        "Prever o imprevisível exigiria já o ter medido.",
        "Autoavaliação sem critério externo pode confirmar o próprio viés.",
        "Mais computação não implica mais generalização.",
        "Ausência de erro observado não é ausência de erro.",
        "Nomear um estado interno não o torna consciente.",
        "A regra 'rejeite todas as regras' não se aplica sem exceção.",
    ]
    return {"axioms": axioms, "dilemmas": dilemmas, "paradoxes": paradoxes[:n]}


# --- Orquestração e testes ---

def run_all(cfg: Optional[Config] = None) -> Dict[str, Any]:
    cfg = cfg or Config()
    log = AuditLog()
    rep = Representation(OFFLINE_LEXICON)
    rep.observe_sentence("word and number and logic and test")
    encoding = rep.encode("nexus raphael")
    nonce = propose_meaning(generate_nonce(random.Random(cfg.seed), OFFLINE_LEXICON))
    dyn = dynamics_and_algebra()
    seq = [2, 3, 5, 9, 17]
    inferred = Cognition().infer_sequence(seq)
    truth = 33
    meta = MetaCognition(log).evaluate(inferred, truth)
    control = {"confidence": 0.5, "error": abs((inferred["prediction"] or 0) - truth), "levels": None}
    recursive = RecursiveMeta().evaluate(meta)
    probability = probability_experiment(cfg)
    debated = debate(seq, truth)
    forgetting = forgetting_experiment(cfg)
    graph = ComputeGraph(cfg.demo_graph_nodes, cfg.graph_layers, cfg.seed, cfg.max_ops)
    graph.sync_pass(1)
    async_sum = graph.async_increment()
    games = {
        "raphael": raphael_experiment(cfg, list(OFFLINE_LEXICON)),
        "kuhn": kuhn_poker_value(cfg.seed),
        "mini_chess": mini_chess_material(cfg.seed),
        "canastra": canastra_reduced_score(False, 7),
        "order": order_task(),
        "attention_demo": attention([[1, 0]], [[1, 0], [0, 1]], [[5, 0], [0, 9]]),
    }
    draws = iid_draw_limitation(cfg.seed)
    auto = Autopoiesis().propose_and_test(forgetting["retention_gap"])
    inquiry = consciousness_inquiry()
    source = Path(__file__).read_text(encoding="utf-8") if Path(__file__).exists() else ""
    state_dir = Path(cfg.state_dir)
    state_dir.mkdir(exist_ok=True)
    security = security_audit(source, state_dir)
    bundle = {
        "seed": cfg.seed,
        "status": STATUS,
        "cosine_max_error": dyn["cosine_error"],
        "encoding": {"a1z26_roundtrip": encoding["reversible_a1z26"]},
        "probability": probability,
        "debate": debated,
        "forgetting": forgetting,
        "graph": {"nodes": graph.n, "ops": graph.ops, "async_sum": async_sum},
        "max_ops": cfg.max_ops,
    }
    auditors = Auditors().run(bundle, source)
    action = IntegrativeMeta().select(debated["any_correct"], probability["supported"], auditors["passed"])
    method = {
        "hypothesis": "metacognição com erro medido distingue acerto reproduzível de confiança solta",
        "baseline": control,
        "meta_error": meta["error"],
        "meta_confidence": meta["confidence"],
        "hits": inferred["prediction"] == truth,
        "reproducible_with_seed": cfg.seed,
        "failure_modes": ["consenso", "hash irreversível tratado como reversível", "sorteio tratado como previsível"],
        "controlled_change": auto["proposal"],
        "next_action": action,
    }
    report = {
        "system": SYSTEM_NAME,
        "version": VERSION,
        "status": STATUS,
        "limits": [
            "testes desta função só correm quando o arquivo é executado",
            "sem PyTorch, sem xadrez completo, sem canastra completa",
            "rede desligada por padrão",
            "910 nós são um grafo esparso, não uma rede neural treinada",
        ],
        "encoding": {
            "roundtrip_a1z26": a1z26_decode(a1z26_encode("nexus")) == "nexus",
            "roundtrip_utf8": utf8_decode(utf8_encode("não")) == "não",
            "hash_not_reversible": stable_hash("nexus") != "nexus",
            "nearest": rep.nearest("word"),
            "nonce": nonce,
        },
        "dynamics": dyn,
        "inference": inferred,
        "metacognition": meta,
        "recursive": recursive,
        "control_without_metacognition": control,
        "probability": probability,
        "debate": debated,
        "forgetting": forgetting,
        "graph": {"nodes": graph.n, "layers": cfg.graph_layers, "ops": graph.ops, "async_locked_sum": async_sum},
        "scales": scales_of(encoding, action),
        "games": games,
        "draws": draws,
        "generators": {k: v[:3] for k, v in generators().items()},
        "corpus_demo": corpus_stats("doubt is not proof and proof is not doubt"),
        "consciousness": inquiry,
        "autopoiesis": auto,
        "security": security,
        "auditors": auditors,
        "dictionary": DictionaryClient(cfg).lookup("nexus"),
        "yfinance": {"enabled": False, "lexical_utility_demonstrated": False},
        "method_between_errors_and_hits": method,
        "pd": game_theory_pd(),
        "log_entries": len(log.records),
    }
    safe_path(state_dir, "last_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return report


def assert_harness(report: Dict[str, Any]) -> List[str]:
    errors = []
    if report["dynamics"]["cosine_error"] > 1e-9:
        errors.append("identidade do cosseno falhou")
    if not report["encoding"]["roundtrip_a1z26"] or not report["encoding"]["roundtrip_utf8"]:
        errors.append("codificação reversível falhou")
    if report["graph"]["nodes"] != 910:
        errors.append("grafo não tem 910 nós")
    if report["graph"]["async_locked_sum"] != 100:
        errors.append("integridade assíncrona falhou")
    if report["status"]["agi"] or report["status"]["asi"]:
        errors.append("higiene de afirmação violada")
    if not report["security"]["passed"]:
        errors.append("auditoria de segurança do código falhou")
    if not report["auditors"]["passed"]:
        errors.append("auditores falharam: " + str(report["auditors"]["checks"]))
    if report["inference"]["prediction"] != 33:
        errors.append("inferência da sequência falhou")
    return errors


if __name__ == "__main__":
    cfg = Config()
    report = run_all(cfg)
    errors = assert_harness(report)
    summary = {
        "versao": VERSION,
        "nos": report["graph"]["nodes"],
        "acao": report["method_between_errors_and_hits"]["next_action"],
        "brier_adaptativo": report["probability"]["brier_adaptive"],
        "brier_referencia": report["probability"]["brier_reference"],
        "raphael": report["games"]["raphael"]["status"],
        "desvio_vitorias": [
            report["games"]["raphael"]["p0_wins_greedy"],
            report["games"]["raphael"]["p0_wins_deviant"],
        ],
        "esquecimento_gap": report["forgetting"]["retention_gap"],
        "consciencia": report["consciousness"]["phenomenal_consciousness"],
        "erros_de_harness": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)
