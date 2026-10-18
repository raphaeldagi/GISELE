"""CFR (Counterfactual Regret Minimization, Zinkevich et al. 2007) no pôquer de Kuhn (Parte 113). Biblioteca padrão, só +, −, ×, ÷ e
comparações. É o caminho que NÃO monta a forma normal (27×64 na Parte 112): aprende jogando contra si mesmo, conjunto de informação
por conjunto de informação, com casamento de arrependimento (regret matching). A estratégia MÉDIA converge para um equilíbrio.

Conjuntos de informação (carta + histórico público): jogador 1 em "" (passa p / aposta b) e em "pb" (desiste p / paga b); jogador 2 em
"p" (passa p / aposta b) e em "b" (desiste p / paga b). A ação 0 é "p" e a 1 é "b". As 6 distribuições de cartas são enumeradas
(sem sorteio): o CFR aqui é determinístico, e a rodada 80 do diálogo o traduz bit a bit."""

CARTAS = (1, 2, 3)
DISTRIBUICOES = tuple((a, b) for a in CARTAS for b in CARTAS if a != b)
HISTORICOS_P1 = ("", "pb")
HISTORICOS_P2 = ("p", "b")


def chaves():
    """Os 12 conjuntos de informação, numa ordem fixa (para o diálogo)."""
    return [(c, h) for c in CARTAS for h in HISTORICOS_P1] + [(c, h) for c in CARTAS for h in HISTORICOS_P2]


def _terminal(h, c1, c2):
    """O payoff do JOGADOR 1 num histórico terminal, ou None se não é terminal."""
    ganha = 1 if c1 > c2 else -1
    if h == "pp":
        return ganha
    if h in ("bb", "pbb"):
        return 2 * ganha
    if h == "bp":
        return 1
    if h == "pbp":
        return -1
    return None


def _jogador(h):
    return 0 if len(h) % 2 == 0 else 1


class CFR:
    def __init__(self):
        self.regret = {k: [0.0, 0.0] for k in chaves()}
        self.soma = {k: [0.0, 0.0] for k in chaves()}

    def estrategia(self, k):
        r = self.regret[k]
        a = r[0] if r[0] > 0.0 else 0.0
        b = r[1] if r[1] > 0.0 else 0.0
        s = a + b
        if s > 0.0:
            return [a / s, b / s]
        return [0.5, 0.5]

    def _cfr(self, c1, c2, h, p1, p2):
        """Valor do histórico h para o JOGADOR 1, com as alcances p1, p2; atualiza arrependimentos e somas."""
        u = _terminal(h, c1, c2)
        if u is not None:
            return float(u)
        j = _jogador(h)
        k = (c1 if j == 0 else c2, h)
        s = self.estrategia(k)
        util = [0.0, 0.0]
        no = 0.0
        for a, letra in enumerate("pb"):
            if j == 0:
                util[a] = self._cfr(c1, c2, h + letra, p1 * s[a], p2)
            else:
                util[a] = self._cfr(c1, c2, h + letra, p1, p2 * s[a])
            no = no + s[a] * util[a]
        sinal = 1.0 if j == 0 else -1.0
        alcance_adv = p2 if j == 0 else p1
        alcance_prop = p1 if j == 0 else p2
        for a in range(2):
            self.regret[k][a] = self.regret[k][a] + alcance_adv * sinal * (util[a] - no)
            self.soma[k][a] = self.soma[k][a] + alcance_prop * s[a]
        return no

    def iterar(self, n):
        for _ in range(n):
            for c1, c2 in DISTRIBUICOES:
                self._cfr(c1, c2, "", 1.0, 1.0)
        return self

    def media(self):
        """A estratégia MÉDIA (a que converge): {chave: [P(p), P(b)]}."""
        out = {}
        for k in chaves():
            a, b = self.soma[k]
            s = a + b
            out[k] = [a / s, b / s] if s > 0.0 else [0.5, 0.5]
        return out


def valor(estr):
    """O valor exato para o jogador 1 de um perfil de comportamento {chave: [P(p), P(b)]}, por enumeração das 6 distribuições."""
    def v(c1, c2, h):
        u = _terminal(h, c1, c2)
        if u is not None:
            return float(u)
        j = _jogador(h)
        s = estr[(c1 if j == 0 else c2, h)]
        return s[0] * v(c1, c2, h + "p") + s[1] * v(c1, c2, h + "b")
    tot = 0.0
    for c1, c2 in DISTRIBUICOES:
        tot = tot + v(c1, c2, "") / 6.0
    return tot


def _melhor_resposta(estr, jogador):
    """O valor (para o jogador 1) quando `jogador` (0 ou 1) responde da melhor forma ao comportamento do outro em `estr`. Enumera as
    estratégias puras de comportamento do respondente (2^6 = 64) — exato."""
    from itertools import product
    meus = [k for k in chaves() if (k[1] in HISTORICOS_P1) == (jogador == 0)]
    melhor = None
    for escolha in product((0, 1), repeat=len(meus)):
        e = dict(estr)
        for k, a in zip(meus, escolha):
            e[k] = [1.0 - a, float(a)]
        x = valor(e)
        if melhor is None or (x > melhor if jogador == 0 else x < melhor):
            melhor = x
    return melhor


def explorabilidade(estr):
    """Quanto o perfil cede no total a melhores respostas: (BR do jogador 1 contra o 2) − (BR do 2 contra o 1). É 0 só no equilíbrio."""
    return _melhor_resposta(estr, 0) - _melhor_resposta(estr, 1)
