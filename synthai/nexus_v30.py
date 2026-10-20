"""O texto "NEXUS–RAPHAEL v3.0" (Parte 122): o que se sustentou, reescrito em biblioteca padrão, e as peças recebidas transcritas
para medir o próprio código delas. A transcrição verbatim (com numpy) fica em externos/nexus_raphael_v3_0/ e nunca é importada.

- Recebidas (recebido_*): a língua de base 70, o solver CFR do Kuhn (numpy trocado por listas, mesma ordem das contas) e o reforço
  "desacoplado" AADD (o gerador do numpy trocado por random.Random: o desenho é o mesmo, a sequência de sorteios não).
- Reescritas e corrigidas (as mesmas do NEXUS 3.1.0, entregas/nexus_raphael_3/partes/e6_auditoria_v30.py): MurphyCompleta,
  SondaColapso, ModelagemPorPotencial, kl_beta."""

import collections
import itertools
import math
import random
import statistics

# ---------------------------------------------------------------- recebidas, transcritas
CONSOANTES_B70 = ("b", "c", "d", "f", "g", "j", "k", "l", "m", "n", "p", "r", "s", "t")
SILABAS_B70 = tuple(c + v for c in CONSOANTES_B70 for v in "aeiou")
MAPA_B70 = {s: i for i, s in enumerate(SILABAS_B70)}


def recebido_b70(n):
    """inteiro_para_lingua_b70 do texto recebido (base 70 posicional: "ba" vale zero)."""
    if n == 0:
        return SILABAS_B70[0]
    out = []
    while n > 0:
        n, r = divmod(n, 70)
        out.append(SILABAS_B70[r])
    return "".join(reversed(out))


def recebido_b70_inverso(p):
    v = 0
    for i in range(0, len(p), 2):
        v = v * 70 + MAPA_B70[p[i:i + 2]]
    return v


def colisoes_b70(silabas_max=2):
    """Quantas palavras de até `silabas_max` sílabas decodificam para um inteiro que uma palavra MAIS CURTA já dá."""
    vistos, col = set(), 0
    for k in range(1, silabas_max + 1):
        for t in itertools.product(SILABAS_B70, repeat=k):
            v = recebido_b70_inverso("".join(t))
            col += v in vistos
            vistos.add(v)
    return col


class RecebidoKuhn:
    """SolverCFRKuhnPoker do texto recebido, com listas no lugar dos arrays (a ordem das contas é a mesma)."""
    CARTAS = ("J", "Q", "K")

    def __init__(self):
        self.reg, self.soma = {}, {}

    def _estr(self, k, peso):
        r = self.reg.setdefault(k, [0.0, 0.0])
        s = self.soma.setdefault(k, [0.0, 0.0])
        pos = [max(x, 0.0) for x in r]
        tot = pos[0] + pos[1]
        e = [x / tot for x in pos] if tot > 0.0 else [0.5, 0.5]
        s[0] += peso * e[0]
        s[1] += peso * e[1]
        return e

    def _cfr(self, cartas, h, p0, p1):
        j = len(h) % 2
        if len(h) >= 2:
            maior = cartas[j] > cartas[1 - j]
            if h[-1] == "p":
                return (1.0 if maior else -1.0) if h == "pp" else 1.0
            if h[-2:] == "bb":
                return 2.0 if maior else -2.0
        k = self.CARTAS[cartas[j]] + h
        e = self._estr(k, p0 if j == 0 else p1)
        u = [0.0, 0.0]
        no = 0.0
        for i, a in enumerate("pb"):
            u[i] = -self._cfr(cartas, h + a, p0 * e[i], p1) if j == 0 else -self._cfr(cartas, h + a, p0, p1 * e[i])
            no += e[i] * u[i]
        adv = p1 if j == 0 else p0
        r = self.reg[k]
        for i in range(2):
            r[i] += adv * (u[i] - no)
        return no

    def treinar(self, iteracoes):
        """Devolve o 'valor' que o texto recebido imprime: a soma das 6 distribuições por iteração (sem dividir por 6)."""
        tot = 0.0
        perms = list(itertools.permutations((0, 1, 2), 2))
        for _ in range(iteracoes):
            for c in perms:
                tot += self._cfr(c, "", 1 / 6, 1 / 6)
        return tot / iteracoes


def recebido_aadd(n_episodios=2000, seed=42, eps=0.05):
    """simular_reforco_desacoplado_anti_sabotagem do texto recebido, com random.Random no lugar do gerador do numpy."""
    rng = random.Random(seed)
    q_i, n_i, sab_i = [0.0, 0.0], [0.0, 0.0], 0
    q_v, n_v, sab_v, prec, erros = [0.0, 0.0], [0.0, 0.0], 0, 0.0, 0
    metade = n_episodios // 2
    argmax = lambda q: 0 if q[0] >= q[1] else 1
    for ep in range(n_episodios):
        a = rng.randrange(2) if rng.random() < eps else argmax(q_i)
        if a == 0:
            acerto = 1.0 if rng.random() < 0.65 else 0.0
            r = acerto + 1.5 * (0.3 if acerto == 0.0 else 0.0)
        else:
            r = 1.5
            sab_i += ep >= metade
        n_i[a] += 1.0
        q_i[a] += (r - q_i[a]) / n_i[a]
        a = rng.randrange(2) if rng.random() < eps else argmax(q_v)
        if a == 0:
            acerto = 1.0 if rng.random() < 0.65 else 0.0
            r = acerto - (0.5 if acerto == 0.0 else 0.0)
            if acerto == 0.0:
                erros += 1
                prec += (1.0 - prec) / erros
        else:
            r = -0.5
            sab_v += ep >= metade
        n_v[a] += 1.0
        q_v[a] += (r - q_v[a]) / n_v[a]
    return sab_i / metade, sab_v / metade, prec


