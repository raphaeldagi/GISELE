

# =============================================================================
# EXTENSÃO 3.0 — CALIBRAÇÃO (recalibrar probabilidades com dados reservados)
# =============================================================================

class Calibracao:
    @staticmethod
    def isotonica(probs: list[float], rotulos: list[int]) -> list[tuple[float, float]]:
        """Regressão isotônica pelo algoritmo PAV (pool adjacent violators). Devolve os degraus
        [(limite superior da probabilidade, frequência calibrada)], monotônicos."""
        pares = sorted(zip(probs, rotulos))
        blocos = []  # [soma_y, contagem, maior_p]
        for p, y in pares:
            blocos.append([float(y), 1, p])
            while len(blocos) > 1 and blocos[-2][0] / blocos[-2][1] > blocos[-1][0] / blocos[-1][1]:
                s, c, m = blocos.pop()
                blocos[-1][0] += s
                blocos[-1][1] += c
                blocos[-1][2] = m
        return [(m, s / c) for s, c, m in blocos]

    @staticmethod
    def aplicar_isotonica(degraus: list[tuple[float, float]], p: float) -> float:
        for limite, valor in degraus:
            if p <= limite:
                return valor
        return degraus[-1][1]

    @staticmethod
    def platt(probs: list[float], rotulos: list[int], iteracoes: int = 100) -> tuple[float, float]:
        """Escala de Platt: p' = σ(a·logit(p) + b), a e b por Newton na perda logarítmica."""
        z = [math.log(max(1e-12, p) / max(1e-12, 1 - p)) for p in probs]
        a, b = 1.0, 0.0
        for _ in range(iteracoes):
            ga = gb = haa = hab = hbb = 0.0
            for zi, y in zip(z, rotulos):
                q = RegressaoLogistica.sigmoide(a * zi + b)
                r = q - y
                w = q * (1 - q)
                ga += r * zi
                gb += r
                haa += w * zi * zi
                hab += w * zi
                hbb += w
            det = haa * hbb - hab * hab + 1e-12
            da = (hbb * ga - hab * gb) / det
            db = (haa * gb - hab * ga) / det
            a, b = a - da, b - db
            if abs(da) + abs(db) < 1e-12:
                break
        return a, b

    @staticmethod
    def diagrama(probs: list[float], rotulos: list[int], faixas: int = 10) -> list[dict[str, float]]:
        """Diagrama de confiabilidade: por faixa, a confiança média, a frequência observada, n e o IC de Wilson."""
        linhas = []
        for f in range(faixas):
            pares = [(p, y) for p, y in zip(probs, rotulos) if min(faixas - 1, int(p * faixas)) == f]
            if not pares:
                continue
            k = sum(y for _, y in pares)
            lo, hi = Estatistica.wilson(k, len(pares))
            linhas.append(dict(faixa=f, n=len(pares), confianca=statistics.fmean(p for p, _ in pares),
                               frequencia=k / len(pares), ic_lo=lo, ic_hi=hi))
        return linhas

    @staticmethod
    def experimento(seed: int = 7, n: int = 3000) -> dict[str, Any]:
        """Um previsor DESCALIBRADO de propósito (p' = p^0,5, superconfiante para baixo) recalibrado com
        metade dos dados e avaliado na outra metade: ECE antes e depois, para isotônica e Platt."""
        rng = random.Random(seed)
        verdade = [rng.random() for _ in range(n)]
        y = [int(rng.random() < p) for p in verdade]
        previsto = [math.sqrt(p) for p in verdade]
        meio = n // 2
        degraus = Calibracao.isotonica(previsto[:meio], y[:meio])
        a, b = Calibracao.platt(previsto[:meio], y[:meio])
        teste_p, teste_y = previsto[meio:], y[meio:]
        iso = [Calibracao.aplicar_isotonica(degraus, p) for p in teste_p]
        pl = [RegressaoLogistica.sigmoide(a * math.log(max(1e-12, p) / max(1e-12, 1 - p)) + b) for p in teste_p]
        return dict(ece_antes=AvaliadorProbabilistico.pontuar(teste_p, teste_y)["ece"],
                    ece_isotonica=AvaliadorProbabilistico.pontuar(iso, teste_y)["ece"],
                    ece_platt=AvaliadorProbabilistico.pontuar(pl, teste_y)["ece"],
                    brier_antes=AvaliadorProbabilistico.pontuar(teste_p, teste_y)["brier"],
                    brier_isotonica=AvaliadorProbabilistico.pontuar(iso, teste_y)["brier"],
                    platt=(a, b), rotulo="[MEDIDO]", dados="[SINTÉTICO]")


# =============================================================================
# EXTENSÃO 3.0 — BANDIDOS DE K BRAÇOS (ε-guloso, UCB1, Thompson) com arrependimento
# =============================================================================

