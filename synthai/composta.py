"""A SYNTHAI composta (Parte 29, P351): compor em vez de herdar.

A Parte 28 mostrou o defeito da linhagem de versões: a âncora herdou o pensamento de Newton, que perde no bandido. O
princípio é o do livro *Design Patterns* (1994): "prefira a composição de objetos à herança de classes", e a forma mais
extrema da composição é a DELEGAÇÃO. A SynthaiComposta não é nenhuma das versões: ela TEM duas e passa cada decisão
para a que funciona naquele tipo de situação:

- no bandido (situação de exploração): a versão principal (SynthaiExploradora), que explora por Thompson;
- fora dele: a SYNTHAI ancorada (P343), que calcula o próprio limiar com as âncoras.

As duas são calibradas com o MESMO histórico auditado (um só pedido ao mundo), então cada uma decide exatamente como
decidiria sozinha. Qualquer módulo de dentro pode ser trocado de fora (por exemplo, o pensamento rico, P353)."""

from .ancora import SynthaiComAncora
from .reconhecimento import SynthaiExploradora


class _HistoricoFixo:
    """Entrega o mesmo histórico auditado a mais de um agente."""

    def __init__(self, historico):
        self.historico = historico

    def historico_auditado(self, n):
        return self.historico


class SynthaiComposta:
    def __init__(self, semente=0, fora=None, bandido=None):
        self.fora = fora if fora is not None else SynthaiComAncora(semente, z=0.8416, auditoria=True)
        self.bandido = bandido if bandido is not None else SynthaiExploradora(semente)
        self._ultimo = self.fora

    def calibrar(self, mundo, n=150):
        fixo = _HistoricoFixo(mundo.historico_auditado(n))
        self.fora.calibrar(fixo, n)
        self.bandido.calibrar(fixo, n)
        return self

    def decidir(self, sit):
        self._ultimo = self.bandido if sit.explorar else self.fora
        return self._ultimo.decidir(sit)

    def observar(self, resultado):
        self._ultimo.observar(resultado)

    def nova_rodada(self):
        self.bandido.nova_rodada()
        self.fora.nova_rodada()

    @property
    def vetados_agora(self):
        return self._ultimo.vetados_agora

    @property
    def relacao(self):
        return self._ultimo.relacao


def composta_rica(semente=0):
    """A composta com o pensamento rico (10 pesos) na parte de fora do bandido: um módulo trocado de fora."""
    from .pensamento_rico import PensamentoRico
    c = SynthaiComposta(semente)
    c.fora.pensamento = PensamentoRico()
    c.fora.percepcao.pensamento = c.fora.pensamento
    return c
