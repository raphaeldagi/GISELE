"""GRPO de uma decisão num bandido contextual com recompensa verificável (Parte 137).

Reescrita offline, só biblioteca padrão, de `externos/pacote3/rl_grupos.py`. Cinco features [1, x, y, xy, x² − y²] de um ponto
uniforme em [−1, 1]², três ações, uma política softmax linear (pesos 5×3), a recompensa 1 se a ação é a do oráculo (o argmax de
features·ORÁCULO, a mesma matriz do original) e 0 senão. Para cada grupo de G ações amostradas no mesmo contexto: vantagem normalizada
pelo grupo (a `vantagem_grpo` da Parte 87, reusada, com zero quando o grupo não tem contraste), razão de importância recortada em
[1 − ε, 1 + ε] e KL exata contra a referência uniforme congelada. A diferença para o original: os contextos e as amostras vêm do
`random` da biblioteca padrão (o original usa o gerador do numpy), então os números não são os do original, só o desenho.
"""
import math
import random

from synthai.plasticidade import vantagem_grpo

ORACULO = [[.1, -.1, 0.], [1., -1., .2], [.2, .7, -1.], [.25, -.3, .1], [.1, .05, -.15]]


def features(x, y):
    return [1.0, x, y, x * y, x * x - y * y]


def gerar_contextos(n, semente):
    r = random.Random(semente)
    return [features(r.uniform(-1, 1), r.uniform(-1, 1)) for _ in range(n)]


def logits(pesos, f):
    return [sum(f[i] * pesos[i][a] for i in range(5)) for a in range(3)]


def log_softmax(z):
    m = max(z)
    s = sum(math.exp(v - m) for v in z)
    return [v - m - math.log(s) for v in z]


def acao_otima(f):
    z = logits(ORACULO, f)
    return max(range(3), key=lambda a: z[a])


def vantagens_grupo(recompensas, eps=1e-8):
    """A vantagem do texto recebido: zero se o grupo não tem contraste; senão a da Parte 87."""
    if all(r == recompensas[0] for r in recompensas):
        return [0.0] * len(recompensas)
    return vantagem_grpo(recompensas, eps)


def vantagens_binarias_fechadas(G, k):
    """A forma fechada para recompensas 0/1 com k acertos em G (0 < k < G), sem o ε: p̂ = k/G, desvio √(p̂(1 − p̂)); o acerto
    recebe √((1 − p̂)/p̂) e o erro −√(p̂/(1 − p̂))."""
    p = k / G
    return math.sqrt((1 - p) / p), -math.sqrt(p / (1 - p))


def prob_sem_contraste(p, G):
    """P(as G recompensas do grupo são iguais) = p^G + (1 − p)^G, com p = π(ação ótima)."""
    return p ** G + (1 - p) ** G


def gradiente(pesos, f, acoes, logp_velha, vant, clip=0.2, beta=0.025):
    """Gradiente da perda −média(min(r·A, clip(r)·A)) + β·KL(π‖uniforme) em relação aos pesos (5×3), como no original."""
    logp = log_softmax(logits(pesos, f))
    p = [math.exp(v) for v in logp]
    G = len(acoes)
    dlog = [0.0, 0.0, 0.0]
    for a, lv, A in zip(acoes, logp_velha, vant):
        razao = math.exp(logp[a] - lv)
        ativa = not ((A > 0 and razao > 1 + clip) or (A < 0 and razao < 1 - clip))
        if ativa:
            for b in range(3):
                score = (1.0 if b == a else 0.0) - p[b]
                dlog[b] -= razao * A / G * score
    ref = -math.log(3.0)
    diff = [v - ref for v in logp]
    kl = sum(pi * di for pi, di in zip(p, diff))
    for b in range(3):
        dlog[b] += beta * p[b] * (diff[b] - kl)
    return [[f[i] * dlog[b] for b in range(3)] for i in range(5)]


def treinar(contextos, G, orcamento=4096, semente=41, taxa=0.15, passes=3, clip=0.2, beta=0.025):
    """Treina com orcamento/G grupos. Devolve (pesos, grupos sem contraste, grupos)."""
    pesos = [[0.0] * 3 for _ in range(5)]
    escolha = random.Random(semente * 1000 + 367)
    amostra = random.Random(semente * 1000 + G)
    sem = 0
    for _ in range(orcamento // G):
        f = contextos[escolha.randrange(len(contextos))]
        lv = log_softmax(logits(pesos, f))
        pv = [math.exp(v) for v in lv]
        acoes = amostra.choices(range(3), weights=pv, k=G)
        rec = [1.0 if a == acao_otima(f) else 0.0 for a in acoes]
        vant = vantagens_grupo(rec)
        sem += all(v == 0.0 for v in vant)
        lva = [lv[a] for a in acoes]
        for _ in range(passes):
            g = gradiente(pesos, f, acoes, lva, vant, clip, beta)
            pesos = [[pesos[i][b] - taxa * g[i][b] for b in range(3)] for i in range(5)]
    return pesos, sem, orcamento // G


def retorno_esperado(pesos, contextos):
    """A média exata de π(ação ótima | contexto) nos contextos dados (como o `avaliar` do original)."""
    t = 0.0
    for f in contextos:
        t += math.exp(log_softmax(logits(pesos, f))[acao_otima(f)])
    return t / len(contextos)
