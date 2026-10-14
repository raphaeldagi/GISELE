"""Sentimento (P35, P42, P68, P202, P78): o juízo de valor que contém os extremos.

- pessimismo: ordena por nota − discordância (+ intuição);
- quantilização: sorteia entre as `q` melhores, nunca vai direto ao topo;
- último passo: sem futuro, a cautela vira caráter e o sorteio fica mais largo (`q_final`);
- veto direto: descarta o que tem probabilidade de catástrofe alta demais para valer a pena perguntar."""


class Sentimento:
    def __init__(self, q=0.05, q_final=0.2, risco_max=0.5):
        self.q, self.q_final, self.risco_max = q, q_final, risco_max

    def ordenar(self, situacao, intuicao):
        return sorted(situacao.opcoes, key=lambda o: -(o.nota - o.discordancia + intuicao.bonus(o, situacao)))

    def candidatas(self, ordem, situacao, rng):
        q = self.q_final if situacao.horizonte > 1 and situacao.restantes == 0 else self.q
        c = ordem[: max(1, int(q * len(ordem)))]
        rng.shuffle(c)
        return c + ordem[len(c):]

    def inaceitavel(self, p):
        return p > self.risco_max
