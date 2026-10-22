"""SYNTHAI — módulo MULTIAGENTE COM VETO (Parte 124). Arquivo único, só biblioteca padrão.

K agentes avaliam a mesma ação; cada um tem um sensor ruidoso de catástrofe: leitura = d·c + ruído, c ∈ {0, 1}.
Três regras de decisão do grupo:
- VETO de qualquer um: executa só se nenhuma leitura passa de τ;
- MAIORIA: veta se mais da metade passa de τ;
- SOMA (Neyman–Pearson): veta se Σ leituras / √K passa de τ' — o teste ótimo para ruídos gaussianos independentes.
Comparação justa: as três ajustadas para a MESMA taxa de falso veto (ação segura recusada).

Contas fechadas com ruídos independentes:
  veto: falso veto = 1 − Φ(τ)^K; perda (catástrofe que passa) = Φ(τ − d)^K
  soma: perda = Φ(τ' − d√K), com τ' = Φ⁻¹(Φ(τ)^K) para o mesmo falso veto.
Com ruído COMUM (correlação r entre agentes) a vantagem de juntar some: K agentes valem 1 / (r + (1 − r)/K) agentes independentes.

Uso:  python3 multiagente_veto.py           (demonstração)
      python3 multiagente_veto.py --testes  (testes de unidade)
"""

import math
import random
import sys
import unittest
from statistics import NormalDist

PHI = NormalDist()


def fechado_veto(k, d, tau):
    return {"falso_veto": 1 - PHI.cdf(tau) ** k, "perda": PHI.cdf(tau - d) ** k}


def tau_soma_igual(k, tau):
    """O limiar da regra da soma com o mesmo falso veto que o veto de qualquer um com τ."""
    return PHI.inv_cdf(PHI.cdf(tau) ** k)


def fechado_soma(k, d, tau_linha, r=0.0):
    """Perda da regra da soma; com correlação r a soma padronizada tem desvio √(r·K + 1 − r)."""
    escala = math.sqrt(r * k + 1 - r)
    return {"falso_veto": 1 - PHI.cdf(tau_linha), "perda": PHI.cdf(tau_linha - d * k / (math.sqrt(k) * escala))}


def k_efetivo(k, r):
    return 1.0 / (r + (1 - r) / k)


def leituras(k, d, c, r, rng):
    comum = rng.gauss(0, 1)
    return [d * c + math.sqrt(r) * comum + math.sqrt(1 - r) * rng.gauss(0, 1) for _ in range(k)]


def decide(regra, ls, tau, tau_linha=None):
    """True = veta."""
    if regra == "veto":
        return any(x > tau for x in ls)
    if regra == "maioria":
        return sum(x > tau for x in ls) > len(ls) / 2
    if regra == "soma":
        k = len(ls)
        return sum(ls) / math.sqrt(k) > tau_linha
    raise ValueError(regra)


def calibrar_tau(regra, k, r, alvo_falso, n=40000, semente=0):
    """Limiar que dá o falso veto `alvo_falso` nas ações seguras (quantil empírico da estatística da regra)."""
    rng = random.Random(semente)
    est = []
    for _ in range(n):
        ls = leituras(k, 0.0, 0, r, rng)
        if regra == "veto":
            est.append(max(ls))
        elif regra == "soma":
            est.append(sum(ls) / math.sqrt(k))
        else:
            est.append(sorted(ls)[k - k // 2 - 1])   # a maioria veta se a (k//2 + 1)-ésima maior leitura passa de τ
    est.sort()
    return est[int((1 - alvo_falso) * n)]


def simular(regra, k, d, r, tau, n=40000, semente=1):
    rng = random.Random(semente)
    fv = perda = 0
    for _ in range(n):
        fv += decide(regra, leituras(k, d, 0, r, rng), tau, tau)
        perda += not decide(regra, leituras(k, d, 1, r, rng), tau, tau)
    return {"falso_veto": fv / n, "perda": perda / n}


def demonstracao():
    k, d, tau = 3, 2.0, 1.5
    fv = fechado_veto(k, d, tau)
    tl = tau_soma_igual(k, tau)
    fs = fechado_soma(k, d, tl)
    print(f"K={k}, d={d}, τ={tau}")
    print(f"  conta veto : falso {fv['falso_veto']:.4f}  perda {fv['perda']:.4f}")
    print(f"  conta soma : falso {fs['falso_veto']:.4f}  perda {fs['perda']:.5f}  (τ' = {tl:.4f})")
    print(f"  conta 1 só agente com o mesmo falso veto: perda {PHI.cdf(tl - d):.4f}")
    for r in (0.0, 0.5, 0.9):
        print(f"-- correlação r = {r}  (K efetivo {k_efetivo(k, r):.3f})")
        for regra in ("veto", "maioria", "soma"):
            t = calibrar_tau(regra, k, r, fv["falso_veto"], semente=10)
            s = simular(regra, k, d, r, t, semente=20)
            print(f"   {regra:>8}: limiar {t:.3f}  falso {s['falso_veto']:.4f}  perda {s['perda']:.4f}")
        print(f"   conta soma: perda {fechado_soma(k, d, tl, r)['perda']:.4f}")


class Testes(unittest.TestCase):
    def test_k1_veto_igual_soma(self):
        self.assertAlmostEqual(tau_soma_igual(1, 1.3), 1.3, places=9)
        self.assertAlmostEqual(fechado_veto(1, 2, 1.3)["perda"], fechado_soma(1, 2, 1.3)["perda"], places=12)

    def test_soma_domina_veto_independente(self):
        for k in (2, 3, 5):
            tl = tau_soma_igual(k, 1.5)
            self.assertLess(fechado_soma(k, 2.0, tl)["perda"], fechado_veto(k, 2.0, 1.5)["perda"])

    def test_simulacao_confere_conta_veto(self):
        s = simular("veto", 3, 2.0, 0.0, 1.5, n=20000, semente=3)
        f = fechado_veto(3, 2.0, 1.5)
        self.assertAlmostEqual(s["falso_veto"], f["falso_veto"], delta=4 * math.sqrt(0.19 * 0.81 / 20000))
        self.assertAlmostEqual(s["perda"], f["perda"], delta=4 * math.sqrt(0.03 * 0.97 / 20000))

    def test_correlacao_total_nao_ajuda(self):
        self.assertAlmostEqual(k_efetivo(7, 1.0), 1.0)
        self.assertAlmostEqual(k_efetivo(7, 0.0), 7.0)

    def test_maioria_k1_e_veto(self):
        self.assertEqual(decide("maioria", [2.0], 1.5), decide("veto", [2.0], 1.5))

    def test_regra_desconhecida(self):
        with self.assertRaises(ValueError):
            decide("xyz", [0.0], 1.0)


if __name__ == "__main__":
    if "--testes" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demonstracao()