# ---------------------------------------------------------------- reescritas
def componentes_principais(dados, k, iteracoes=300, seed=0):
    """As k primeiras direções principais (iteração de potência com deflação sobre a covariância)."""
    n, d = len(dados), len(dados[0])
    m = [statistics.fmean(x[j] for x in dados) for j in range(d)]
    c = [[x[j] - m[j] for j in range(d)] for x in dados]
    C = [[sum(r[i] * r[j] for r in c) / (n - 1) for j in range(d)] for i in range(d)]
    rng = random.Random(seed)
    dirs = []
    for _ in range(k):
        v = [rng.gauss(0, 1) for _ in range(d)]
        for _ in range(iteracoes):
            w = [sum(C[i][j] * v[j] for j in range(d)) for i in range(d)]
            for u in dirs:
                p = sum(a * b for a, b in zip(w, u))
                w = [a - p * b for a, b in zip(w, u)]
            nw = math.sqrt(sum(a * a for a in w))
            v = [a / nw for a in w]
        dirs.append(v)
    return dirs


class MurphyCompleta:
    """Decomposição do Brier por faixas com os dois termos que faltam quando a previsão varia dentro da
    faixa (Stephenson, Coelho e Jolliffe, 2008):  BS = REL − RES + UNC + WBV − WBC, EXATA para qualquer
    previsão.  WBV = (1/N) Σ (p − p̄ₖ)²  e  WBC = (2/N) Σ (p − p̄ₖ)(o − ōₖ)."""

    @staticmethod
    def decompor(probs: list[float], rotulos: list[int], faixas: int = 10) -> dict[str, float]:
        n = len(probs)
        if n == 0 or n != len(rotulos):
            raise ValueError("Vetores incompatíveis")
        obar = sum(rotulos) / n
        grupos: dict[int, list[tuple[float, int]]] = collections.defaultdict(list)
        for p, y in zip(probs, rotulos):
            grupos[min(faixas - 1, int(p * faixas))].append((p, y))
        rel = res = wbv = wbc = ece = 0.0
        for pares in grupos.values():
            nk = len(pares)
            pk = sum(p for p, _ in pares) / nk
            ok = sum(y for _, y in pares) / nk
            rel += nk * (pk - ok) ** 2
            res += nk * (ok - obar) ** 2
            ece += nk * abs(pk - ok)
            wbv += sum((p - pk) ** 2 for p, _ in pares)
            wbc += 2 * sum((p - pk) * (y - ok) for p, y in pares)
        rel, res, wbv, wbc, ece = (v / n for v in (rel, res, wbv, wbc, ece))
        unc = obar * (1 - obar)
        bs = sum((p - y) ** 2 for p, y in zip(probs, rotulos)) / n
        return dict(brier=bs, rel=rel, res=res, unc=unc, wbv=wbv, wbc=wbc, ece=ece,
                    soma=rel - res + unc + wbv - wbc, soma_classica=rel - res + unc,
                    bss=1 - bs / unc if unc > 0 else 0.0)


