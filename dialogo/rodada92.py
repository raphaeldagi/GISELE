"""Rodada 92 do diálogo Python <-> Java (Parte 139): a GRPO de synthai.grpo_bandido (de externos/pacote3/rl_grupos.py) bit a bit.
16 contextos e as amostras de ações vêm de um LCG; G = 4, 64 grupos, 3 passes por grupo, taxa 0,15, recorte 0,2, KL 0,025 contra a
uniforme. O log-softmax usa o exp e o log PRÓPRIOS da rodada 26 (a libm é fronteira, Parte 52). As somas são em laço (o sum() do
Python 3.12 é compensado, Parte 34). A vantagem segue a da Parte 87: (r − média)/(desvio populacional + 1e-8), zero sem contraste.
Antes de imprimir, confere que o gradiente desta tradução fica a menos de 1e-12 do gradiente do módulo real nos mesmos dados.
Imprime os 15 pesos finais e o retorno exato médio em hexadecimal. Da raiz: python3 dialogo/rodada92.py"""
import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
_spec = importlib.util.spec_from_file_location("rodada26", os.path.join(AQUI, "rodada26.py"))
r26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r26)
exp_, log_ = r26.exp_, r26.log_
from synthai import grpo_bandido as gb  # noqa: E402

ORACULO = gb.ORACULO
x = 13092


def u():
    global x
    x = (1103515245 * x + 12345) % 2147483648
    return x / 2147483648.0


def logits(w, f):
    z = []
    for a in range(3):
        t = 0.0
        for i in range(5):
            t += f[i] * w[i][a]
        z.append(t)
    return z


def log_softmax(z):
    m = z[0] if z[0] >= z[1] else z[1]
    m = m if m >= z[2] else z[2]
    s = 0.0
    for v in z:
        s += exp_(v - m)
    ls = log_(s)
    return [v - m - ls for v in z]


def acao_otima(f):
    z = logits(ORACULO, f)
    best = 0
    for a in (1, 2):
        if z[a] > z[best]:
            best = a
    return best


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


def gradiente(w, f, acoes, lv, vant, clip=0.2, beta=0.025):
    logp = log_softmax(logits(w, f))
    p = [exp_(v) for v in logp]
    G = len(acoes)
    d = [0.0, 0.0, 0.0]
    for a, l, A in zip(acoes, lv, vant):
        razao = exp_(logp[a] - l)
        ativa = not ((A > 0 and razao > 1 + clip) or (A < 0 and razao < 1 - clip))
        if ativa:
            for b in range(3):
                score = (1.0 if b == a else 0.0) - p[b]
                d[b] -= razao * A / G * score
    ref = -log_(3.0)
    diff = [v - ref for v in logp]
    kl = 0.0
    for pi, di in zip(p, diff):
        kl += pi * di
    for b in range(3):
        d[b] += beta * p[b] * (diff[b] - kl)
    return [[f[i] * d[b] for b in range(3)] for i in range(5)]


def main():
    ctx = [gb.features(2.0 * u() - 1.0, 2.0 * u() - 1.0) for _ in range(16)]
    w = [[0.0] * 3 for _ in range(5)]
    conferido = False
    for _ in range(64):
        f = ctx[int(u() * 16)]
        lv = log_softmax(logits(w, f))
        pv = [exp_(v) for v in lv]
        acoes = []
        for _ in range(4):
            r = u()
            a = 0 if r < pv[0] else (1 if r < pv[0] + pv[1] else 2)
            acoes.append(a)
        otima = acao_otima(f)
        rec = [1.0 if a == otima else 0.0 for a in acoes]
        vant = vantagens(rec)
        lva = [lv[a] for a in acoes]
        for _ in range(3):
            g = gradiente(w, f, acoes, lva, vant)
            if not conferido and any(vant):
                gm = gb.gradiente(w, f, acoes, lva, gb.vantagens_grupo(rec))
                assert max(abs(g[i][b] - gm[i][b]) for i in range(5) for b in range(3)) < 1e-12
                conferido = True
            w = [[w[i][b] - 0.15 * g[i][b] for b in range(3)] for i in range(5)]
    for i in range(5):
        for b in range(3):
            print("w" + str(i) + str(b) + " " + w[i][b].hex())
    t = 0.0
    for f in ctx:
        t += exp_(log_softmax(logits(w, f))[acao_otima(f)])
    print("retorno " + (t / 16).hex())
    print("conferido " + str(conferido))
    print("fim")


if __name__ == "__main__":
    main()
