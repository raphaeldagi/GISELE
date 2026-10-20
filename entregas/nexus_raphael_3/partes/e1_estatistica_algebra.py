

# =============================================================================
# EXTENSÃO 3.0 — ESTATÍSTICA EXATA (biblioteca padrão, sem scipy)
# =============================================================================
# Cada função aqui tem um teste em TestesExtensao contra um valor conhecido
# (forma fechada, tabela clássica ou outra função independente).

class Estatistica:
    """Distribuições e testes com funções especiais calculadas por série e fração
    contínua (Numerical Recipes, cap. 6), sem dependências externas."""

    # ---------------- funções especiais ----------------
    @staticmethod
    def gama_inferior_regularizada(a: float, x: float) -> float:
        """P(a, x) = γ(a, x)/Γ(a). Série para x < a+1, fração contínua (Lentz) caso contrário."""
        if a <= 0:
            raise ValueError("a deve ser positivo")
        if x <= 0:
            return 0.0
        if x < a + 1:
            termo = 1.0 / a
            soma = termo
            n = a
            for _ in range(10_000):
                n += 1
                termo *= x / n
                soma += termo
                if abs(termo) < abs(soma) * 1e-16:
                    break
            return soma * math.exp(-x + a * math.log(x) - math.lgamma(a))
        return 1.0 - Estatistica._gama_superior_fc(a, x)

    @staticmethod
    def _gama_superior_fc(a: float, x: float) -> float:
        minusculo = 1e-300
        b = x + 1 - a
        c = 1 / minusculo
        d = 1 / b
        h = d
        for i in range(1, 10_000):
            an = -i * (i - a)
            b += 2
            d = an * d + b
            if abs(d) < minusculo:
                d = minusculo
            c = b + an / c
            if abs(c) < minusculo:
                c = minusculo
            d = 1 / d
            delta = d * c
            h *= delta
            if abs(delta - 1) < 1e-16:
                break
        return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h

    @staticmethod
    def beta_regularizada(x: float, a: float, b: float) -> float:
        """I_x(a, b) pela fração contínua de Lentz, com a simetria I_x(a,b) = 1 − I_{1−x}(b,a)."""
        if not 0 <= x <= 1:
            raise ValueError("x fora de [0, 1]")
        if x in (0.0, 1.0):
            return x
        ln_frente = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                     + a * math.log(x) + b * math.log(1 - x))
        if x < (a + 1) / (a + b + 2):
            return math.exp(ln_frente) * Estatistica._beta_fc(x, a, b) / a
        return 1 - math.exp(ln_frente) * Estatistica._beta_fc(1 - x, b, a) / b

    @staticmethod
    def _beta_fc(x: float, a: float, b: float) -> float:
        minusculo = 1e-300
        qab, qap, qam = a + b, a + 1, a - 1
        c, d = 1.0, 1 - qab * x / qap
        d = 1 / (d if abs(d) > minusculo else minusculo)
        h = d
        for m in range(1, 10_000):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1 + aa * d
            d = 1 / (d if abs(d) > minusculo else minusculo)
            c = 1 + aa / c
            c = c if abs(c) > minusculo else minusculo
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1 + aa * d
            d = 1 / (d if abs(d) > minusculo else minusculo)
            c = 1 + aa / c
            c = c if abs(c) > minusculo else minusculo
            delta = d * c
            h *= delta
            if abs(delta - 1) < 1e-16:
                break
        return h

    @staticmethod
    def _inverter(f, alvo: float, lo: float, hi: float, iteracoes: int = 200) -> float:
        """Bisseção para f crescente: o x em [lo, hi] com f(x) = alvo."""
        for _ in range(iteracoes):
            meio = (lo + hi) / 2
            if f(meio) < alvo:
                lo = meio
            else:
                hi = meio
        return (lo + hi) / 2

    # ---------------- distribuições ----------------
    @staticmethod
    def qui2_cdf(x: float, gl: float) -> float:
        return Estatistica.gama_inferior_regularizada(gl / 2, x / 2) if x > 0 else 0.0

    @staticmethod
    def qui2_sf(x: float, gl: float) -> float:
        return 1.0 - Estatistica.qui2_cdf(x, gl)

    @staticmethod
    def t_cdf(t: float, gl: float) -> float:
        """F(t) da t de Student: 1 − ½ I_{gl/(gl+t²)}(gl/2, ½) para t ≥ 0."""
        x = gl / (gl + t * t)
        cauda = 0.5 * Estatistica.beta_regularizada(x, gl / 2, 0.5)
        return 1 - cauda if t >= 0 else cauda

    @staticmethod
    def t_quantil(p: float, gl: float) -> float:
        if not 0 < p < 1:
            raise ValueError("p fora de (0, 1)")
        if p < 0.5:
            return -Estatistica.t_quantil(1 - p, gl)
        return Estatistica._inverter(lambda t: Estatistica.t_cdf(t, gl), p, 0.0, 1e4)

    @staticmethod
    def beta_quantil(p: float, a: float, b: float) -> float:
        return Estatistica._inverter(lambda x: Estatistica.beta_regularizada(x, a, b), p, 0.0, 1.0)

    @staticmethod
    def normal_cdf(z: float) -> float:
        return 0.5 * math.erfc(-z / math.sqrt(2))

    @staticmethod
    def normal_quantil(p: float) -> float:
        return statistics.NormalDist().inv_cdf(p)

    # ---------------- intervalos ----------------
    @staticmethod
    def wilson(sucessos: int, n: int, confianca: float = 0.95) -> tuple[float, float]:
        if n <= 0:
            raise ValueError("n deve ser positivo")
        z = Estatistica.normal_quantil(0.5 + confianca / 2)
        p = sucessos / n
        centro = (p + z * z / (2 * n)) / (1 + z * z / n)
        meia = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        return max(0.0, centro - meia), min(1.0, centro + meia)

    @staticmethod
    def clopper_pearson(sucessos: int, n: int, confianca: float = 0.95) -> tuple[float, float]:
        """Intervalo binomial EXATO pelos quantis da Beta."""
        a = (1 - confianca) / 2
        lo = 0.0 if sucessos == 0 else Estatistica.beta_quantil(a, sucessos, n - sucessos + 1)
        hi = 1.0 if sucessos == n else Estatistica.beta_quantil(1 - a, sucessos + 1, n - sucessos)
        return lo, hi

    @staticmethod
    def beta_credivel(a: float, b: float, nivel: float = 0.95) -> tuple[float, float]:
        """Intervalo de credibilidade EXATO da posterior Beta(a, b) (corrige a aproximação normal da 2.2.0)."""
        cauda = (1 - nivel) / 2
        return Estatistica.beta_quantil(cauda, a, b), Estatistica.beta_quantil(1 - cauda, a, b)

    @staticmethod
    def media_ic_t(dados: list[float], confianca: float = 0.95) -> tuple[float, float, float]:
        n = len(dados)
        if n < 2:
            raise ValueError("São necessários ao menos 2 dados")
        media = statistics.fmean(dados)
        s = statistics.stdev(dados)
        m = Estatistica.t_quantil(0.5 + confianca / 2, n - 1) * s / math.sqrt(n)
        return media, media - m, media + m

    @staticmethod
    def quantil(valores: list[float], p: float) -> float:
        """Quantil por interpolação linear (tipo 7), para qualquer número de valores."""
        v = sorted(valores)
        if not v:
            raise ValueError("Lista vazia")
        h = (len(v) - 1) * p
        i = math.floor(h)
        j = min(i + 1, len(v) - 1)
        return v[i] + (h - i) * (v[j] - v[i])

    @staticmethod
    def bootstrap_media(dados: list[float], seed: int, repeticoes: int = 1000,
                        confianca: float = 0.95) -> tuple[float, float, float]:
        """IC percentil da média com os quantis calculados do NÚMERO de réplicas (corrige os índices
        fixos [24]/[974] da 2.2.0, que quebravam com outro número de réplicas)."""
        if not dados:
            raise ValueError("Lista vazia")
        rng = random.Random(seed)
        n = len(dados)
        replicas = [statistics.fmean(dados[rng.randrange(n)] for _ in range(n)) for _ in range(repeticoes)]
        a = (1 - confianca) / 2
        return statistics.fmean(dados), Estatistica.quantil(replicas, a), Estatistica.quantil(replicas, 1 - a)

    # ---------------- testes ----------------
    @staticmethod
    def t_pareado(a: list[float], b: list[float]) -> dict[str, float]:
        if len(a) != len(b) or len(a) < 2:
            raise ValueError("Amostras pareadas incompatíveis")
        d = [x - y for x, y in zip(a, b)]
        n = len(d)
        s = statistics.stdev(d)
        media = statistics.fmean(d)
        if s == 0:
            return dict(t=math.inf if media else 0.0, gl=n - 1, p_bilateral=0.0 if media else 1.0, media=media)
        t = media / (s / math.sqrt(n))
        return dict(t=t, gl=n - 1, p_bilateral=2 * (1 - Estatistica.t_cdf(abs(t), n - 1)), media=media)

    @staticmethod
    def binomial_exato(sucessos: int, n: int, p: float = 0.5) -> float:
        """P-valor bilateral exato: soma das probabilidades ≤ a do observado."""
        probs = [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
        obs = probs[sucessos]
        return min(1.0, sum(x for x in probs if x <= obs * (1 + 1e-12)))

    @staticmethod
    def sinal(diferencas: list[float]) -> dict[str, float]:
        pos = sum(d > 0 for d in diferencas)
        neg = sum(d < 0 for d in diferencas)
        n = pos + neg
        return dict(positivos=pos, negativos=neg, empates=len(diferencas) - n,
                    p_bilateral=Estatistica.binomial_exato(pos, n) if n else 1.0)

    @staticmethod
    def permutacao_pareada(a: list[float], b: list[float], seed: int, repeticoes: int = 5000) -> float:
        """P-valor bilateral por troca aleatória de sinal das diferenças pareadas."""
        d = [x - y for x, y in zip(a, b)]
        obs = abs(statistics.fmean(d))
        rng = random.Random(seed)
        extremos = 0
        for _ in range(repeticoes):
            m = abs(statistics.fmean(x if rng.random() < 0.5 else -x for x in d))
            extremos += m >= obs - 1e-15
        return (extremos + 1) / (repeticoes + 1)

    @staticmethod
    def holm(p_valores: dict[str, float], alfa: float = 0.05) -> dict[str, bool]:
        """Correção de Holm–Bonferroni para várias hipóteses: devolve quem é rejeitada."""
        ordem = sorted(p_valores.items(), key=lambda kv: kv[1])
        m = len(ordem)
        rejeita, parou = {}, False
        for i, (nome, p) in enumerate(ordem):
            if not parou and p <= alfa / (m - i):
                rejeita[nome] = True
            else:
                parou = True
                rejeita[nome] = False
        return rejeita

    @staticmethod
    def qui2_uniformidade(contagens: list[int], fator: float = 1.0) -> dict[str, float]:
        """Qui-quadrado de aderência à uniforme. `fator` corrige a escala quando as categorias não são
        multinomiais (Mega-Sena: 6 dezenas DISTINTAS por sorteio; ver MegaSenaCorrigida)."""
        n = sum(contagens)
        k = len(contagens)
        e = n / k
        x = sum((c - e) ** 2 / e for c in contagens)
        return dict(estatistica=x, gl=k - 1, fator=fator, p_valor=Estatistica.qui2_sf(x / fator, k - 1))


# =============================================================================
# EXTENSÃO 3.0 — ÁLGEBRA LINEAR (listas de listas, sem numpy)
# =============================================================================

class AlgebraLinear:
    @staticmethod
    def identidade(n: int) -> list[list[float]]:
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    @staticmethod
    def transposta(a: list[list[float]]) -> list[list[float]]:
        return [list(c) for c in zip(*a)]

    @staticmethod
    def produto(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
        if len(a[0]) != len(b):
            raise ValueError("Dimensões incompatíveis")
        bt = AlgebraLinear.transposta(b)
        return [[sum(x * y for x, y in zip(linha, coluna)) for coluna in bt] for linha in a]

    @staticmethod
    def aplicar(a: list[list[float]], v: list[float]) -> list[float]:
        return [sum(x * y for x, y in zip(linha, v)) for linha in a]

    @staticmethod
    def eliminacao(a: list[list[float]]) -> tuple[list[list[float]], list[int], int]:
        """LU com pivô parcial (Doolittle, no lugar). Devolve (LU, permutação, sinal)."""
        n = len(a)
        m = [list(map(float, linha)) for linha in a]
        perm = list(range(n))
        sinal = 1
        for c in range(n):
            p = max(range(c, n), key=lambda r: abs(m[r][c]))
            if abs(m[p][c]) < 1e-300:
                raise ValueError("Matriz singular")
            if p != c:
                m[c], m[p] = m[p], m[c]
                perm[c], perm[p] = perm[p], perm[c]
                sinal = -sinal
            for r in range(c + 1, n):
                f = m[r][c] / m[c][c]
                m[r][c] = f
                for k in range(c + 1, n):
                    m[r][k] -= f * m[c][k]
        return m, perm, sinal

    @staticmethod
    def determinante(a: list[list[float]]) -> float:
        try:
            lu, _, sinal = AlgebraLinear.eliminacao(a)
        except ValueError:
            return 0.0
        d = float(sinal)
        for i in range(len(a)):
            d *= lu[i][i]
        return d

    @staticmethod
    def resolver(a: list[list[float]], b: list[float]) -> list[float]:
        lu, perm, _ = AlgebraLinear.eliminacao(a)
        n = len(a)
        y = [0.0] * n
        for i in range(n):
            y[i] = b[perm[i]] - sum(lu[i][k] * y[k] for k in range(i))
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(lu[i][k] * x[k] for k in range(i + 1, n))) / lu[i][i]
        return x

    @staticmethod
    def inversa(a: list[list[float]]) -> list[list[float]]:
        n = len(a)
        colunas = [AlgebraLinear.resolver(a, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
        return AlgebraLinear.transposta(colunas)

    @staticmethod
    def minimos_quadrados(x: list[list[float]], y: list[float], cumeeira: float = 0.0) -> list[float]:
        """β = (XᵀX + λI)⁻¹ Xᵀy pelas equações normais (λ = 0: mínimos quadrados ordinários)."""
        xt = AlgebraLinear.transposta(x)
        xtx = AlgebraLinear.produto(xt, x)
        for i in range(len(xtx)):
            xtx[i][i] += cumeeira
        return AlgebraLinear.resolver(xtx, AlgebraLinear.aplicar(xt, y))

    @staticmethod
    def gram_schmidt(a: list[list[float]]) -> tuple[list[list[float]], list[list[float]]]:
        """QR por Gram–Schmidt modificado (colunas de a). Devolve (Q, R)."""
        n, m = len(a), len(a[0])
        colunas = [[a[i][j] for i in range(n)] for j in range(m)]
        q, r = [], [[0.0] * m for _ in range(m)]
        for j, v in enumerate(colunas):
            v = list(v)
            for i, u in enumerate(q):
                r[i][j] = sum(x * y for x, y in zip(u, v))
                v = [x - r[i][j] * y for x, y in zip(v, u)]
            r[j][j] = math.sqrt(sum(x * x for x in v))
            if r[j][j] < 1e-300:
                raise ValueError("Colunas linearmente dependentes")
            q.append([x / r[j][j] for x in v])
        return AlgebraLinear.transposta(q), r

    @staticmethod
    def jacobi(s: list[list[float]], varreduras: int = 100) -> tuple[list[float], list[list[float]]]:
        """Autovalores e autovetores de uma matriz simétrica (Jacobi cíclico). Devolve (valores, vetores em colunas)."""
        n = len(s)
        a = [list(map(float, l)) for l in s]
        v = AlgebraLinear.identidade(n)
        for _ in range(varreduras):
            fora = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
            if fora < 1e-30:
                break
            for p in range(n - 1):
                for q in range(p + 1, n):
                    if abs(a[p][q]) < 1e-300:
                        continue
                    th = (a[q][q] - a[p][p]) / (2 * a[p][q])
                    t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1))
                    c = 1 / math.sqrt(t * t + 1)
                    sn = t * c
                    for k in range(n):
                        akp, akq = a[k][p], a[k][q]
                        a[k][p], a[k][q] = c * akp - sn * akq, sn * akp + c * akq
                    for k in range(n):
                        apk, aqk = a[p][k], a[q][k]
                        a[p][k], a[q][k] = c * apk - sn * aqk, sn * apk + c * aqk
                    for k in range(n):
                        vkp, vkq = v[k][p], v[k][q]
                        v[k][p], v[k][q] = c * vkp - sn * vkq, sn * vkp + c * vkq
        return [a[i][i] for i in range(n)], v

    @staticmethod
    def valores_singulares(a: list[list[float]]) -> list[float]:
        valores, _ = AlgebraLinear.jacobi(AlgebraLinear.produto(AlgebraLinear.transposta(a), a))
        return sorted((math.sqrt(max(x, 0.0)) for x in valores), reverse=True)

    @staticmethod
    def potencia(a: list[list[float]], iteracoes: int = 1000, seed: int = 0) -> tuple[float, list[float]]:
        """Maior autovalor em módulo pela iteração de potência (com o quociente de Rayleigh)."""
        rng = random.Random(seed)
        v = [rng.gauss(0, 1) for _ in range(len(a))]
        for _ in range(iteracoes):
            w = AlgebraLinear.aplicar(a, v)
            nw = math.sqrt(sum(x * x for x in w))
            if nw == 0:
                return 0.0, v
            v = [x / nw for x in w]
        av = AlgebraLinear.aplicar(a, v)
        return sum(x * y for x, y in zip(v, av)), v

    @staticmethod
    def componentes_principais(dados: list[list[float]], k: int) -> dict[str, Any]:
        """PCA pela covariância (Jacobi): as k direções, as variâncias e a fração explicada."""
        n, d = len(dados), len(dados[0])
        medias = [statistics.fmean(l[j] for l in dados) for j in range(d)]
        centrados = [[l[j] - medias[j] for j in range(d)] for l in dados]
        cov = [[sum(c[i] * c[j] for c in centrados) / (n - 1) for j in range(d)] for i in range(d)]
        valores, vetores = AlgebraLinear.jacobi(cov)
        ordem = sorted(range(d), key=lambda i: -valores[i])
        total = sum(valores)
        return dict(variancias=[valores[i] for i in ordem[:k]],
                    fracao_explicada=sum(valores[i] for i in ordem[:k]) / total if total else 0.0,
                    direcoes=[[vetores[r][i] for r in range(d)] for i in ordem[:k]], medias=medias)
