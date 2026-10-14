"""A relação com o humano (P71, P112, P118, P131): quando perguntar e quanto da atenção dele gastar.

- limiar de pergunta: P* = 2 × c / ((1 − ε) L), com a imagem fixa do humano ε = 0,1 (a anima, P118) e o dobro
  pelo preço-sombra do orçamento (P131);
- orçamento: só pergunta enquanto a carga recente do humano mais as perguntas deste passo ficam em 0,3 (P108);
  sem orçamento, uma opção que pedia pergunta é descartada, não aceita às cegas;
- no bandido, um orçamento fixo por rodada (3 perguntas, P194), e cada braço é perguntado no máximo uma vez."""

from calculos import p71_valor_da_pergunta


class Relacao:
    def __init__(self, custo=0.1, perda=50.0, eps_crido=0.1, mult=2.0, carga_alvo=0.3, orcamento_rodada=3):
        self.limiar = mult * p71_valor_da_pergunta(custo, perda, eps_crido)
        self.carga_alvo = carga_alvo
        self.orcamento_rodada = orcamento_rodada
        self.nova_rodada()

    def nova_rodada(self):
        self.restante_rodada = self.orcamento_rodada
        self.respostas = {}

    def precisa_perguntar(self, p):
        return p > self.limiar

    def pode_perguntar(self, opcao, situacao):
        if situacao.explorar:
            return id(opcao) in self.respostas or self.restante_rodada > 0
        return situacao.carga_do_humano + situacao.perguntas <= self.carga_alvo

    def perguntar(self, opcao, situacao):
        """Devolve True se o humano vetou."""
        if situacao.explorar:
            if id(opcao) not in self.respostas:
                self.restante_rodada -= 1
                self.respostas[id(opcao)] = situacao.perguntar(opcao)
            return self.respostas[id(opcao)]
        return situacao.perguntar(opcao)
