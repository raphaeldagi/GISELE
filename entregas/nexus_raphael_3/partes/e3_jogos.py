

# =============================================================================
# EXTENSÃO 3.0 — JOGOS DE INFORMAÇÃO IMPERFEITA: KUHN E LEDUC, CFR E MCCFR,
# MELHOR RESPOSTA EXATA E PROGRAMAÇÃO LINEAR (SIMPLEX EM FRAÇÕES)
# =============================================================================
# A 2.2.0 tinha só o prêmio do Kuhn e uma estratégia fixa "sem alegação de equilíbrio".
# Aqui o equilíbrio é CALCULADO de três jeitos independentes (CFR, programação linear
# exata e melhor resposta), e a explorabilidade mede quanto uma estratégia cede.

class JogoKuhn:
    """Pôquer de Kuhn: cartas 0 < 1 < 2 (valete, dama, rei), ante 1, uma aposta de 1.
    Ações: "p" (passar/desistir) e "b" (apostar/pagar)."""
    nome = "kuhn"
    DISTRIBUICOES = tuple((a, b, -1) for a in range(3) for b in range(3) if a != b)

    @staticmethod
    def acoes(h: str) -> tuple[str, ...]:
        return ("p", "b")

    @staticmethod
    def jogador(h: str) -> int:
        return len(h) % 2

    @staticmethod
    def proximo(h: str, a: str) -> str:
        return h + a

    @staticmethod
    def terminal(h: str, c1: int, c2: int, _b: int = -1) -> float | None:
        ganha = 1.0 if c1 > c2 else -1.0
        if h == "pp":
            return ganha
        if h in ("bb", "pbb"):
            return 2 * ganha
        if h == "bp":
            return 1.0
        if h == "pbp":
            return -1.0
        return None

    @staticmethod
    def chave(h: str, c1: int, c2: int, _b: int = -1) -> tuple:
        return (c1 if len(h) % 2 == 0 else c2, h)


