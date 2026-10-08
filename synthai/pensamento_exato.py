"""Pensamento diferenciado (Parte 24, P302): o mesmo modelo logístico do `pensamento`, ajustado até convergir.

O `Pensamento` da Parte 22 faz 3 épocas de gradiente (taxa 0,05), como a SYNTHAI faz desde a P83, e a P293 mostrou
que ele para longe do fim (peso da leitura 0,73 com d' = 1). Aqui o ajuste é o de Newton (IRLS), que converge
quadraticamente, com a correção de Firth (1993) opcional: a verossimilhança penalizada pela priori de Jeffreys,
½ log |I(w)|, que reduz o viés de eventos raros (King e Zeng, 2001). A catástrofe é rara: ~0,5% das opções.

Depois de calibrado, o aprendizado com os próprios resultados (sombra própria) continua o mesmo do `Pensamento`."""

from math import exp, log

from .pensamento import Pensamento
from .reconhecimento import SynthaiExploradora


def _inversa(m):
    n = len(m)
    a = [list(linha) + [1.0 if i == j else 0.0 for j in range(n)] for i, linha in enumerate(m)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[piv] = a[piv], a[c]
        d = a[c][c]
        a[c] = [x / d for x in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0.0:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [linha[n:] for linha in a]


def _sigmoide(z):
    return 1 / (1 + exp(-max(-30.0, min(30.0, z))))


def ajustar_logistica(xs, ys, firth=True, iteracoes=30, passo_max=5.0, cresta=1e-6):
    """Newton–Raphson para a logística (com o escore modificado de Firth, se pedido). Devolve os pesos."""
    k = len(xs[0])
    w = [0.0] * k
    for _ in range(iteracoes):
        ps = [_sigmoide(sum(wi * xi for wi, xi in zip(w, x))) for x in xs]
        info = [[cresta if i == j else 0.0 for j in range(k)] for i in range(k)]
        for x, p in zip(xs, ps):
            v = p * (1 - p)
            for i in range(k):
                vi = v * x[i]
                for j in range(i, k):
                    info[i][j] += vi * x[j]
        for i in range(k):
            for j in range(i):
                info[i][j] = info[j][i]
        inv = _inversa(info)
        escore = [0.0] * k
        for x, p, y in zip(xs, ps, ys):
            r = y - p
            if firth:  # alavanca h = v x' I⁻¹ x; escore modificado: y − p + h (½ − p)
                ix = [sum(inv[i][j] * x[j] for j in range(k)) for i in range(k)]
                h = p * (1 - p) * sum(a * b for a, b in zip(x, ix))
                r += h * (0.5 - p)
            for i in range(k):
                escore[i] += r * x[i]
        passo = [sum(inv[i][j] * escore[j] for j in range(k)) for i in range(k)]
        tamanho = max(abs(s) for s in passo)
        if tamanho > passo_max:
            passo = [s * passo_max / tamanho for s in passo]
        w = [wi + si for wi, si in zip(w, passo)]
        if tamanho < 1e-9:
            break
    return w


def perda_logistica(w, xs, ys):
    """Log-perda média (nats): a régua da calibração."""
    total = 0.0
    for x, y in zip(xs, ys):
        p = min(1 - 1e-12, max(1e-12, _sigmoide(sum(wi * xi for wi, xi in zip(w, x)))))
        total -= y * log(p) + (1 - y) * log(1 - p)
    return total / len(xs)


def dados_do_historico(historico):
    xs, ys = [], []
    for episodio in historico:
        melhor = max(o.comite for o, _, _ in episodio)
        for o, rotulo, leitura in episodio:
            xs.append((1.0, o.discordancia, o.comite - melhor, leitura))  # as variáveis do Pensamento (testado)
            ys.append(1.0 if rotulo else 0.0)
    return xs, ys


class PensamentoExato(Pensamento):
    def __init__(self, taxa=0.05, firth=True):
        super().__init__(taxa)
        self.firth = firth

    def calibrar(self, historico, epocas=None):
        xs, ys = dados_do_historico(historico)
        self.w = ajustar_logistica(xs, ys, self.firth)


class SynthaiPensante(SynthaiExploradora):
    """A versão principal da Parte 23 com o pensamento ajustado até convergir (P305)."""

    def __init__(self, semente=0, firth=True, **kw):
        super().__init__(semente, **kw)
        self.pensamento = PensamentoExato(firth=firth)
        self.percepcao.pensamento = self.pensamento  # o neutro (se ligado) lê o peso deste pensamento
