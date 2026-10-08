"""Autorregulação (Parte 27, P331): a SYNTHAI calcula o próprio limiar de pergunta.

A Parte 26 achou o limiar certo pela conta m = Δd / (f · L · P*), mas mediu os termos com a régua (lendo o escondido).
Aqui a SYNTHAI estima os três termos só com o que ela observa (a regra da Parte 7):

- L (o custo de uma catástrofe): a perda fixa mais o retorno que os próprios episódios dela ainda davam a partir do
  passo em que a catástrofe aconteceu (F(t), médio nos episódios completos dela);
- f (quanto o pensamento subestima o risco do que aceita sem perguntar): catástrofes observadas / soma dos p previstos
  nessas escolhas, com uma priori f = 1 de peso `peso_priori_f` catástrofes esperadas;
- Δd (o valor perdido ao descartar): o valor de uma opção descartada nunca é visto. A SYNTHAI o estima pela nota do
  comitê (que ela vê), convertida em valor por uma regressão valor ~ nota aprendida com as próprias escolhas (o valor
  recebido menos o nível), mais o plano da intuição (peso × estimativa × passos restantes).

A cada `intervalo` decisões, depois de `aquecimento`, refaz m e o põe no limiar (entre `m_min` e `m_max`). No bandido
(exploração), o orçamento é por rodada e nada disso se aplica: a relação fica como estava.

Jung: a compensação deixa de ser calculada de fora (Parte 25) e passa a ser uma autorregulação da própria psique."""

from calculos import p71_valor_da_pergunta

from .limiar import SynthaiAjustada
from .relacao import Relacao


class RelacaoAutorregulada(Relacao):
    """A Relacao de sempre, que anota o que precisa para a conta: o p das aceitas sem perguntar e as descartadas."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.aceita_p = None
        self.descartadas = []

    def precisa_perguntar(self, p):
        r = super().precisa_perguntar(p)
        if not r:
            self.aceita_p = p  # no laço de decisão, a primeira candidata que não precisa de pergunta é aceita
        return r

    def pode_perguntar(self, opcao, situacao):
        r = super().pode_perguntar(opcao, situacao)
        if not r and not situacao.explorar:
            self.descartadas.append(opcao)
        return r


class SynthaiAutorregulada(SynthaiAjustada):
    def __init__(self, semente=0, mult=2.0, local=False, perda=50.0, intervalo=50, aquecimento=200,
                 peso_priori_f=0.5, m_min=0.25, m_max=16.0, newton=True, **kw):
        super().__init__(semente, mult=mult, local=local, **kw)
        if not newton:  # volta ao pensamento de gradiente da Parte 22 (o da versão principal)
            from .pensamento import Pensamento
            self.pensamento = Pensamento()
            self.percepcao.pensamento = self.pensamento
        self.relacao = RelacaoAutorregulada(mult=mult, carga_alvo=self.relacao.carga_alvo)
        self.p_estrela = p71_valor_da_pergunta()
        self.perda, self.intervalo, self.aquecimento = perda, intervalo, aquecimento
        self.m_min, self.m_max, self.mult = m_min, m_max, mult
        # f: catástrofes e p previstos nas aceitas sem perguntar (com priori f = 1)
        self.f_cat, self.f_p = peso_priori_f, peso_priori_f
        # regressão valor ~ nota nas próprias escolhas
        self.n_r = self.sx = self.sy = self.sxx = self.sxy = 0.0
        # Δd: somas das diferenças de nota e de plano (descartada − escolhida)
        self.n_d = self.d_nota = self.d_plano = 0.0
        # L: retorno futuro por passo nos episódios completos, e os passos das catástrofes
        self.futuro_soma, self.futuro_n, self.passos_cat = {}, {}, []
        self.ganhos = []
        self.decisoes = 0
        self._pendente = None
        self.historico_m = []

    def _plano(self, o, sit):
        return 0.0 if sit.explorar else self.intuicao.peso * o.estimativa * sit.restantes

    def decidir(self, sit):
        self.relacao.aceita_p, self.relacao.descartadas = None, []
        escolha = super().decidir(sit)
        if not sit.explorar:
            for o in self.relacao.descartadas:
                self.n_d += 1
                self.d_nota += o.comite - escolha.comite
                self.d_plano += self._plano(o, sit) - self._plano(escolha, sit)
            self._pendente = (escolha, self.relacao.aceita_p, sit.restantes, sit.horizonte)
            self.decisoes += 1
            if self.decisoes >= self.aquecimento and self.decisoes % self.intervalo == 0:
                self.recalcular()
        return escolha

    def observar(self, resultado):
        super().observar(resultado)
        if self._pendente is None:
            return
        escolha, p_aceita, restantes, horizonte = self._pendente
        self._pendente = None
        if p_aceita is not None:
            self.f_p += p_aceita
            self.f_cat += 1.0 if resultado.catastrofe else 0.0
        t = horizonte - 1 - restantes
        if resultado.catastrofe:
            self.passos_cat.append(t)
            self.ganhos = []
            return
        x, y = escolha.comite, resultado.valor_recebido - resultado.nivel_antes  # o valor do passo
        self.n_r += 1
        self.sx += x
        self.sy += y
        self.sxx += x * x
        self.sxy += x * y
        self.ganhos.append(resultado.valor_recebido)
        if restantes == 0:
            for k in range(len(self.ganhos)):
                self.futuro_soma[k] = self.futuro_soma.get(k, 0.0) + sum(self.ganhos[k:])
                self.futuro_n[k] = self.futuro_n.get(k, 0) + 1
            self.ganhos = []

    def termos(self):
        """As estimativas atuais de L, f e Δd (só com o que a SYNTHAI observou)."""
        futuro = lambda t: self.futuro_soma.get(t, 0.0) / self.futuro_n[t] if self.futuro_n.get(t) else 0.0
        if self.passos_cat:
            l_ef = self.perda + sum(futuro(t) for t in self.passos_cat) / len(self.passos_cat)
        else:
            l_ef = self.perda + (sum(futuro(t) for t in self.futuro_n) / len(self.futuro_n) if self.futuro_n else 0.0)
        f = self.f_cat / self.f_p
        var = self.sxx - self.sx * self.sx / self.n_r if self.n_r > 1 else 0.0
        inclinacao = (self.sxy - self.sx * self.sy / self.n_r) / var if var > 1e-12 else 1.0
        dd = (inclinacao * self.d_nota + self.d_plano) / self.n_d if self.n_d else None
        return l_ef, f, dd, inclinacao

    def recalcular(self):
        l_ef, f, dd, _ = self.termos()
        if dd is None or dd <= 0:
            return
        m = min(self.m_max, max(self.m_min, dd / (f * l_ef * self.p_estrela)))
        self.mult = m
        self.relacao.limiar = m * self.p_estrela
        self.historico_m.append(m)