class JogoLeduc:
    """Pôquer Leduc (Southey et al., 2005): 6 cartas (2×valete, 2×dama, 2×rei), ante 1, carta pública
    entre as rodadas, apostas fixas 2 e 4, no máximo 2 aumentos por rodada, o jogador 1 abre as duas.
    Ações "c" (passar/pagar), "r" (apostar/aumentar), "f" (desistir diante de aposta). Pareia com a
    pública: ganha; senão a maior; iguais dividem. As 120 distribuições ordenadas são o acaso."""
    nome = "leduc"
    POSTOS = (0, 0, 1, 1, 2, 2)
    DISTRIBUICOES = tuple((a // 2, b // 2, c // 2) for a, b, c in itertools.permutations(range(6), 3))
    APOSTA = (2, 4)

    @staticmethod
    def _rodada(h: str) -> tuple[str, int]:
        return h.split("/")[-1], h.count("/")

    @staticmethod
    def acoes(h: str) -> tuple[str, ...]:
        s, _ = JogoLeduc._rodada(h)
        if s.endswith("r"):
            return ("f", "c", "r") if s.count("r") < 2 else ("f", "c")
        return ("c", "r")

    @staticmethod
    def jogador(h: str) -> int:
        return len(JogoLeduc._rodada(h)[0]) % 2

    @staticmethod
    def _acabou(s: str) -> bool:
        return s == "cc" or (len(s) >= 2 and s.endswith("rc"))

    @staticmethod
    def proximo(h: str, a: str) -> str:
        h2 = h + a
        s, r = JogoLeduc._rodada(h2)
        return h2 + "/" if r == 0 and JogoLeduc._acabou(s) else h2

    @staticmethod
    def contribuicoes(h: str) -> list[int]:
        pos = [1, 1]
        for r, s in enumerate(h.split("/")):
            devido = [0, 0]
            for i, a in enumerate(s):
                if a == "c":
                    devido[i % 2] = max(devido)
                elif a == "r":
                    devido[i % 2] = max(devido) + JogoLeduc.APOSTA[r]
            pos[0] += devido[0]
            pos[1] += devido[1]
        return pos

    @staticmethod
    def terminal(h: str, c1: int, c2: int, b: int) -> float | None:
        s, r = JogoLeduc._rodada(h)
        if s.endswith("f"):
            quem = (len(s) - 1) % 2
            pos = JogoLeduc.contribuicoes(h[:-1])
            return -float(pos[0]) if quem == 0 else float(pos[1])
        if r == 1 and JogoLeduc._acabou(s):
            pos = JogoLeduc.contribuicoes(h)
            f1 = 10 + c1 if c1 == b else c1
            f2 = 10 + c2 if c2 == b else c2
            return float(pos[1]) if f1 > f2 else (-float(pos[0]) if f2 > f1 else 0.0)
        return None

    @staticmethod
    def chave(h: str, c1: int, c2: int, b: int) -> tuple:
        j = JogoLeduc.jogador(h)
        return (c1 if j == 0 else c2, b if "/" in h else -1, h)


class LCGPortavel:
    """Gerador congruencial inteiro (portável entre linguagens): o uniforme x/2³¹ é exato."""
    def __init__(self, semente: int):
        self.x = semente

    def inteiro(self, n: int) -> int:
        self.x = (1103515245 * self.x + 12345) % 2147483648
        return (self.x >> 16) % n

    def uniforme(self) -> float:
        self.x = (1103515245 * self.x + 12345) % 2147483648
        return self.x / 2147483648.0


class CFR:
    """Minimização do arrependimento contrafactual (Zinkevich et al., 2007) para qualquer jogo
    com a interface acima: vanilla, com o acaso amostrado e com amostragem externa
    (Lanctot et al., 2009). `nos` conta as chamadas da recursão (a unidade de custo)."""

    def __init__(self, jogo):
        self.jogo = jogo
        self.arrependimento: dict[tuple, list[float]] = {}
        self.soma: dict[tuple, list[float]] = {}
        self.nos = 0

    def estrategia(self, k: tuple, n: int) -> list[float]:
        r = self.arrependimento.get(k)
        if r is None:
            return [1.0 / n] * n
        pos = [x if x > 0 else 0.0 for x in r]
        s = sum(pos)
        return [x / s for x in pos] if s > 0 else [1.0 / n] * n

    def _cfr(self, d: tuple, h: str, p1: float, p2: float) -> float:
        self.nos += 1
        g = self.jogo
        u = g.terminal(h, *d)
        if u is not None:
            return u
        j = g.jogador(h)
        acs = g.acoes(h)
        k = g.chave(h, *d)
        s = self.estrategia(k, len(acs))
        util = [0.0] * len(acs)
        no = 0.0
        for i, a in enumerate(acs):
            util[i] = (self._cfr(d, g.proximo(h, a), p1 * s[i], p2) if j == 0
                       else self._cfr(d, g.proximo(h, a), p1, p2 * s[i]))
            no += s[i] * util[i]
        sinal = 1.0 if j == 0 else -1.0
        adv, prop = (p2, p1) if j == 0 else (p1, p2)
        r = self.arrependimento.setdefault(k, [0.0] * len(acs))
        m = self.soma.setdefault(k, [0.0] * len(acs))
        for i in range(len(acs)):
            r[i] += adv * sinal * (util[i] - no)
            m[i] += prop * s[i]
        return no

    def _externo(self, d: tuple, h: str, viajante: int, rng: LCGPortavel) -> float:
        self.nos += 1
        g = self.jogo
        u = g.terminal(h, *d)
        if u is not None:
            return u if viajante == 0 else -u
        acs = g.acoes(h)
        k = g.chave(h, *d)
        s = self.estrategia(k, len(acs))
        if g.jogador(h) == viajante:
            util = [self._externo(d, g.proximo(h, a), viajante, rng) for a in acs]
            no = sum(x * y for x, y in zip(s, util))
            r = self.arrependimento.setdefault(k, [0.0] * len(acs))
            for i in range(len(acs)):
                r[i] += util[i] - no
            return no
        m = self.soma.setdefault(k, [0.0] * len(acs))
        for i in range(len(acs)):
            m[i] += s[i]
        x, acum, escolhida = rng.uniforme(), 0.0, acs[-1]
        for i, a in enumerate(acs):
            acum += s[i]
            if x < acum:
                escolhida = a
                break
        return self._externo(d, g.proximo(h, escolhida), viajante, rng)

    def vanilla(self, iteracoes: int) -> "CFR":
        for _ in range(iteracoes):
            for d in self.jogo.DISTRIBUICOES:
                self._cfr(d, "", 1.0, 1.0)
        return self

    def acaso_amostrado(self, iteracoes: int, semente: int) -> "CFR":
        rng = LCGPortavel(semente)
        n = len(self.jogo.DISTRIBUICOES)
        for _ in range(iteracoes):
            self._cfr(self.jogo.DISTRIBUICOES[rng.inteiro(n)], "", 1.0, 1.0)
        return self

    def amostragem_externa(self, iteracoes: int, semente: int) -> "CFR":
        rng = LCGPortavel(semente)
        n = len(self.jogo.DISTRIBUICOES)
        for _ in range(iteracoes):
            for viajante in (0, 1):
                self._externo(self.jogo.DISTRIBUICOES[rng.inteiro(n)], "", viajante, rng)
        return self

    def media(self) -> dict[tuple, list[float]]:
        out = {}
        for k, m in self.soma.items():
            s = sum(m)
            out[k] = [x / s for x in m] if s > 0 else [1.0 / len(m)] * len(m)
        return out


class AnaliseJogo:
    """Valor exato de um perfil e melhor resposta exata (conjunto por conjunto, do mais fundo ao mais raso)."""

    @staticmethod
    def _s(estr: dict, k: tuple, n: int) -> list[float]:
        return estr.get(k) or [1.0 / n] * n

    @staticmethod
    def valor(jogo, estr: dict) -> float:
        def v(d, h):
            u = jogo.terminal(h, *d)
            if u is not None:
                return u
            acs = jogo.acoes(h)
            s = AnaliseJogo._s(estr, jogo.chave(h, *d), len(acs))
            return sum(s[i] * v(d, jogo.proximo(h, a)) for i, a in enumerate(acs))
        return sum(v(d, "") for d in jogo.DISTRIBUICOES) / len(jogo.DISTRIBUICOES)

    @staticmethod
    def melhor_resposta(jogo, estr: dict, resp: int) -> float:
        entradas: dict[tuple, list] = {}

        def anda(d, h, alc):
            if jogo.terminal(h, *d) is not None:
                return
            acs = jogo.acoes(h)
            k = jogo.chave(h, *d)
            if jogo.jogador(h) == resp:
                entradas.setdefault(k, []).append((d, h, alc))
                for a in acs:
                    anda(d, jogo.proximo(h, a), alc)
            else:
                s = AnaliseJogo._s(estr, k, len(acs))
                for i, a in enumerate(acs):
                    if s[i] > 0:
                        anda(d, jogo.proximo(h, a), alc * s[i])
        for d in jogo.DISTRIBUICOES:
            anda(d, "", 1.0)
        escolha, memo = {}, {}
        sinal = 1.0 if resp == 0 else -1.0

        def v(d, h):
            chave_memo = (d, h)
            if chave_memo in memo:
                return memo[chave_memo]
            u = jogo.terminal(h, *d)
            if u is not None:
                return u
            acs = jogo.acoes(h)
            k = jogo.chave(h, *d)
            if jogo.jogador(h) == resp:
                x = v(d, jogo.proximo(h, escolha[k]))
            else:
                s = AnaliseJogo._s(estr, k, len(acs))
                x = sum(s[i] * v(d, jogo.proximo(h, a)) for i, a in enumerate(acs) if s[i] > 0)
            memo[chave_memo] = x
            return x
        for k in sorted(entradas, key=lambda k: -len(k[-1])):
            melhor, qual = None, None
            for a in jogo.acoes(k[-1]):
                tot = sum(alc * v(d, jogo.proximo(h, a)) for d, h, alc in entradas[k])
                if melhor is None or sinal * tot > sinal * melhor:
                    melhor, qual = tot, a
            escolha[k] = qual
        return sum(v(d, "") for d in jogo.DISTRIBUICOES) / len(jogo.DISTRIBUICOES)

    @staticmethod
    def explorabilidade(jogo, estr: dict) -> float:
        """Soma do que o perfil cede às duas melhores respostas; 0 só no equilíbrio de Nash."""
        return AnaliseJogo.melhor_resposta(jogo, estr, 0) - AnaliseJogo.melhor_resposta(jogo, estr, 1)

    @staticmethod
    def conjuntos(jogo) -> tuple[int, int]:
        vistos = (set(), set())

        def anda(d, h):
            if jogo.terminal(h, *d) is not None:
                return
            vistos[jogo.jogador(h)].add(jogo.chave(h, *d))
            for a in jogo.acoes(h):
                anda(d, jogo.proximo(h, a))
        for d in jogo.DISTRIBUICOES:
            anda(d, "")
        return len(vistos[0]), len(vistos[1])

    @staticmethod
    def estrategia_fixa_kuhn_2_2_0() -> dict[tuple, list[float]]:
        """A estratégia fixa de PokerKuhn.resultado_fixo (2.2.0) escrita como perfil: o 1 aposta com o rei
        e blefa com o valete 25%; o 2 paga só com o rei, e aposta (após passe) com o rei ou blefa 20% com o valete."""
        e = {}
        for c in range(3):
            aposta = 1.0 if c == 2 else (0.25 if c == 0 else 0.0)
            e[(c, "")] = [1 - aposta, aposta]
            e[(c, "pb")] = [0.0, 1.0] if c == 2 else [1.0, 0.0]
            e[(c, "b")] = [0.0, 1.0] if c == 2 else [1.0, 0.0]
            aposta2 = 1.0 if c == 2 else (0.20 if c == 0 else 0.0)
            e[(c, "p")] = [1 - aposta2, aposta2]
        return e


class Simplex:
    """Programação linear EXATA em frações (regra de Bland, sem ciclagem): max cᵀx, Ax ≤ b, x ≥ 0, b ≥ 0."""

    @staticmethod
    def maximizar(a: list[list], b: list, c: list) -> tuple[Any, list, list]:
        from fractions import Fraction as F
        m, n = len(a), len(c)
        t = [[F(x) for x in a[i]] + [F(int(i == j)) for j in range(m)] + [F(b[i])] for i in range(m)]
        z = [-F(x) for x in c] + [F(0)] * m + [F(0)]
        base = [n + i for i in range(m)]
        while True:
            entra = next((j for j in range(n + m) if z[j] < 0), None)
            if entra is None:
                break
            linhas = [(t[i][-1] / t[i][entra], base[i], i) for i in range(m) if t[i][entra] > 0]
            if not linhas:
                raise ValueError("Problema ilimitado")
            _, _, sai = min(linhas)
            piv = t[sai][entra]
            t[sai] = [x / piv for x in t[sai]]
            for i in range(m):
                if i != sai and t[i][entra] != 0:
                    f = t[i][entra]
                    t[i] = [x - f * y for x, y in zip(t[i], t[sai])]
            f = z[entra]
            z = [x - f * y for x, y in zip(z, t[sai])]
            base[sai] = entra
        x = [F(0)] * n
        for i, bi in enumerate(base):
            if bi < n:
                x[bi] = t[i][-1]
        dual = [z[n + i] for i in range(m)]
        return z[-1], x, dual

    @staticmethod
    def resolver_jogo(matriz: list[list]) -> dict[str, Any]:
        """Jogo de soma zero (linhas maximizam). Desloca a matriz para positiva, resolve o LP do jogador
        das colunas e lê as estratégias dos dois (primal e dual). Valor exato em frações."""
        from fractions import Fraction as F
        menor = min(min(l) for l in matriz)
        k = F(1) - F(menor) if menor <= 0 else F(0)
        a = [[F(x) + k for x in l] for l in matriz]
        m, n = len(a), len(a[0])
        opt, y, dual = Simplex.maximizar(a, [1] * m, [1] * n)
        valor = 1 / opt - k
        return dict(valor=valor, linhas=[d / opt for d in dual], colunas=[v / opt for v in y])

    @staticmethod
    def kuhn_forma_normal() -> list[list]:
        """A matriz 64 × 64 do Kuhn em estratégias puras (2⁶ por jogador), com valor esperado exato em frações."""
        from fractions import Fraction as F
        conj1 = [(c, h) for c in range(3) for h in ("", "pb")]
        conj2 = [(c, h) for c in range(3) for h in ("p", "b")]
        puras1 = list(itertools.product((0, 1), repeat=6))
        puras2 = list(itertools.product((0, 1), repeat=6))
        acao = JogoKuhn.acoes("")

        def jogar(e1, e2, d):
            h = ""
            while True:
                u = JogoKuhn.terminal(h, *d)
                if u is not None:
                    return F(int(u))
                j = JogoKuhn.jogador(h)
                k = JogoKuhn.chave(h, *d)
                escolha = e1[conj1.index(k)] if j == 0 else e2[conj2.index(k)]
                h += acao[escolha]
        return [[sum(jogar(e1, e2, d) for d in JogoKuhn.DISTRIBUICOES) / 6 for e2 in puras2] for e1 in puras1]


class VelhaAvancada:
    """Jogo da velha: poda alfa-beta, contagem por camadas (caminho independente do da 2.2.0) e um
    agente de Q-learning tabular treinado contra um adversário aleatório e avaliado em partidas novas."""

    @staticmethod
    def alfa_beta(t: str = "." * 9, j: str = "X", alfa: int = -2, beta: int = 2) -> int:
        v = vencedor_velha(t)
        if v:
            return 1 if v == j else -1
        if "." not in t:
            return 0
        outro = "O" if j == "X" else "X"
        melhor = -2
        for i, c in enumerate(t):
            if c == ".":
                x = -VelhaAvancada.alfa_beta(t[:i] + j + t[i + 1:], outro, -beta, -alfa)
                melhor = max(melhor, x)
                alfa = max(alfa, x)
                if alfa >= beta:
                    break
        return melhor

    @staticmethod
    def estados_por_camadas() -> int:
        camada, total = {"." * 9}, 1
        for k in range(9):
            j = "X" if k % 2 == 0 else "O"
            nova = set()
            for t in camada:
                if vencedor_velha(t) or "." not in t:
                    continue
                for i, c in enumerate(t):
                    if c == ".":
                        nova.add(t[:i] + j + t[i + 1:])
            total += len(nova)
            camada = nova
        return total

    @staticmethod
    def treinar_q(episodios: int, seed: int, alfa: float = 0.3, gama: float = 1.0,
                  epsilon: float = 0.2) -> dict[str, float]:
        """O agente joga de X contra O aleatório. Q[tabuleiro][casa]; recompensa só no fim (+1/0/−1)."""
        rng = random.Random(seed)
        q: dict[str, dict[int, float]] = collections.defaultdict(dict)

        def livres(t):
            return [i for i, c in enumerate(t) if c == "."]
        for _ in range(episodios):
            t = "." * 9
            while True:
                acs = livres(t)
                if rng.random() < epsilon:
                    a = rng.choice(acs)
                else:
                    a = max(acs, key=lambda i: q[t].get(i, 0.0))
                t2 = t[:a] + "X" + t[a + 1:]
                if vencedor_velha(t2) == "X" or "." not in t2:
                    r = 1.0 if vencedor_velha(t2) == "X" else 0.0
                    q[t][a] = q[t].get(a, 0.0) + alfa * (r - q[t].get(a, 0.0))
                    break
                o = rng.choice(livres(t2))
                t3 = t2[:o] + "O" + t2[o + 1:]
                if vencedor_velha(t3) == "O" or "." not in t3:
                    r = -1.0 if vencedor_velha(t3) == "O" else 0.0
                    q[t][a] = q[t].get(a, 0.0) + alfa * (r - q[t].get(a, 0.0))
                    break
                alvo = gama * max(q[t3].get(i, 0.0) for i in livres(t3))
                q[t][a] = q[t].get(a, 0.0) + alfa * (alvo - q[t].get(a, 0.0))
                t = t3
        return VelhaAvancada.avaliar(lambda t: max(livres(t), key=lambda i: q[t].get(i, 0.0)), 1000, seed + 1)

    @staticmethod
    def avaliar(politica, partidas: int, seed: int) -> dict[str, float]:
        """A política (de X) contra O aleatório em partidas novas: frações de vitória, empate e derrota."""
        rng = random.Random(seed)
        v = e = d = 0
        for _ in range(partidas):
            t = "." * 9
            while True:
                a = politica(t)
                t = t[:a] + "X" + t[a + 1:]
                if vencedor_velha(t) == "X":
                    v += 1
                    break
                if "." not in t:
                    e += 1
                    break
                livres = [i for i, c in enumerate(t) if c == "."]
                o = rng.choice(livres)
                t = t[:o] + "O" + t[o + 1:]
                if vencedor_velha(t) == "O":
                    d += 1
                    break
        return dict(vitorias=v / partidas, empates=e / partidas, derrotas=d / partidas)
