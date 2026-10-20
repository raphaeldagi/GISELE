"""O NEXUS–RAPHAEL 2.2.0 enviado na Parte 121 (externos/nexus_raphael_v2_0/nexus_raphael_v2_0.py.txt), medido no próprio código.

O arquivo recebido não é importado nem executado (regra da Parte 72): ele grava num diretório, tem rede (desligada por padrão, ligável por
--online) e se roda como programa. Aqui as peças que fazem afirmações medíveis estão TRANSCRITAS com o mesmo comportamento (`recebido_*`, a
mesma ordem de sorteios e de contas, sem o repositório em disco), ao lado das contas independentes que as conferem e das correções. Biblioteca
padrão."""

import collections
import math
import random
import statistics


# --- transcrições do arquivo recebido ---

def recebido_beta_prever(a, b):
    return a / (a + b)


def recebido_pontuar(probs, rotulos, faixas=10):
    """AvaliadorProbabilistico.pontuar: Brier, perda logarítmica, ECE (média por faixa) e acurácia."""
    brier = statistics.fmean((p - y) ** 2 for p, y in zip(probs, rotulos))
    perda = -statistics.fmean(y * math.log(max(1e-15, p)) + (1 - y) * math.log(max(1e-15, 1 - p)) for p, y in zip(probs, rotulos))
    ece = 0.0
    for faixa in range(faixas):
        pares = [(p, y) for p, y in zip(probs, rotulos) if min(faixas - 1, int(p * faixas)) == faixa]
        if pares:
            ece += len(pares) / len(probs) * abs(statistics.fmean(p for p, _ in pares) - statistics.fmean(y for _, y in pares))
    acuracia = statistics.fmean(int(p >= .5) == y for p, y in zip(probs, rotulos))
    return dict(brier=brier, log_loss=perda, ece=ece, acuracia=acuracia)


def recebido_bootstrap_ganho(erros_base, erros_modelo, seed, repeticoes=1000):
    deltas = [a - b for a, b in zip(erros_base, erros_modelo)]
    media = statistics.fmean(deltas)
    rng = random.Random(seed)
    n = len(deltas)
    replicas = sorted(sum(deltas[rng.randrange(n)] for _ in range(n)) / n for _ in range(repeticoes))
    return media, replicas[int(.025 * (repeticoes - 1))], replicas[int(.975 * (repeticoes - 1))]


def recebido_probabilidade(modo="rapido", seeds=(0, 1, 2, 3, 4), bootstrap=1000):
    """Experimentos.probabilidade (H-M3-001): Beta global contra Beta por grupo, P(y=1|x) = 0,15 ou 0,85. Devolve [(ganho, inf, sup, veredito)]."""
    n = 300 if modo == "rapido" else (1_500 if modo == "padrao" else 8_000)
    out = []
    for seed in seeds:
        rng = random.Random(seed)
        amostras = [(rng.randrange(2), None) for _ in range(n)]
        amostras = [(x, int(rng.random() < (.15 if x == 0 else .85))) for x, _ in amostras]
        treino, teste = amostras[:int(.6 * n)], amostras[int(.8 * n):]
        g = [1.0, 1.0]
        grupos = {0: [1.0, 1.0], 1: [1.0, 1.0]}
        for x, y in treino:
            g[0] += y
            g[1] += 1 - y
            grupos[x][0] += y
            grupos[x][1] += 1 - y
        y_t = [y for _, y in teste]
        pb = [recebido_beta_prever(*g) for _ in teste]
        pc = [recebido_beta_prever(*grupos[x]) for x, _ in teste]
        ganho, inf, sup = recebido_bootstrap_ganho([(p - y) ** 2 for p, y in zip(pb, y_t)], [(p - y) ** 2 for p, y in zip(pc, y_t)],
                                                   seed + 100, bootstrap)
        out.append((ganho, inf, sup, "ACEITA" if inf > 0 else "REJEITADA" if sup <= 0 else "INCONCLUSIVA"))
    return out


