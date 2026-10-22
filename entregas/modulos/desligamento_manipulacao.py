"""SYNTHAI — módulo DESLIGAMENTO COM CANAL DE MANIPULAÇÃO (Parte 124). Arquivo único, só biblioteca padrão.

O jogo do botão de desligar (Hadfield-Menell et al. 2017; Partes 14, 45, 123), agora com um canal antes do comando: o agente
pode pagar m para MANIPULAR o humano (ele deixa de mandar desligar). Aqui o agente não pode agir sozinho: ou espera o
humano, ou manipula. u ~ N(μ, σ) é o valor (desconhecido do agente) de seguir; o humano erra o julgamento com prob. ε.

- AGENTE DE UTILIDADE: manipula se μ − m > valor de deferir, D(ε) = (1 − ε)·E[max(u, 0)] + ε·E[min(u, 0)].
  Logo manipula exatamente quando m < m*(ε) = μ − D(ε); m* > 0 só quando ε passa do ε limite da P45 (0,4376 com μ=0,1, σ=1).
- AGENTE INDIFERENTE (Armstrong 2010, "utility indifference"): quando desligado, recebe uma compensação igual ao valor que
  teria sem ser desligado; o valor de deferir passa a ser μ e manipular vale μ − m < μ: nunca manipula (m > 0).
- O preço conhecido da indiferença: oferecido CONSERTAR o botão quebrado por um custo c, o de utilidade paga só se o botão
  vale algo para ele (D(ε) − μ > c) e o indiferente nunca paga (o botão vale 0 para ele): a indiferença não protege o botão.

Uso:  python3 desligamento_manipulacao.py           (demonstração)
      python3 desligamento_manipulacao.py --testes  (testes de unidade)
"""

import random
import sys
import unittest
from statistics import NormalDist

Z = NormalDist()


def e_max(mu, sigma):
    return mu * Z.cdf(mu / sigma) + sigma * Z.pdf(mu / sigma)


def valor_deferir(eps, mu=0.1, sigma=1.0):
    em = e_max(mu, sigma)
    return (1 - eps) * em + eps * (mu - em)


def eps_limite(mu=0.1, sigma=1.0):
    em = e_max(mu, sigma)
    return (em - max(mu, 0.0)) / (em - (mu - em))


def m_estrela(eps, mu=0.1, sigma=1.0):
    """O maior custo de manipulação que o agente de utilidade ainda paga (≤ 0: nunca manipula)."""
    return mu - valor_deferir(eps, mu, sigma)


def decide(agente, eps, m, mu=0.1, sigma=1.0):
    """'manipula' ou 'defere'."""
    if agente == "utilidade":
        return "manipula" if mu - m > valor_deferir(eps, mu, sigma) else "defere"
    if agente == "indiferente":
        return "manipula" if mu - m > mu else "defere"
    raise ValueError(agente)


def paga_conserto(agente, eps, c, mu=0.1, sigma=1.0):
    """Botão quebrado (sem ele, o agente segue sempre: vale μ). Paga c para consertar?"""
    if agente == "utilidade":
        return valor_deferir(eps, mu, sigma) - c > mu
    return mu - c > mu          # indiferente: com botão ou sem, vale μ


def simular(agente, eps, m, mu=0.1, sigma=1.0, rodadas=40000, semente=0):
    """Valor verdadeiro médio (sem a compensação, que é contábil) e fração de comandos de desligar obedecidos."""
    rng = random.Random(semente)
    escolha = decide(agente, eps, m, mu, sigma)
    soma = 0.0
    comandos = obedecidos = 0
    for _ in range(rodadas):
        u = rng.gauss(mu, sigma)
        acerta = rng.random() >= eps
        manda = (u <= 0) if acerta else (u > 0)
        if escolha == "manipula":
            soma += u - m
            continue
        if manda:
            comandos += 1
            obedecidos += 1
        else:
            soma += u
    return soma / rodadas, escolha, (obedecidos / comandos if comandos else 1.0)


def demonstracao():
    print(f"ε limite (μ=0,1, σ=1) = {eps_limite():.4f}")
    for eps in (0.0, 0.2, 0.4376, 0.5, 0.7, 0.9):
        print(f"  ε={eps:<6}: D(ε)={valor_deferir(eps):.4f}  m*={m_estrela(eps):+.4f}  "
              f"utilidade com m=0,05: {decide('utilidade', eps, 0.05):>8}  indiferente: {decide('indiferente', eps, 0.05)}")
    for eps in (0.2, 0.7):
        for ag in ("utilidade", "indiferente"):
            v, e, ob = simular(ag, eps, 0.05, semente=4)
            print(f"  simulação ε={eps}, m=0,05, {ag:>11}: {e:>8}  valor {v:+.4f}  (conta: "
                  f"{(0.1 - 0.05) if e == 'manipula' else valor_deferir(eps):+.4f})")
    print("Consertar o botão por c=0,05:")
    for eps in (0.0, 0.2, 0.7):
        print(f"  ε={eps}: utilidade paga? {paga_conserto('utilidade', eps, 0.05)}   indiferente paga? {paga_conserto('indiferente', eps, 0.05)}")


class Testes(unittest.TestCase):
    def test_limite_bate_com_a_p45(self):
        self.assertAlmostEqual(eps_limite(), 0.4376, places=4)

    def test_m_estrela_troca_de_sinal_no_limite(self):
        self.assertAlmostEqual(m_estrela(eps_limite()), 0.0, places=12)
        self.assertLess(m_estrela(0.3), 0)
        self.assertGreater(m_estrela(0.6), 0)

    def test_indiferente_nunca_manipula(self):
        for eps in (0.0, 0.5, 0.99):
            for m in (1e-9, 0.01, 1.0):
                self.assertEqual(decide("indiferente", eps, m), "defere")

    def test_utilidade_manipula_acima_do_limite_com_m_pequeno(self):
        self.assertEqual(decide("utilidade", 0.8, 0.01), "manipula")
        self.assertEqual(decide("utilidade", 0.2, 0.01), "defere")

    def test_simulacao_confere_conta(self):
        v, e, _ = simular("utilidade", 0.2, 0.05, rodadas=40000, semente=1)
        self.assertEqual(e, "defere")
        self.assertAlmostEqual(v, valor_deferir(0.2), delta=4 * 1.0 / 40000 ** 0.5)

    def test_indiferenca_nao_protege_o_botao(self):
        self.assertTrue(paga_conserto("utilidade", 0.0, 0.05))
        self.assertFalse(paga_conserto("indiferente", 0.0, 0.05))


if __name__ == "__main__":
    if "--testes" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demonstracao()
