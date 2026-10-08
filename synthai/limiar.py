"""O sentimento que acompanha o pensamento (Parte 25, P311).

A P305 mostrou que um pensamento preciso com o limiar de pergunta antigo (2 P*, achado na P131 com um pensamento
rombudo) quase dobra as catástrofes. Duas respostas que já existiam:

- recalibrar o limiar para o pensamento novo: com orçamento de perguntas, a regra ótima pergunta onde o valor da
  pergunta passa do preço-sombra λ do orçamento (relaxação de Lagrange), o que dá um limiar no quantil da
  probabilidade das candidatas que gasta o orçamento (P312);
- ajustar o pensamento onde a decisão acontece: a verossimilhança local (Eguchi e Copas, 1998) pesa as observações
  perto do ponto de interesse; aqui, só as opções do topo de cada episódio auditado entram no ajuste (P313)."""

from .pensamento_exato import PensamentoExato, SynthaiPensante, ajustar_logistica
from .relacao import Relacao


def dados_do_topo(historico, fracao):
    """As variáveis do Pensamento, mas só das `fracao` melhores opções (nota − discordância) de cada episódio. A
    'melhor nota' de referência continua sendo a do episódio inteiro."""
    xs, ys = [], []
    for episodio in historico:
        melhor = max(o.comite for o, _, _ in episodio)
        ordem = sorted(episodio, key=lambda t: -(t[0].nota - t[0].discordancia))
        for o, rotulo, leitura in ordem[: max(1, int(fracao * len(ordem)))]:
            xs.append((1.0, o.discordancia, o.comite - melhor, leitura))
            ys.append(1.0 if rotulo else 0.0)
    return xs, ys


class PensamentoLocal(PensamentoExato):
    def __init__(self, fracao=0.1, **kw):
        super().__init__(**kw)
        self.fracao = fracao

    def calibrar(self, historico, epocas=None):
        xs, ys = dados_do_topo(historico, self.fracao)
        self.w = ajustar_logistica(xs, ys, self.firth)


class SynthaiAjustada(SynthaiPensante):
    """Pensamento exato (ou local) com o limiar de pergunta mult × P* escolhido para ele."""

    def __init__(self, semente=0, mult=2.0, local=False, fracao=0.1, **kw):
        super().__init__(semente, **kw)
        self.relacao = Relacao(mult=mult, carga_alvo=self.relacao.carga_alvo)
        if local:
            self.pensamento = PensamentoLocal(fracao)
            self.percepcao.pensamento = self.pensamento
