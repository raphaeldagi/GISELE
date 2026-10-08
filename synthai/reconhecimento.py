"""Reconhecimento (Parte 23, P291): o que a SYNTHAI já sabia e não usava.

Cada classe aqui troca uma heurística dos módulos da Parte 22 por uma conta que já estava resolvida, sem
editar os módulos originais (eles são medidos pela P285):

- LeiturasNeutras (P292): uma opção sem leitura do sensor não vale "leitura 0". Com sensor gaussiano de
  sensibilidade d', o log da razão de verossimilhança é d'(s − d'/2): o ponto neutro é s = d'/2 (teoria de
  detecção de sinais). A SYNTHAI estima d' com o próprio peso da leitura no pensamento (w₃), então o neutro é w₃/2.
- PercepcaoReconhecida (P293): a atenção olha onde a decisão vai olhar (nota − discordância + intuição),
  e, no bandido, lembra o que já leu na rodada.
- IntuicaoBayes (P295): no bandido, a exploração é da própria SYNTHAI, por amostragem de Thompson (1933) sobre
  as contagens que ela viu (assintoticamente ótima em braços de Bernoulli: Kaufmann, Korda e Munos, 2012).
- SynthaiReconhecida: a Synthai da Parte 22 com essas três peças.
"""

from calculos import _rng

from .agente import Synthai
from .intuicao import Intuicao
from .percepcao import Percepcao


class LeiturasNeutras(dict):
    """Dicionário de leituras em que a leitura que falta vale o ponto neutro, não zero."""

    def __init__(self, leituras, neutro):
        super().__init__(leituras)
        self.neutro = neutro

    def get(self, chave, padrao=None):
        return dict.get(self, chave, self.neutro)


class PercepcaoReconhecida(Percepcao):
    def __init__(self, foco=0.1, pensamento=None, intuicao=None, neutro=True, atencao_inteira=True, memoria=True):
        super().__init__(foco)
        self.pensamento, self.intuicao = pensamento, intuicao
        self.neutro, self.atencao_inteira, self.memoria = neutro, atencao_inteira, memoria
        self.lembradas = {}

    def esquecer(self):
        self.lembradas = {}

    def perceber(self, situacao):
        if self.atencao_inteira and self.intuicao is not None:
            chave = lambda o: -(o.nota - o.discordancia + self.intuicao.bonus(o, situacao))
        else:
            chave = lambda o: -(o.nota - o.discordancia)
        ordem = sorted(situacao.opcoes, key=chave)
        alvo = ordem[: max(1, int(self.foco * len(ordem)))]
        lidas = {id(o): situacao.ler_sensor(o) for o in alvo}
        if self.memoria and situacao.explorar:
            self.lembradas.update(lidas)
            lidas = {id(o): self.lembradas[id(o)] for o in situacao.opcoes if id(o) in self.lembradas}
        neutro = self.pensamento.w[3] / 2 if (self.neutro and self.pensamento is not None) else 0.0
        return LeiturasNeutras(lidas, neutro)


class IntuicaoBayes(Intuicao):
    """Fora do bandido, igual à Intuicao. No bandido, o bônus é o desvio de uma amostra da posterior Beta em
    relação à média dela: a nota já tem a média; a amostra acrescenta a dúvida que ainda resta."""

    def __init__(self, semente=0, **kw):
        super().__init__(**kw)
        self.rng = _rng(semente + 23)
        self._amostra = {}

    def nova_decisao(self):
        self._amostra = {}

    def bonus(self, opcao, situacao):
        if not situacao.explorar:
            return super().bonus(opcao, situacao)
        k = id(opcao)
        if k not in self._amostra:  # uma amostra por braço por decisão (percepção e decisão veem a mesma)
            a, b = 1 + opcao.sucessos, 1 + opcao.vezes - opcao.sucessos
            self._amostra[k] = self.rng.betavariate(a, b) - a / (a + b)
        return self._amostra[k]


class SynthaiReconhecida(Synthai):
    def __init__(self, semente=0, neutro=True, atencao_inteira=True, memoria=True, thompson=True, **kw):
        super().__init__(semente, **kw)
        if thompson:
            self.intuicao = IntuicaoBayes(semente)
        self.percepcao = PercepcaoReconhecida(self.percepcao.foco, self.pensamento, self.intuicao,
                                              neutro, atencao_inteira, memoria)

    def nova_rodada(self):
        super().nova_rodada()
        self.percepcao.esquecer()

    def decidir(self, sit):
        if hasattr(self.intuicao, "nova_decisao"):
            self.intuicao.nova_decisao()
        return super().decidir(sit)
