"""Réguas, não agentes (P265): o acaso (0 do Υ), o guloso (só a função dominante, sem cautela nem humano) e o
oráculo (1 do Υ), que lê os atributos escondidos das opções e por isso sabe o que nenhum agente poderia saber."""

from calculos import _rng


class _Referencia:
    vetados_agora = ()

    def __init__(self, semente=0):
        self.rng = _rng(semente)

    def calibrar(self, mundo, n=150):
        return self

    def nova_rodada(self):
        pass

    def observar(self, resultado):
        pass


class Acaso(_Referencia):
    def decidir(self, sit):
        return sit.opcoes[self.rng.randrange(len(sit.opcoes))]


class Guloso(_Referencia):
    """A intuição sozinha (o tipo 'puro' de Jung): nota + bônus de futuro, sem sentimento, pensamento ou relação."""

    def decidir(self, sit):
        bonus = (lambda o: o.estimativa) if sit.explorar else (lambda o: o.estimativa * sit.restantes)
        return max(sit.opcoes, key=lambda o: o.nota + bonus(o))


class Oraculo(_Referencia):
    def decidir(self, sit):
        seguras = [o for o in sit.opcoes if not o._catastrofe] or sit.opcoes
        return max(seguras, key=lambda o: o._valor + o._consequencia * sit.restantes)