class RecebidaLogistica:
    """RegressaoLogistica do arquivo: descida do gradiente com taxa 0,8 e 300 passos."""

    def __init__(self, dimensoes):
        self.pesos = [0.0] * (dimensoes + 1)

    @staticmethod
    def sigmoide(z):
        if z >= 0:
            return 1.0 / (1 + math.exp(-z))
        e = math.exp(z)
        return e / (1 + e)

    def predizer(self, x):
        return self.sigmoide(self.pesos[0] + sum(a * b for a, b in zip(self.pesos[1:], x)))

    def treinar(self, dados, passos=300, taxa=.8):
        for _ in range(passos):
            g = [0.0] * len(self.pesos)
            for x, y in dados:
                r = self.predizer(x) - y
                g[0] += r
                for i, v in enumerate(x):
                    g[i + 1] += r * v
            self.pesos = [p - taxa * v / len(dados) for p, v in zip(self.pesos, g)]


def recebido_angulo(modo="rapido", seeds=(0, 1, 2, 3, 4), bootstrap=1000):
    """experimento_angulo (H-M2-001): y = 1[cos²θ > 0,49]; logística com cos θ contra com (cos θ, cos 2θ). Devolve
    [(Brier base, Brier transformado, ganho, inf, sup)]."""
    n = 500 if modo == "rapido" else (1200 if modo == "padrao" else 4000)
    out = []
    for seed in seeds:
        rng = random.Random(seed)
        amostras = [(rng.uniform(-math.pi, math.pi), None) for _ in range(n)]
        amostras = [(t, int(math.cos(t) ** 2 > .49)) for t, _ in amostras]
        treino, teste = amostras[:int(.6 * n)], amostras[int(.8 * n):]
        b, t2 = RecebidaLogistica(1), RecebidaLogistica(2)
        b.treinar([([math.cos(t)], y) for t, y in treino])
        t2.treinar([([math.cos(t), math.cos(2 * t)], y) for t, y in treino])
        y_t = [y for _, y in teste]
        pb = [b.predizer([math.cos(t)]) for t, _ in teste]
        pt = [t2.predizer([math.cos(t), math.cos(2 * t)]) for t, _ in teste]
        eb, et = [(p - y) ** 2 for p, y in zip(pb, y_t)], [(p - y) ** 2 for p, y in zip(pt, y_t)]
        d, li, ls = recebido_bootstrap_ganho(eb, et, seed + 101, bootstrap)
        out.append((statistics.fmean(eb), statistics.fmean(et), d, li, ls))
    return out


def recebido_megasena(modo="rapido", seed=42, bootstrap=1000):
    """MegaSenaLaboratorio.realizar sem o disco: médias de acertos, a diferença quentes − aleatória, o IC pelos índices FIXOS [24] e [974]
    da réplica ordenada, e o qui-quadrado das frequências. Devolve um dict (ou levanta IndexError se bootstrap < 975)."""
    rng = random.Random(seed)
    n = 400 if modo == "rapido" else (2900 if modo == "padrao" else 10000)
    sorteios = [set(rng.sample(range(1, 61), 6)) for _ in range(n)]
    res = {p: [] for p in ("quentes", "frias", "aleatoria")}
    deltas = []
    for pos in range(100, n):
        passado = collections.Counter(x for s in sorteios[pos - 100:pos] for x in s)
        ranking = sorted(range(1, 61), key=lambda x: (-passado[x], x))
        quentes, frias = set(ranking[:6]), set(ranking[-6:])
        aleatoria = set(rng.sample(range(1, 61), 6))
        futuro = sorteios[pos]
        for nome, e in (("quentes", quentes), ("frias", frias), ("aleatoria", aleatoria)):
            res[nome].append(len(e & futuro))
        deltas.append(len(quentes & futuro) - len(aleatoria & futuro))
    rng_boot = random.Random(seed + 999)
    replicas = sorted(statistics.fmean(deltas[rng_boot.randrange(len(deltas))] for _ in deltas) for _ in range(bootstrap))
    ic = [replicas[24], replicas[974]]
    contagem = collections.Counter(x for s in sorteios for x in s)
    esperado = n / 10
    qui2 = sum((contagem[x] - esperado) ** 2 / esperado for x in range(1, 61))
    return dict(medias={k: statistics.fmean(v) for k, v in res.items()}, delta=statistics.fmean(deltas), ic=ic, qui2=qui2,
                replicas=replicas, veredito="ACEITA" if ic[0] > 0 else "REJEITADA" if ic[1] <= 0 else "INCONCLUSIVA")


