"""O pôquer Leduc (Southey et al. 2005) e o CFR nele (Parte 120): vanilla, com o acaso amostrado e com amostragem externa. Biblioteca padrão.

As regras: 6 cartas (valete, dama e rei, duas de cada), ante 1 de cada jogador, uma carta privada para cada um e uma pública revelada entre
as duas rodadas de aposta. Aposta fixa de 2 na 1ª rodada e de 4 na 2ª, no máximo 2 aumentos por rodada, e o jogador 1 abre as duas. Ações: "c"
(passar/pagar), "r" (apostar/aumentar), "f" (desistir, só diante de uma aposta). No confronto, quem pareia com a pública ganha; senão, a maior
carta; cartas iguais dividem. O histórico é a 1ª rodada, "/", a 2ª. O acaso são as 120 distribuições ordenadas (6 × 5 × 4) das cartas.

Um conjunto de informação é (carta própria, carta pública ou −1, histórico). O CFR é o da Parte 113 com 2 ou 3 ações."""

from itertools import permutations

POSTOS = (0, 0, 1, 1, 2, 2)                    # valete, dama, rei
DISTRIBUICOES = tuple((POSTOS[a], POSTOS[b], POSTOS[c]) for a, b, c in permutations(range(6), 3))   # (carta 1, carta 2, pública)
APOSTA = (2, 4)


def _rodada(h):
    return h.split("/")[-1], h.count("/")


def acoes(h):
    s, _ = _rodada(h)
    if s.endswith("r"):
        return ("f", "c", "r") if s.count("r") < 2 else ("f", "c")
    return ("c", "r")


def jogador(h):
    return len(_rodada(h)[0]) % 2


def _rodada_acabou(s):
    return s == "cc" or (len(s) >= 2 and s.endswith("rc"))


def proximo(h, a):
    """O histórico depois da ação a; se a rodada 1 acaba, abre a 2ª com "/"."""
    h2 = h + a
    s, r = _rodada(h2)
    if r == 0 and _rodada_acabou(s):
        return h2 + "/"
    return h2


def contribuicoes(h):
    """Quanto cada jogador pôs no pote ao fim do histórico (ante incluído)."""
    pos = [1, 1]
    for r, s in enumerate(h.split("/")):
        devido = [0, 0]
        for i, a in enumerate(s):
            p = i % 2
            if a == "c":
                devido[p] = max(devido)
            elif a == "r":
                devido[p] = max(devido) + APOSTA[r]
        pos[0] += devido[0]
        pos[1] += devido[1]
    return pos


def terminal(h, c1, c2, b):
    """O ganho do JOGADOR 1 se h é terminal, senão None."""
    s, r = _rodada(h)
    if s.endswith("f"):
        quem = (len(s) - 1) % 2                  # quem desistiu
        pos = contribuicoes(h[:-1])
        return -float(pos[0]) if quem == 0 else float(pos[1])
    if r == 1 and _rodada_acabou(s):
        pos = contribuicoes(h)
        f1 = 10 + c1 if c1 == b else c1
        f2 = 10 + c2 if c2 == b else c2
        return float(pos[1]) if f1 > f2 else (-float(pos[0]) if f2 > f1 else 0.0)
    return None


def chave(h, c1, c2, b):
    j = jogador(h)
    return (c1 if j == 0 else c2, b if "/" in h else -1, h)


class CFRLeduc:
    def __init__(self):
        self.regret, self.soma = {}, {}
        self.nos = 0

    def estrategia(self, k, n):
        r = self.regret.get(k)
        if r is None:
            return [1.0 / n] * n
        pos = [x if x > 0.0 else 0.0 for x in r]
        s = 0.0
        for x in pos:
            s += x
        return [x / s for x in pos] if s > 0.0 else [1.0 / n] * n

    def _cfr(self, c1, c2, b, h, p1, p2):
        self.nos += 1
        u = terminal(h, c1, c2, b)
        if u is not None:
            return u
        j = jogador(h)
        acs = acoes(h)
        k = chave(h, c1, c2, b)
        s = self.estrategia(k, len(acs))
        util = [0.0] * len(acs)
        no = 0.0
        for i, a in enumerate(acs):
            util[i] = self._cfr(c1, c2, b, proximo(h, a), p1 * s[i], p2) if j == 0 else self._cfr(c1, c2, b, proximo(h, a), p1, p2 * s[i])
            no += s[i] * util[i]
        sinal = 1.0 if j == 0 else -1.0
        adv, prop = (p2, p1) if j == 0 else (p1, p2)
        r = self.regret.setdefault(k, [0.0] * len(acs))
        m = self.soma.setdefault(k, [0.0] * len(acs))
        for i in range(len(acs)):
            r[i] += adv * sinal * (util[i] - no)
            m[i] += prop * s[i]
        return no

    def _es(self, c1, c2, b, h, i, g):
        self.nos += 1
        u = terminal(h, c1, c2, b)
        if u is not None:
            return u if i == 0 else -u
        j = jogador(h)
        acs = acoes(h)
        k = chave(h, c1, c2, b)
        s = self.estrategia(k, len(acs))
        if j == i:
            util = [self._es(c1, c2, b, proximo(h, a), i, g) for a in acs]
            no = 0.0
            for x, y in zip(s, util):
                no += x * y
            r = self.regret.setdefault(k, [0.0] * len(acs))
            for t in range(len(acs)):
                r[t] += util[t] - no
            return no
        m = self.soma.setdefault(k, [0.0] * len(acs))
        for t in range(len(acs)):
            m[t] += s[t]
        x = g.uniforme()
        acum, escolhida = 0.0, acs[-1]
        for t, a in enumerate(acs):
            acum += s[t]
            if x < acum:
                escolhida = a
                break
        return self._es(c1, c2, b, proximo(h, escolhida), i, g)

    def vanilla(self, n):
        for _ in range(n):
            for c1, c2, b in DISTRIBUICOES:
                self._cfr(c1, c2, b, "", 1.0, 1.0)
        return self

    def acaso(self, n, semente):
        from synthai.mccfr_externo import LCGFracao
        g = LCGFracao(semente)
        for _ in range(n):
            c1, c2, b = DISTRIBUICOES[g.inteiro(120)]
            self._cfr(c1, c2, b, "", 1.0, 1.0)
        return self

    def externo(self, n, semente):
        from synthai.mccfr_externo import LCGFracao
        g = LCGFracao(semente)
        for _ in range(n):
            for i in (0, 1):
                c1, c2, b = DISTRIBUICOES[g.inteiro(120)]
                self._es(c1, c2, b, "", i, g)
        return self

    def media(self):
        out = {}
        for k, m in self.soma.items():
            s = 0.0
            for x in m:
                s += x
            out[k] = [x / s for x in m] if s > 0.0 else [1.0 / len(m)] * len(m)
        return out