class Bandidos:
    """Braços de Bernoulli. O arrependimento é calculado com as médias VERDADEIRAS (não com
    as amostras), então a comparação entre políticas não depende da sorte do avaliador."""

    @staticmethod
    def jogar(politica: str, medias: list[float], passos: int, seed: int, epsilon: float = 0.1) -> dict[str, float]:
        rng = random.Random(seed)
        k = len(medias)
        n = [0] * k
        s = [0.0] * k
        a_beta, b_beta = [1.0] * k, [1.0] * k
        melhor = max(medias)
        arrependimento = 0.0
        for t in range(1, passos + 1):
            if politica == "epsilon":
                if rng.random() < epsilon or 0 in n:
                    braco = rng.randrange(k)
                else:
                    braco = max(range(k), key=lambda i: s[i] / n[i])
            elif politica == "ucb1":
                if 0 in n:
                    braco = n.index(0)
                else:
                    braco = max(range(k), key=lambda i: s[i] / n[i] + math.sqrt(2 * math.log(t) / n[i]))
            elif politica == "thompson":
                braco = max(range(k), key=lambda i: rng.betavariate(a_beta[i], b_beta[i]))
            else:
                raise ValueError("Política desconhecida")
            r = int(rng.random() < medias[braco])
            n[braco] += 1
            s[braco] += r
            a_beta[braco] += r
            b_beta[braco] += 1 - r
            arrependimento += melhor - medias[braco]
        return dict(arrependimento=arrependimento, fracao_melhor=n[medias.index(melhor)] / passos)

    @staticmethod
    def comparar(medias: list[float] = (0.75, 0.55, 0.5), passos: int = 2000,
                 sementes: range = range(30)) -> dict[str, Any]:
        """As três políticas nas MESMAS sementes; teste t pareado do arrependimento e correção de Holm."""
        medias = list(medias)
        res = {p: [Bandidos.jogar(p, medias, passos, s)["arrependimento"] for s in sementes]
               for p in ("epsilon", "ucb1", "thompson")}
        pares = {"thompson-ucb1": Estatistica.t_pareado(res["thompson"], res["ucb1"]),
                 "thompson-epsilon": Estatistica.t_pareado(res["thompson"], res["epsilon"]),
                 "ucb1-epsilon": Estatistica.t_pareado(res["ucb1"], res["epsilon"])}
        holm = Estatistica.holm({k: v["p_bilateral"] for k, v in pares.items()})
        return dict(medias_arrependimento={k: statistics.fmean(v) for k, v in res.items()},
                    pares=pares, rejeita_holm=holm, sementes=len(sementes), rotulo="[MEDIDO]")

    @staticmethod
    def lai_robbins(medias: list[float]) -> float:
        """A constante de Lai–Robbins: arrependimento ≥ c·ln T assintoticamente, c = Σ Δᵢ/KL(μᵢ, μ*)."""
        melhor = max(medias)
        c = 0.0
        for m in medias:
            if m < melhor:
                kl = m * math.log(m / melhor) + (1 - m) * math.log((1 - m) / (1 - melhor))
                c += (melhor - m) / kl
        return c


# =============================================================================
# EXTENSÃO 3.0 — INFORMAÇÃO E TEXTO
# =============================================================================

class Informacao:
    @staticmethod
    def entropia(probs: list[float], base: float = 2.0) -> float:
        return -sum(p * math.log(p, base) for p in probs if p > 0)

    @staticmethod
    def kl(p: list[float], q: list[float], base: float = 2.0) -> float:
        if any(pi > 0 and qi == 0 for pi, qi in zip(p, q)):
            return math.inf
        return sum(pi * math.log(pi / qi, base) for pi, qi in zip(p, q) if pi > 0)

    @staticmethod
    def informacao_mutua(pares: list[tuple[Any, Any]]) -> float:
        """I(X; Y) empírica em bits a partir de pares observados."""
        n = len(pares)
        cxy = collections.Counter(pares)
        cx = collections.Counter(x for x, _ in pares)
        cy = collections.Counter(y for _, y in pares)
        return sum(c / n * math.log2((c / n) / ((cx[x] / n) * (cy[y] / n))) for (x, y), c in cxy.items())

    @staticmethod
    def levenshtein(a: str, b: str) -> int:
        anterior = list(range(len(b) + 1))
        for i, ca in enumerate(a, 1):
            atual = [i]
            for j, cb in enumerate(b, 1):
                atual.append(min(anterior[j] + 1, atual[j - 1] + 1, anterior[j - 1] + (ca != cb)))
            anterior = atual
        return anterior[-1]

    @staticmethod
    def jaccard(a: set, b: set) -> float:
        return len(a & b) / len(a | b) if a | b else 1.0


