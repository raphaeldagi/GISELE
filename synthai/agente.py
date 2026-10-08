"""A SYNTHAI montada a partir dos módulos (P281): cada função de Jung é um objeto, e o agente só os põe em ordem.

    sensação (Percepcao) → intuição (Intuicao) + sentimento (Sentimento) ordenam → pensamento (Pensamento) avalia
    o risco de cada candidata → relação (Relacao) decide se pergunta ao humano → escolha → observar o resultado
    corrige o pensamento (sombra própria, P104) e a intuição (sensação corrige intuição, P273).

O agente só recebe uma `Situacao` e só lê o que é público nas opções; o teste da P285 confere isso no código."""

from calculos import _rng

from .intuicao import Intuicao
from .pensamento import Pensamento
from .percepcao import Percepcao
from .relacao import Relacao
from .sentimento import Sentimento


class Synthai:
    def __init__(self, semente=0, foco=0.1, q=0.05, q_final=0.2, risco_max=0.5, carga_alvo=0.3):
        self.percepcao = Percepcao(foco)
        self.pensamento = Pensamento()
        self.intuicao = Intuicao()
        self.sentimento = Sentimento(q, q_final, risco_max)
        self.relacao = Relacao(carga_alvo=carga_alvo)
        self.rng = _rng(semente)
        self.vetados_agora = []
        self._escolha = None

    def calibrar(self, mundo, n=150):
        """Calibra o pensamento num histórico auditado do mundo (P83: 150 passos, como em `_construir_seq`)."""
        self.pensamento.calibrar(mundo.historico_auditado(n))
        return self

    def nova_rodada(self):
        self.relacao.nova_rodada()

    def decidir(self, sit):
        self.vetados_agora = []
        leituras = self.percepcao.perceber(sit)
        ordem = self.sentimento.ordenar(sit, self.intuicao)
        melhor = max(o.comite for o in sit.opcoes)
        for o in self.sentimento.candidatas(ordem, sit, self.rng):
            leitura = leituras.get(id(o), 0.0)
            p = self.pensamento.p_catastrofe(o, melhor, leitura)
            if self.sentimento.inaceitavel(p):
                continue
            if self.relacao.precisa_perguntar(p):
                if not self.relacao.pode_perguntar(o, sit):
                    continue
                if self.relacao.perguntar(o, sit):
                    self.vetados_agora.append(o)
                    continue
            self._escolha = (o, melhor, leitura, sit.restantes, sit.explorar)
            return o
        self._escolha = None
        return ordem[0]

    def observar(self, resultado):
        if self._escolha is None:
            return
        o, melhor, leitura, restantes, explorar = self._escolha
        self.pensamento.aprender(o, melhor, leitura, 1.0 if resultado.catastrofe else 0.0)
        if not explorar and restantes > 0 and not resultado.catastrofe:
            self.intuicao.corrigir(o.estimativa, resultado.nivel_antes, resultado.nivel_depois)
        self._escolha = None