def conjuntos_de_informacao():
    """Todos os conjuntos de informação alcançáveis, por jogador. Devolve (do jogador 1, do jogador 2)."""
    vistos = (set(), set())

    def anda(c1, c2, b, h):
        if terminal(h, c1, c2, b) is not None:
            return
        vistos[jogador(h)].add(chave(h, c1, c2, b))
        for a in acoes(h):
            anda(c1, c2, b, proximo(h, a))
    for c1, c2, b in DISTRIBUICOES:
        anda(c1, c2, b, "")
    return vistos


def _estr(estr, k, n):
    return estr.get(k) or [1.0 / n] * n


def valor(estr):
    """O valor exato para o jogador 1 de um perfil {chave: probabilidades}, média nas 120 distribuições."""
    def v(c1, c2, b, h):
        u = terminal(h, c1, c2, b)
        if u is not None:
            return u
        acs = acoes(h)
        s = _estr(estr, chave(h, c1, c2, b), len(acs))
        tot = 0.0
        for i, a in enumerate(acs):
            tot += s[i] * v(c1, c2, b, proximo(h, a))
        return tot
    tot = 0.0
    for d in DISTRIBUICOES:
        tot += v(*d, "")
    return tot / len(DISTRIBUICOES)


def melhor_resposta(estr, resp):
    """O valor para o jogador 1 quando `resp` (0 ou 1) responde da melhor forma ao comportamento do outro em `estr`. Exato: as decisões do
    respondente são escolhidas conjunto por conjunto, do mais fundo (histórico mais longo) para o mais raso, somando sobre as distribuições
    e históricos do conjunto o ganho pesado pela alcance do adversário e do acaso."""
    entradas = {}

    def anda(c1, c2, b, h, alc):
        if terminal(h, c1, c2, b) is not None:
            return
        acs = acoes(h)
        k = chave(h, c1, c2, b)
        if jogador(h) == resp:
            entradas.setdefault(k, []).append((c1, c2, b, h, alc))
            for a in acs:
                anda(c1, c2, b, proximo(h, a), alc)
        else:
            s = _estr(estr, k, len(acs))
            for i, a in enumerate(acs):
                if s[i] > 0.0:
                    anda(c1, c2, b, proximo(h, a), alc * s[i])
    for d in DISTRIBUICOES:
        anda(*d, "", 1.0)
    escolha, memo = {}, {}
    sinal = 1.0 if resp == 0 else -1.0

    def v(c1, c2, b, h):
        key = (c1, c2, b, h)
        if key in memo:
            return memo[key]
        u = terminal(h, c1, c2, b)
        if u is not None:
            return u
        acs = acoes(h)
        k = chave(h, c1, c2, b)
        if jogador(h) == resp:
            x = v(c1, c2, b, proximo(h, escolha[k]))
        else:
            s = _estr(estr, k, len(acs))
            x = 0.0
            for i, a in enumerate(acs):
                if s[i] > 0.0:
                    x += s[i] * v(c1, c2, b, proximo(h, a))
        memo[key] = x
        return x
    for k in sorted(entradas, key=lambda k: -len(k[2])):
        acs = acoes(k[2])
        melhor, qual = None, None
        for a in acs:
            tot = 0.0
            for c1, c2, b, h, alc in entradas[k]:
                tot += alc * v(c1, c2, b, proximo(h, a))
            if melhor is None or sinal * tot > sinal * melhor:
                melhor, qual = tot, a
        escolha[k] = qual
    tot = 0.0
    for d in DISTRIBUICOES:
        tot += v(*d, "")
    return tot / len(DISTRIBUICOES)


def explorabilidade(estr):
    return melhor_resposta(estr, 0) - melhor_resposta(estr, 1)
