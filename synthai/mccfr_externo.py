"""MCCFR com amostragem EXTERNA (Lanctot et al. 2009) no pôquer de Kuhn (Parte 119). Biblioteca padrão.

A Parte 118 sorteava só o acaso (a distribuição de cartas) e percorria as ações dos DOIS jogadores. Aqui, para cada jogador i (o "viajante"),
sorteia-se o acaso E as ações do adversário segundo a estratégia corrente dele; só as ações do próprio viajante são todas percorridas. O
arrependimento de i em I soma v(a) − v(I) SEM o peso de alcance (a amostragem já faz esse papel em média), e a estratégia média soma σ(I) quando
o ADVERSÁRIO passa por I (a média "estocástica" da amostragem externa). O sorteio usa um LCG inteiro, e o número em [0, 1) é x/2³¹ (exato),
para que a rodada 86 o traduza bit a bit."""

from synthai.cfr import CFR, DISTRIBUICOES, _terminal, _jogador


class LCGFracao:
    def __init__(self, semente):
        self.x = semente

    def inteiro(self, n):
        self.x = (1103515245 * self.x + 12345) % 2147483648
        return (self.x >> 16) % n

    def uniforme(self):
        self.x = (1103515245 * self.x + 12345) % 2147483648
        return self.x / 2147483648.0


class CFRExterno(CFR):
    def _es(self, c1, c2, h, i, g):
        u = _terminal(h, c1, c2)
        if u is not None:
            return float(u) if i == 0 else -float(u)
        j = _jogador(h)
        k = (c1 if j == 0 else c2, h)
        s = self.estrategia(k)
        if j == i:
            util = [self._es(c1, c2, h + "p", i, g), self._es(c1, c2, h + "b", i, g)]
            no = s[0] * util[0] + s[1] * util[1]
            for a in range(2):
                self.regret[k][a] = self.regret[k][a] + (util[a] - no)
            return no
        for a in range(2):
            self.soma[k][a] = self.soma[k][a] + s[a]
        return self._es(c1, c2, h + ("p" if g.uniforme() < s[0] else "b"), i, g)

    def iterar_externo(self, n, semente):
        g = LCGFracao(semente)
        for _ in range(n):
            for i in (0, 1):
                c1, c2 = DISTRIBUICOES[g.inteiro(6)]
                self._es(c1, c2, "", i, g)
        return self


def explorabilidade_externa(iteracoes, semente):
    from synthai.cfr import explorabilidade
    return explorabilidade(CFRExterno().iterar_externo(iteracoes, semente).media())
