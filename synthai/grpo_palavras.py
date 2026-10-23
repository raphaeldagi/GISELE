"""A GRPO de `externos/pacote3/rl_grupos.py` aplicada ao jogo de palavras de `externos/word_rl_lab/` (Parte 147): dois módulos recebidos,
juntos, sobre o dicionário. A política é um softmax tabular por prefixo (logits θ[(prefixo, ação)]); cada grupo são G episódios na MESMA
grade e com o MESMO início (o "mesmo enunciado" da GRPO); a vantagem é a recompensa normalizada pelo grupo (`vantagens_grupo`, Parte 137);
o passo é o gradiente REINFORCE de log π ao longo de cada trajetória: θ[s, b] += taxa · A · (1[b = a] − π(b|s)). Sem crítico, sem tabela de
valor. O ambiente, as ações e a recompensa são os de `synthai.palavras_rl` (Parte 111), reusados.
"""
import math
import random

from synthai.grpo_bandido import vantagens_grupo
from synthai.palavras_rl import (FAIL_REWARD, STOP, WordGridEnv, valid_actions, word_score)


class AgenteGRPO:
    def __init__(self, taxa=0.5, seed=0):
        self.taxa = taxa
        self.rng = random.Random(seed)
        self.theta = {}

    def probs(self, s, acoes):
        z = [self.theta.get((s, a), 0.0) for a in acoes]
        m = max(z)
        e = [math.exp(v - m) for v in z]
        t = sum(e)
        return [v / t for v in e]

    def choose(self, s, acoes, mode):
        """A interface do QAgent: 'greedy' = argmax dos logits (desempate pelo gerador), senão amostra de π."""
        if mode == "random":
            return self.rng.choice(acoes)
        if mode == "greedy":
            z = [self.theta.get((s, a), 0.0) for a in acoes]
            m = max(z)
            return self.rng.choice([a for a, v in zip(acoes, z) if v == m])
        p = self.probs(s, acoes)
        return self.rng.choices(acoes, weights=p, k=1)[0]

    def value(self, s, a):
        return self.theta.get((s, a), 0.0)

    def update(self, *args):  # o run_episode chama update; a GRPO atualiza por grupo, não por passo
        pass


def episodio_amostrado(env, dic, agente, inicio):
    """Um episódio na grade ATUAL do ambiente, a partir de `inicio`, amostrando de π. Devolve (trajetória [(s, ações, a)], recompensa, válida)."""
    path, prefix, traj = [inicio], env.letter(inicio), []
    while True:
        acts = valid_actions(env, path)
        if not acts:
            return traj, FAIL_REWARD, False
        nomes = list(acts)
        a = agente.choose(prefix, nomes, "amostra")
        traj.append((prefix, nomes, a))
        if a == STOP:
            ok = dic.is_word(prefix)
            return traj, (float(word_score(prefix)) if ok else FAIL_REWARD), ok
        path.append(acts[a])
        prefix += a


def treinar(dic, episodios=5000, G=8, taxa=0.5, tamanho=5, min_len=3, max_len=5, seed=42):
    """episodios/G grupos; cada grupo sorteia uma grade e um início e roda G episódios nela. Devolve (agente, grupos sem contraste, grupos)."""
    env = WordGridEnv(tamanho, min_len, max_len, rng=random.Random(seed))
    agente = AgenteGRPO(taxa, seed=seed + 1)
    sem = 0
    n = episodios // G
    for _ in range(n):
        env.reset()
        inicio = (env.rng.randrange(env.size), env.rng.randrange(env.size))
        rollouts = [episodio_amostrado(env, dic, agente, inicio) for _ in range(G)]
        vant = vantagens_grupo([r for _, r, _ in rollouts])
        if all(v == 0.0 for v in vant):
            sem += 1
            continue
        for (traj, _, _), A in zip(rollouts, vant):
            for s, nomes, a in traj:
                p = agente.probs(s, nomes)
                for b, pb in zip(nomes, p):
                    agente.theta[(s, b)] = agente.theta.get((s, b), 0.0) + taxa * A / G * ((1.0 if b == a else 0.0) - pb)
    return agente, sem, n