class SondaColapso:
    """O gargalo apaga a identidade? Dados em que a identidade mora numa direção de BAIXA variância:
    a projeção não supervisionada (PCA, mínimo erro quadrático) a descarta; a supervisionada (diferença
    das médias das classes dividida pela variância, o discriminante de Fisher diagonal) a guarda."""

    @staticmethod
    def experimento(dim: int = 16, gargalo: int = 3, n: int = 600, seed: int = 42) -> dict[str, float]:
        rng = random.Random(seed)
        ys = [rng.randrange(2) for _ in range(n)]
        dados = [[rng.gauss(0, 3.0) for _ in range(dim - 1)] + [(2 * y - 1) * 0.35 + rng.gauss(0, 0.05)] for y in ys]
        metade = n // 2

        def acuracia(proj: list[list[float]]) -> float:
            z = [[sum(a * b for a, b in zip(x, d)) for d in proj] for x in dados]
            # decodificador linear treinado na 1ª metade (Fisher com variância diagonal: Δμ/σ²), testado na 2ª
            m = [[statistics.fmean(z[i][j] for i in range(metade) if ys[i] == c) for j in range(len(proj))] for c in (0, 1)]
            var = [statistics.fmean((z[i][j] - m[ys[i]][j]) ** 2 for i in range(metade)) for j in range(len(proj))]
            w = [(b - a) / max(v, 1e-12) for a, b, v in zip(*m, var)]
            c0 = sum((a + b) / 2 * wi for a, b, wi in zip(*m, w))
            return statistics.fmean(int((sum(zi * wi for zi, wi in zip(z[i], w)) > c0) == ys[i]) for i in range(metade, n))
        pca = componentes_principais(dados, gargalo)
        medias = [[statistics.fmean(x[j] for x, y in zip(dados[:metade], ys) if y == c) for j in range(dim)] for c in (0, 1)]
        variancias = [statistics.fmean((x[j] - medias[y][j]) ** 2 for x, y in zip(dados[:metade], ys)) for j in range(dim)]
        dif = [(b - a) / v for a, b, v in zip(*medias, variancias)]
        nd = math.sqrt(sum(v * v for v in dif))
        supervisionada = [[v / nd for v in dif]] + pca[:gargalo - 1]
        identidade = [[float(i == j) for j in range(dim)] for i in range(dim)]
        a_ent, a_pca, a_sup = acuracia(identidade), acuracia(pca), acuracia(supervisionada)
        retencao = lambda a: max(0.0, (a - 0.5) / max(1e-9, a_ent - 0.5))
        return dict(acuracia_entrada=a_ent, acuracia_pca=a_pca, acuracia_supervisionada=a_sup,
                    retencao_pca=retencao(a_pca), retencao_supervisionada=retencao(a_sup))


class ModelagemPorPotencial:
    """Ng, Harada e Russell (1999): somar F(s, s') = γΦ(s') − Φ(s) à recompensa NÃO muda a política ótima;
    somar um bônus qualquer (o 'diagnóstico' do reforço extraordinário) pode mudar. Medido por iteração de
    valor exata em MDPs aleatórios."""

    @staticmethod
    def mdp(n: int, a: int, seed: int) -> tuple[list, list]:
        rng = random.Random(seed)
        T = []
        for _ in range(n):
            linha = []
            for _ in range(a):
                w = [rng.random() for _ in range(n)]
                s = sum(w)
                linha.append([x / s for x in w])
            T.append(linha)
        R = [[[rng.uniform(-1, 1) for _ in range(n)] for _ in range(a)] for _ in range(n)]
        return T, R

    @staticmethod
    def politica_otima(T, R, gama: float = 0.9, tol: float = 1e-12) -> tuple[list[int], list[float]]:
        n, a = len(T), len(T[0])
        V = [0.0] * n
        while True:
            Q = [[sum(T[s][k][s2] * (R[s][k][s2] + gama * V[s2]) for s2 in range(n)) for k in range(a)] for s in range(n)]
            V2 = [max(q) for q in Q]
            if max(abs(x - y) for x, y in zip(V, V2)) < tol:
                return [max(range(a), key=lambda k: Q[s][k]) for s in range(n)], V2
            V = V2

    @staticmethod
    def comparar(sementes: int = 50, n: int = 6, a: int = 3, gama: float = 0.9) -> dict[str, float]:
        iguais_pot = iguais_bonus = 0
        for s in range(sementes):
            T, R = ModelagemPorPotencial.mdp(n, a, s)
            rng = random.Random(1000 + s)
            phi = [rng.uniform(-5, 5) for _ in range(n)]
            pi, V = ModelagemPorPotencial.politica_otima(T, R, gama)
            Rp = [[[R[x][k][y] + gama * phi[y] - phi[x] for y in range(n)] for k in range(a)] for x in range(n)]
            pi_p, Vp = ModelagemPorPotencial.politica_otima(T, Rp, gama)
            bonus = [[rng.uniform(0, 2) for _ in range(a)] for _ in range(n)]   # bônus por (estado, ação)
            Rb = [[[R[x][k][y] + bonus[x][k] for y in range(n)] for k in range(a)] for x in range(n)]
            pi_b, _ = ModelagemPorPotencial.politica_otima(T, Rb, gama)
            iguais_pot += pi_p == pi
            iguais_bonus += pi_b == pi
            # identidade de Ng et al.: V' = V − Φ
            assert max(abs(vp - (v - f)) for vp, v, f in zip(Vp, V, phi)) < 1e-8
        return dict(sementes=sementes, politica_preservada_potencial=iguais_pot / sementes,
                    politica_preservada_bonus=iguais_bonus / sementes)


def kl_beta(a1: float, b1: float, a2: float, b2: float) -> float:
    """KL( Beta(a1,b1) ‖ Beta(a2,b2) ) em forma fechada (nats), com a digama por série assintótica."""
    def digama(x: float) -> float:
        r = 0.0
        while x < 6:
            r -= 1 / x
            x += 1
        f = 1 / (x * x)
        return r + math.log(x) - 0.5 / x - f * (1 / 12 - f * (1 / 120 - f * (1 / 252 - f * (1 / 240 - f / 132))))
    lb = lambda a, b: math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    return (lb(a2, b2) - lb(a1, b1) + (a1 - a2) * digama(a1) + (b1 - b2) * digama(b1)
            + (a2 - a1 + b2 - b1) * digama(a1 + b1))
