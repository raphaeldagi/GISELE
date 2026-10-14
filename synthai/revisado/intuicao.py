"""Intuição (P182, P273): perceber possibilidades que ainda não estão aí.

- no mundo sequencial, o bônus de plano é peso × estimativa × passos restantes, e o peso é aprendido
  comparando a estimativa com a consequência que de fato aconteceu (a sensação corrigindo a intuição);
- no bandido, a "possibilidade" é a do braço pouco explorado: o bônus é a própria estimativa (otimismo, P25)."""


class Intuicao:
    def __init__(self, prior_pares=10.0):
        self.sxy = self.sxx = prior_pares
        self.peso = 1.0

    def bonus(self, opcao, situacao):
        if situacao.explorar:
            return opcao.estimativa
        return self.peso * opcao.estimativa * situacao.restantes

    def corrigir(self, estimativa_escolhida, nivel_antes, nivel_depois):
        """Regressão pela origem da consequência real sobre a estimativa (P273)."""
        c = nivel_depois - nivel_antes
        self.sxy += estimativa_escolhida * c
        self.sxx += estimativa_escolhida * estimativa_escolhida
        self.peso = self.sxy / self.sxx
