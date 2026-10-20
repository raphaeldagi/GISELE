

# =============================================================================
# SYNTHAI-GPT — O MOTOR: TRANSFORMER DECODIFICADOR (FORMA DE GPT) EM PYTHON PURO
# =============================================================================
# Arquitetura (a mesma família do GPT-2, em miniatura):
#   h₀ = E[x_t] + P[t]
#   para cada camada:  h ← h + Atenção(LN₁(h))       (atenção causal com H cabeças)
#                      h ← h + MLP(LN₂(h))           (d → 4d → d, GELU)
#   logits = LN_f(h) · U + c        p(x_{t+1} | x_≤t) = softmax(logits)
# A perda é a entropia cruzada média. O gradiente é escrito à mão (sem autograd e sem numpy) e
# conferido por diferenças finitas nos testes (TestesGPT.test_gradiente_por_diferencas_finitas).

import gzip
from operator import mul as _mul

VERSAO_GPT = "1.0.0"
_C_GELU = math.sqrt(2.0 / math.pi)


def _transposta(a: list[list[float]]) -> list[list[float]]:
    return [list(c) for c in zip(*a)]


def _mm(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """A (n×k) · B (k×m)."""
    bt = _transposta(b)
    return [[sum(map(_mul, linha, col)) for col in bt] for linha in a]


def _mm_bt(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """A (n×k) · Bᵀ, com B (m×k)."""
    return [[sum(map(_mul, linha, outra)) for outra in b] for linha in a]


def _at_b(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Aᵀ (k×n) · B (n×m): o gradiente de um peso."""
    return _mm(_transposta(a), b)


def _soma_linhas(a: list[list[float]]) -> list[float]:
    return [sum(c) for c in zip(*a)]


def _somar_em(alvo: list[list[float]], g: list[list[float]]) -> None:
    for la, lg in zip(alvo, g):
        for j, v in enumerate(lg):
            la[j] += v


def _softmax(v: list[float]) -> list[float]:
    m = max(v)
    e = [math.exp(x - m) for x in v]
    s = sum(e)
    return [x / s for x in e]


@dataclass
class ConfigGPT:
    vocab: int
    contexto: int = 32       # T: janela de atenção
    d: int = 32              # largura do fluxo residual
    camadas: int = 2
    cabecas: int = 4
    semente: int = 2026

    def __post_init__(self) -> None:
        if self.d % self.cabecas:
            raise ValueError("d precisa ser múltiplo do número de cabeças")
        if min(self.vocab, self.contexto, self.d, self.camadas, self.cabecas) < 1:
            raise ValueError("Configuração inválida")

    def parametros(self) -> int:
        d, v, t, c = self.d, self.vocab, self.contexto, self.camadas
        por_camada = 4 * d * d + 4 * d + 2 * (4 * d * d) + 4 * d + d + 4 * d
        return v * d + t * d + c * por_camada + 2 * d + d * v + v


class ModeloGPT:
    """Os pesos, a ida (com o que a volta precisa) e a volta. Matrizes são listas de linhas."""

    def __init__(self, cfg: ConfigGPT):
        self.cfg = cfg
        r = random.Random(cfg.semente)
        d, v = cfg.d, cfg.vocab

        def g(n: int, m: int, s: float) -> list[list[float]]:
            return [[r.gauss(0.0, s) for _ in range(m)] for _ in range(n)]

        def z(n: int, m: int) -> list[list[float]]:
            return [[0.0] * m for _ in range(n)]

        def u(n: int, m: int) -> list[list[float]]:
            return [[1.0] * m for _ in range(n)]
        s = 0.02
        sr = 0.02 / math.sqrt(2 * cfg.camadas)   # resíduos escalados, como no GPT-2
        p: dict[str, list[list[float]]] = {"E": g(v, d, s), "P": g(cfg.contexto, d, s),
                                           "gf": u(1, d), "bf": z(1, d), "U": g(d, v, s), "c": z(1, v)}
        for l in range(cfg.camadas):
            p.update({f"{l}.g1": u(1, d), f"{l}.b1": z(1, d),
                      f"{l}.Wq": g(d, d, s), f"{l}.Wk": g(d, d, s), f"{l}.Wv": g(d, d, s),
                      f"{l}.bq": z(1, d), f"{l}.bk": z(1, d), f"{l}.bv": z(1, d),
                      f"{l}.Wo": g(d, d, sr), f"{l}.bo": z(1, d),
                      f"{l}.g2": u(1, d), f"{l}.b2": z(1, d),
                      f"{l}.W1": g(d, 4 * d, s), f"{l}.c1": z(1, 4 * d),
                      f"{l}.W2": g(4 * d, d, sr), f"{l}.c2": z(1, d)})
        self.p = p

    def contar(self) -> int:
        return sum(len(m) * len(m[0]) for m in self.p.values())

    # ------------------------------------------------------------- blocos
    @staticmethod
    def _ln(x: list[list[float]], g: list[float], b: list[float]):
        saida, cache = [], []
        for linha in x:
            n = len(linha)
            mu = sum(linha) / n
            var = sum((a - mu) * (a - mu) for a in linha) / n
            rs = 1.0 / math.sqrt(var + 1e-5)
            xh = [(a - mu) * rs for a in linha]
            saida.append([gi * a + bi for gi, a, bi in zip(g, xh, b)])
            cache.append((xh, rs))
        return saida, cache

    @staticmethod
    def _ln_volta(dy: list[list[float]], cache, g: list[float], dg: list[float], db: list[float]):
        dx = []
        for dl, (xh, rs) in zip(dy, cache):
            n = len(dl)
            for j in range(n):
                dg[j] += dl[j] * xh[j]
                db[j] += dl[j]
            dxh = [a * gi for a, gi in zip(dl, g)]
            m1 = sum(dxh) / n
            m2 = sum(a * b for a, b in zip(dxh, xh)) / n
            dx.append([rs * (a - m1 - b * m2) for a, b in zip(dxh, xh)])
        return dx

    @staticmethod
    def _mais_vies(x: list[list[float]], b: list[float]) -> list[list[float]]:
        return [[a + c for a, c in zip(linha, b)] for linha in x]

    def adiante(self, x: list[int], guardar: bool = True):
        cfg, p = self.cfg, self.p
        n, d, H = len(x), cfg.d, cfg.cabecas
        hd = d // H
        esc = 1.0 / math.sqrt(hd)
        if n > cfg.contexto:
            raise ValueError("Sequência maior que o contexto")
        h = [[a + b for a, b in zip(p["E"][t], p["P"][i])] for i, t in enumerate(x)]
        caches = []
        for l in range(cfg.camadas):
            a, c1 = self._ln(h, p[f"{l}.g1"][0], p[f"{l}.b1"][0])
            q = self._mais_vies(_mm(a, p[f"{l}.Wq"]), p[f"{l}.bq"][0])
            k = self._mais_vies(_mm(a, p[f"{l}.Wk"]), p[f"{l}.bk"][0])
            v = self._mais_vies(_mm(a, p[f"{l}.Wv"]), p[f"{l}.bv"][0])
            o = [[0.0] * d for _ in range(n)]
            atencoes = []
            for c in range(H):
                fatia = slice(c * hd, (c + 1) * hd)
                qh = [linha[fatia] for linha in q]
                kh = [linha[fatia] for linha in k]
                vh = [linha[fatia] for linha in v]
                A = []
                for t in range(n):
                    s = [sum(map(_mul, qh[t], kh[j])) * esc for j in range(t + 1)]
                    A.append(_softmax(s))
                for t in range(n):
                    oh = [0.0] * hd
                    for j, w in enumerate(A[t]):
                        vj = vh[j]
                        for i in range(hd):
                            oh[i] += w * vj[i]
                    o[t][fatia] = oh
                atencoes.append(A)
            y = self._mais_vies(_mm(o, p[f"{l}.Wo"]), p[f"{l}.bo"][0])
            h1 = [[a_ + b_ for a_, b_ in zip(r1, r2)] for r1, r2 in zip(h, y)]
            bb, c2 = self._ln(h1, p[f"{l}.g2"][0], p[f"{l}.b2"][0])
            f = self._mais_vies(_mm(bb, p[f"{l}.W1"]), p[f"{l}.c1"][0])
            th = [[math.tanh(_C_GELU * (u_ + 0.044715 * u_ * u_ * u_)) for u_ in linha] for linha in f]
            gg = [[0.5 * u_ * (1.0 + t_) for u_, t_ in zip(lf, lt)] for lf, lt in zip(f, th)]
            m = self._mais_vies(_mm(gg, p[f"{l}.W2"]), p[f"{l}.c2"][0])
            h2 = [[a_ + b_ for a_, b_ in zip(r1, r2)] for r1, r2 in zip(h1, m)]
            if guardar:
                caches.append(dict(c1=c1, a=a, q=q, k=k, v=v, A=atencoes, o=o, c2=c2, b=bb, f=f, th=th, g=gg))
            h = h2
        hf, cf = self._ln(h, p["gf"][0], p["bf"][0])
        logits = self._mais_vies(_mm(hf, p["U"]), p["c"][0])
        probs = [_softmax(linha) for linha in logits]
        return probs, dict(x=x, camadas=caches, hf=hf, cf=cf)

    def perda(self, x: list[int], y: list[int]) -> float:
        probs, _ = self.adiante(x, guardar=False)
        return -sum(math.log(max(probs[t][y[t]], 1e-300)) for t in range(len(x))) / len(x)

    def gradiente(self, x: list[int], y: list[int], G: dict | None = None) -> float:
        """Acumula em G os gradientes da perda média de uma sequência; devolve a perda."""
        cfg, p = self.cfg, self.p
        n, d, H = len(x), cfg.d, cfg.cabecas
        hd = d // H
        esc = 1.0 / math.sqrt(hd)
        probs, cache = self.adiante(x)
        if G is None:
            G = self.zeros()
        perda = 0.0
        dlog = []
        for t in range(n):
            perda -= math.log(max(probs[t][y[t]], 1e-300))
            linha = [pi / n for pi in probs[t]]
            linha[y[t]] -= 1.0 / n
            dlog.append(linha)
        _somar_em(G["U"], _at_b(cache["hf"], dlog))
        _somar_em(G["c"], [_soma_linhas(dlog)])
        dhf = _mm_bt(dlog, p["U"])
        dh = self._ln_volta(dhf, cache["cf"], p["gf"][0], G["gf"][0], G["bf"][0])
        for l in reversed(range(cfg.camadas)):
            C = cache["camadas"][l]
            # MLP
            _somar_em(G[f"{l}.W2"], _at_b(C["g"], dh))
            _somar_em(G[f"{l}.c2"], [_soma_linhas(dh)])
            dg = _mm_bt(dh, p[f"{l}.W2"])
            df = []
            for lg, lf, lt in zip(dg, C["f"], C["th"]):
                df.append([a * (0.5 * (1.0 + t_) + 0.5 * u_ * (1.0 - t_ * t_) * _C_GELU * (1.0 + 3 * 0.044715 * u_ * u_))
                           for a, u_, t_ in zip(lg, lf, lt)])
            _somar_em(G[f"{l}.W1"], _at_b(C["b"], df))
            _somar_em(G[f"{l}.c1"], [_soma_linhas(df)])
            db = _mm_bt(df, p[f"{l}.W1"])
            dx = self._ln_volta(db, C["c2"], p[f"{l}.g2"][0], G[f"{l}.g2"][0], G[f"{l}.b2"][0])
            dh = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(dh, dx)]
            # atenção
            _somar_em(G[f"{l}.Wo"], _at_b(C["o"], dh))
            _somar_em(G[f"{l}.bo"], [_soma_linhas(dh)])
            do = _mm_bt(dh, p[f"{l}.Wo"])
            dq = [[0.0] * d for _ in range(n)]
            dk = [[0.0] * d for _ in range(n)]
            dv = [[0.0] * d for _ in range(n)]
            for c in range(H):
                ini = c * hd
                A = C["A"][c]
                for t in range(n):
                    dot = do[t][ini:ini + hd]
                    da = []
                    for j in range(t + 1):
                        vj = C["v"][j]
                        da.append(sum(dot[i] * vj[ini + i] for i in range(hd)))
                        w = A[t][j]
                        dvj = dv[j]
                        for i in range(hd):
                            dvj[ini + i] += w * dot[i]
                    s = sum(a * b for a, b in zip(A[t], da))
                    qt = C["q"][t]
                    dqt = dq[t]
                    for j in range(t + 1):
                        ds = A[t][j] * (da[j] - s) * esc
                        if ds == 0.0:
                            continue
                        kj = C["k"][j]
                        dkj = dk[j]
                        for i in range(hd):
                            dqt[ini + i] += ds * kj[ini + i]
                            dkj[ini + i] += ds * qt[ini + i]
            da_ = None
            for nome, dd in (("q", dq), ("k", dk), ("v", dv)):
                _somar_em(G[f"{l}.W{nome}"], _at_b(C["a"], dd))
                _somar_em(G[f"{l}.b{nome}"], [_soma_linhas(dd)])
                parte = _mm_bt(dd, p[f"{l}.W{nome}"])
                da_ = parte if da_ is None else [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(da_, parte)]
            dx = self._ln_volta(da_, C["c1"], p[f"{l}.g1"][0], G[f"{l}.g1"][0], G[f"{l}.b1"][0])
            dh = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(dh, dx)]
        for i, t in enumerate(x):
            le, lp = G["E"][t], G["P"][i]
            for j, v in enumerate(dh[i]):
                le[j] += v
                lp[j] += v
        return perda / n

    def zeros(self) -> dict[str, list[list[float]]]:
        return {k: [[0.0] * len(m[0]) for _ in m] for k, m in self.p.items()}


class AdamW:
    """Adam com decaimento de peso desacoplado (Loshchilov e Hutter), recorte da norma do gradiente
    e taxa com aquecimento linear e decaimento em cosseno."""

    def __init__(self, modelo: ModeloGPT, lr: float = 3e-3, b1: float = 0.9, b2: float = 0.99,
                 eps: float = 1e-8, decaimento: float = 0.01, recorte: float = 1.0):
        self.modelo = modelo
        self.lr, self.b1, self.b2, self.eps = lr, b1, b2, eps
        self.decaimento, self.recorte = decaimento, recorte
        self.m = modelo.zeros()
        self.v = modelo.zeros()
        self.t = 0

    @staticmethod
    def taxa(passo: int, total: int, base: float, aquecimento: int) -> float:
        if passo < aquecimento:
            return base * (passo + 1) / aquecimento
        frac = (passo - aquecimento) / max(1, total - aquecimento)
        return base * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * min(1.0, frac))))

    def passo(self, G: dict, lr: float | None = None) -> float:
        lr = self.lr if lr is None else lr
        norma = math.sqrt(sum(v * v for m in G.values() for linha in m for v in linha))
        fator = min(1.0, self.recorte / (norma + 1e-12)) if self.recorte else 1.0
        self.t += 1
        c1, c2 = 1 - self.b1 ** self.t, 1 - self.b2 ** self.t
        for nome, M in self.modelo.p.items():
            decai = self.decaimento if (len(M) > 1 and nome[-2:] not in ("g1", "g2") and nome not in ("gf",)) else 0.0
            for Mi, Gi, mi, vi in zip(M, G[nome], self.m[nome], self.v[nome]):
                for j in range(len(Mi)):
                    g = Gi[j] * fator
                    mi[j] = self.b1 * mi[j] + (1 - self.b1) * g
                    vi[j] = self.b2 * vi[j] + (1 - self.b2) * g * g
                    Mi[j] -= lr * ((mi[j] / c1) / (math.sqrt(vi[j] / c2) + self.eps) + decai * Mi[j])
        return norma
