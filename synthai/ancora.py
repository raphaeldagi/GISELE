"""Âncora (Parte 28, P341): a autorregulação com os pés no chão.

A P333 mostrou que a SYNTHAI que calcula o próprio limiar fica mais ousada: com poucas catástrofes, a priori f = 1
("meu pensamento está calibrado") domina, f sai baixo, o limiar sai alto (uma inflação, P336). Duas âncoras que já
existiam:

- pessimismo sob incerteza (o limite inferior de confiança do RL offline, aqui do lado do risco): usar um quantil
  alto da posterior de f, não a média. Com Poisson e priori Gamma, a posterior é Gamma(k + a, Σp + a); o quantil sai
  da aproximação de Wilson–Hilferty, q ≈ (k/λ)(1 − 1/(9k) + z/(3√k))³. Quando as catástrofes se acumulam, o quantil
  encosta na média: a âncora se solta sozinha;
- a realidade de fora (Jung: o ego ancorado no mundo, por uma adaptação precisa): o histórico AUDITADO que calibrou
  o pensamento também tem catástrofes rotuladas. Nas candidatas desse histórico que ela aceitaria sem perguntar,
  a soma dos p previstos e os rótulos viram a priori de f (só o que a auditoria mostra: rótulos, nunca valores)."""

from math import sqrt

from .autorregulacao import SynthaiAutorregulada


def quantil_gama(forma, taxa, z):
    """Quantil de uma Gamma(forma, taxa) pela aproximação de Wilson–Hilferty (z = quantil da normal)."""
    if forma <= 0:
        return 0.0
    return (forma / taxa) * max(0.0, 1 - 1 / (9 * forma) + z / (3 * sqrt(forma))) ** 3


class SynthaiComAncora(SynthaiAutorregulada):
    def __init__(self, semente=0, z=0.8416, auditoria=True, q_auditoria=0.05, **kw):
        super().__init__(semente, **kw)
        self.z, self.auditoria, self.q_auditoria = z, auditoria, q_auditoria
        self.f_auditado = (0.0, 0.0)

    def calibrar(self, mundo, n=150):
        hist = mundo.historico_auditado(n)
        self.pensamento.calibrar(hist)
        if self.auditoria:
            cats = soma_p = 0.0
            for episodio in hist:
                melhor = max(o.comite for o, _, _ in episodio)
                ordem = sorted(episodio, key=lambda t: -(t[0].nota - t[0].discordancia))
                for o, rotulo, leitura in ordem[: max(1, int(self.q_auditoria * len(ordem)))]:
                    p = self.pensamento.p_catastrofe(o, melhor, leitura)
                    if p <= self.relacao.limiar:  # uma candidata que ela aceitaria sem perguntar
                        soma_p += p
                        cats += 1.0 if rotulo else 0.0
            self.f_auditado = (cats, soma_p)
            self.f_cat += cats
            self.f_p += soma_p
        return self

    def termos(self):
        l_ef, _, dd, b = super().termos()
        f = quantil_gama(self.f_cat, self.f_p, self.z) if self.z else self.f_cat / self.f_p
        return l_ef, f, dd, b
