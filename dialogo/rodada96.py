"""Rodada 96 do diálogo Python <-> Java (Parte 148): o passo da GRPO de synthai.grpo_palavras (a GRPO de externos/pacote3/rl_grupos.py no
jogo de palavras de externos/word_rl_lab) bit a bit, num jogo de brinquedo: alfabeto {a, b, c}, prefixos de até 3 letras, a ação P (parar)
ou uma letra, 5 palavras válidas, recompensa = pontuação de Scrabble × comprimento (a = 1, b = c = 3) ou −1. Softmax tabular por prefixo
com o exp PRÓPRIO da rodada 26; vantagem (r − média)/(desvio populacional + 1e-8), zero sem contraste; θ[s, b] += taxa · A/G · (1[b = a] − π(b|s)).
O acaso vem de um LCG; 40 grupos de G = 4 no mesmo início, taxa 0,5; somas em laço (Parte 34). Antes de imprimir, confere que um passo
desta tradução fica a menos de 1e-12 do passo com as probabilidades do módulo real (math.exp). Da raiz: python3 dialogo/rodada96.py"""
import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
_spec = importlib.util.spec_from_file_location("rodada26", os.path.join(AQUI, "rodada26.py"))
r26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r26)
exp_ = r26.exp_
from synthai.grpo_palavras import AgenteGRPO  # noqa: E402

PALAVRAS = {"ab", "ba", "abc", "cab", "ca"}
PONTOS = {"a": 1, "b": 3, "c": 3}
x = 14896


def u():
    global x
    x = (1103515245 * x + 12345) % 2147483648
    return x / 2147483648.0


def acoes(s):
    return ["P", "a", "b", "c"] if len(s) < 3 else ["P"]


def probs(theta, s, acts):
    z = [theta.get(s + "|" + a, 0.0) for a in acts]
    m = z[0]
    for v in z:
        m = v if v > m else m
    e = [exp_(v - m) for v in z]
    t = 0.0
    for v in e:
        t += v
    return [v / t for v in e]


def recompensa(w):
    if w not in PALAVRAS:
        return -1.0
    t = 0
    for c in w:
        t += PONTOS[c]
    return float(t * len(w))


def episodio(theta, inicio):
    s, traj = inicio, []
    while True:
        acts = acoes(s)
        p = probs(theta, s, acts)
        r, acum, a = u(), 0.0, acts[-1]
        for b, pb in zip(acts, p):
            acum += pb
            if r < acum:
                a = b
                break
        traj.append((s, acts, a))
        if a == "P":
            return traj, recompensa(s)
        s += a


def vantagens(rec):
    G = len(rec)
    if all(r == rec[0] for r in rec):
        return [0.0] * G
    s = 0.0
    for r in rec:
        s += r
    media = s / G
    v = 0.0
    for r in rec:
        v += (r - media) * (r - media)
    desvio = math.sqrt(v / G)
    return [(r - media) / (desvio + 1e-8) for r in rec]


def passo(theta, s, acts, a, coef):
    p = probs(theta, s, acts)
    for b, pb in zip(acts, p):
        k = s + "|" + b
        theta[k] = theta.get(k, 0.0) + coef * ((1.0 if b == a else 0.0) - pb)


def main():
    theta, G, taxa, total, sem = {}, 4, 0.5, 0.0, 0
    conferido = False
    for _ in range(40):
        inicio = "abc"[int(u() * 3)]
        rollouts = [episodio(theta, inicio) for _ in range(G)]
        for _, r in rollouts:
            total += r
        vant = vantagens([r for _, r in rollouts])
        if all(v == 0.0 for v in vant):
            sem += 1
            continue
        for (traj, _), A in zip(rollouts, vant):
            for s, acts, a in traj:
                if not conferido and len(theta) > 2:  # o mesmo passo com as probabilidades do módulo (math.exp)
                    ag = AgenteGRPO()
                    ag.theta = {(k.split("|")[0], k.split("|")[1]): v for k, v in theta.items()}
                    pm = ag.probs(s, acts)
                    pr = probs(theta, s, acts)
                    assert max(abs(c - d) for c, d in zip(pm, pr)) < 1e-12
                    conferido = True
                passo(theta, s, acts, a, taxa * A / G)
    for k in sorted(theta):
        print(k + " " + theta[k].hex())
    print("total " + total.hex())
    print("sem_contraste " + str(sem))
    print("conferido " + str(conferido))
    print("fim")


if __name__ == "__main__":
    main()