class ModeloCaracteres:
    """Modelo de n-gramas de caracteres com suavização de Witten–Bell (interpolada até o unigrama
    e a uniforme). Mede bits por caractere num texto reservado."""

    def __init__(self, ordem: int = 3):
        if ordem < 1:
            raise ValueError("Ordem mínima 1")
        self.ordem = ordem
        self.contagens: list[dict[str, collections.Counter]] = [collections.defaultdict(collections.Counter)
                                                                 for _ in range(ordem)]
        self.alfabeto: set[str] = set()

    def treinar(self, texto: str) -> "ModeloCaracteres":
        texto = "\x02" * (self.ordem - 1) + texto
        self.alfabeto |= set(texto)
        for i in range(self.ordem - 1, len(texto)):
            for k in range(self.ordem):
                contexto = texto[i - k:i]
                self.contagens[k][contexto][texto[i]] += 1
        return self

    def prob(self, contexto: str, c: str) -> float:
        p = 1.0 / max(1, len(self.alfabeto) + 1)
        for k in range(self.ordem):
            ctx = contexto[len(contexto) - k:] if k else ""
            tabela = self.contagens[k].get(ctx)
            if not tabela:
                continue
            total = sum(tabela.values())
            tipos = len(tabela)
            lam = total / (total + tipos)
            p = lam * tabela.get(c, 0) / total + (1 - lam) * p
        return p

    def bits_por_caractere(self, texto: str) -> float:
        texto = "\x02" * (self.ordem - 1) + texto
        bits = 0.0
        n = 0
        for i in range(self.ordem - 1, len(texto)):
            bits -= math.log2(self.prob(texto[i - self.ordem + 1:i], texto[i]))
            n += 1
        return bits / max(1, n)

    def gerar(self, n: int, seed: int) -> str:
        rng = random.Random(seed)
        contexto = "\x02" * (self.ordem - 1)
        saida = []
        letras = sorted(self.alfabeto - {"\x02"})
        for _ in range(n):
            pesos = [self.prob(contexto, c) for c in letras]
            c = rng.choices(letras, weights=pesos)[0]
            saida.append(c)
            contexto = (contexto + c)[-(self.ordem - 1):] if self.ordem > 1 else ""
        return "".join(saida)


# =============================================================================
# EXTENSÃO 3.0 — DINÂMICA NÃO LINEAR
# =============================================================================

class Dinamica:
    @staticmethod
    def rk4(f, estado: list[float], dt: float, passos: int) -> list[list[float]]:
        """Runge–Kutta de 4ª ordem para d estado/dt = f(estado)."""
        trajetoria = [list(estado)]
        x = list(estado)
        for _ in range(passos):
            k1 = f(x)
            k2 = f([a + dt / 2 * b for a, b in zip(x, k1)])
            k3 = f([a + dt / 2 * b for a, b in zip(x, k2)])
            k4 = f([a + dt * b for a, b in zip(x, k3)])
            x = [a + dt / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(x, k1, k2, k3, k4)]
            trajetoria.append(x)
        return trajetoria

    @staticmethod
    def lorenz(sigma: float = 10.0, rho: float = 28.0, beta: float = 8 / 3):
        return lambda v: [sigma * (v[1] - v[0]), v[0] * (rho - v[2]) - v[1], v[0] * v[1] - beta * v[2]]

    @staticmethod
    def lyapunov_benettin(f, estado: list[float], dt: float = 0.01, passos: int = 20_000,
                          d0: float = 1e-8, descarte: int = 1000) -> float:
        """Maior expoente de Lyapunov por duas trajetórias vizinhas renormalizadas a cada passo (Benettin)."""
        x = list(estado)
        for _ in range(descarte):
            x = Dinamica.rk4(f, x, dt, 1)[-1]
        y = [x[0] + d0] + x[1:]
        soma = 0.0
        for _ in range(passos):
            x = Dinamica.rk4(f, x, dt, 1)[-1]
            y = Dinamica.rk4(f, y, dt, 1)[-1]
            d = math.sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))
            soma += math.log(d / d0)
            y = [a + d0 * (b - a) / d for a, b in zip(x, y)]
        return soma / (passos * dt)

    @staticmethod
    def periodo_logistico(r: float, transiente: int = 5000, maximo: int = 64, tol: float = 1e-9) -> int | None:
        """O período da órbita atratora do mapa logístico (None se não periódica até `maximo`)."""
        x = 0.4
        for _ in range(transiente):
            x = r * x * (1 - x)
        orbita = [x]
        for _ in range(maximo):
            x = r * x * (1 - x)
            orbita.append(x)
        for p in range(1, maximo + 1):
            if all(abs(orbita[i] - orbita[i + p]) < tol for i in range(maximo + 1 - p)):
                return p
        return None

    @staticmethod
    def feigenbaum(r_inicial: float = 2.9, r_final: float = 3.57, passos: int = 3000) -> list[float]:
        """Os valores de r em que o período dobra (1→2→4→8...), por varredura; as razões entre os
        intervalos sucessivos convergem para δ = 4,669..."""
        dobras = []
        ultimo = Dinamica.periodo_logistico(r_inicial)
        for i in range(1, passos + 1):
            r = r_inicial + (r_final - r_inicial) * i / passos
            p = Dinamica.periodo_logistico(r)
            if p is not None and ultimo is not None and p == 2 * ultimo:
                dobras.append(r)
            if p is not None:
                ultimo = p
        return dobras