def recebido_bandido(seed, tipo, passos=1000):
    """BandidoContextual.simular: dois braços (0,75 e 0,55), ε = 0,1; a recompensa extraordinária é acerto − (1 − acerto) + 0,4·diagnóstico·(1 −
    acerto). A avaliação reservada usa random.Random(seed + 10000) e só o braço escolhido. Devolve (braço escolhido, desempenho reservado)."""
    rng = random.Random(seed)
    q, usos = [0., 0.], [0, 0]
    for _ in range(passos):
        acao = rng.randrange(2) if rng.random() < .1 else (0 if q[0] >= q[1] else 1)
        acerto = int(rng.random() < (.75 if acao == 0 else .55))
        diag = int(acerto == 0 and rng.random() < .5)
        r = float(acerto) if tipo == "ordinario" else acerto - 1.0 * (1 - acerto) + .4 * diag * (1 - acerto)
        usos[acao] += 1
        q[acao] += (r - q[acao]) / usos[acao]
    melhor = 0 if q[0] >= q[1] else 1
    av = random.Random(seed + 10000)
    return melhor, statistics.fmean(int(av.random() < (.75 if melhor == 0 else .55)) for _ in range(200))


VITORIAS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def _vencedor(t):
    for i, j, k in VITORIAS:
        if t[i] != "." and t[i] == t[j] == t[k]:
            return t[i]
    return None


def recebido_contar_estados_velha():
    """contar_estados_velha: busca em profundidade com o conjunto de tabuleiros vistos."""
    vistos = set()

    def visitar(t, j):
        if t in vistos:
            return
        vistos.add(t)
        if _vencedor(t) or "." not in t:
            return
        for i, c in enumerate(t):
            if c == ".":
                visitar(t[:i] + j + t[i + 1:], "O" if j == "X" else "X")
    visitar("." * 9, "X")
    return len(vistos)


def recebido_lyapunov(r, n=20_000, descarte=2_000):
    x = 0.123456789
    valores = []
    for i in range(n + descarte):
        x = r * x * (1 - x)
        if i >= descarte:
            valores.append(math.log(max(1e-300, abs(r * (1 - 2 * x)))))
    return statistics.fmean(valores)


# --- contas independentes e correções ---

def estados_velha_por_camadas():
    """Os tabuleiros alcançáveis contados por outro caminho: camada por camada (número de jogadas), sem recursão, parando nos terminais."""
    camada = {"." * 9}
    total = 1
    for k in range(9):
        j = "X" if k % 2 == 0 else "O"
        nova = set()
        for t in camada:
            if _vencedor(t) or "." not in t:
                continue
            for i, c in enumerate(t):
                if c == ".":
                    nova.add(t[:i] + j + t[i + 1:])
        total += len(nova)
        camada = nova
    return total


def valor_velha_alfa_beta(t="." * 9, j="X", alfa=-2, beta=2):
    """O valor do jogo da velha (para quem joga) por negamax com poda alfa-beta: outro algoritmo que o minimax com memória do arquivo."""
    v = _vencedor(t)
    if v:
        return 1 if v == j else -1
    if "." not in t:
        return 0
    outro = "O" if j == "X" else "X"
    melhor = -2
    for i, c in enumerate(t):
        if c == ".":
            x = -valor_velha_alfa_beta(t[:i] + j + t[i + 1:], outro, -beta, -alfa)
            melhor = max(melhor, x)
            alfa = max(alfa, x)
            if alfa >= beta:
                break
    return melhor


def ic_por_quantis(replicas, nivel=0.95):
    """A correção do IC da Mega-Sena: os índices dos quantis saem do número de réplicas, não de constantes."""
    r = sorted(replicas)
    m = len(r)
    a = (1 - nivel) / 2
    return [r[int(a * (m - 1))], r[int((1 - a) * (m - 1))]]


def megasena_fechada():
    """As probabilidades exatas do arquivo (combinatória) e a esperança do qui-quadrado das frequências: cada dezena está num sorteio com
    probabilidade 6/60, independente entre sorteios, então E[(c − n/10)²/(n/10)] = 1 − 1/10 e a soma das 60 dá 54 (não 59)."""
    total = math.comb(60, 6)
    return dict(total=total, sena=1 / total, quina=math.comb(6, 5) * math.comb(54, 1) / total,
                quadra=math.comb(6, 4) * math.comb(54, 2) / total, acertos=6 * 6 / 60, e_qui2=60 * (1 - 0.1))
