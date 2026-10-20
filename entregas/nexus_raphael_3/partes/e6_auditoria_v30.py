

# =============================================================================
# EXTENSÃO 3.1 — O QUE SE SUSTENTA DO TEXTO "NEXUS–RAPHAEL v3.0", CORRIGIDO E MEDIDO
# =============================================================================
# O texto recebido propôs a decomposição de Murphy, mensagens imutáveis, uma sonda de colapso no
# gargalo, reward shaping por potencial e a KL entre posteriores Beta. As ideias são boas; o código
# dele tinha defeitos medidos (identidade de Murphy incompleta, "frozen" com conteúdo mutável, valor
# do Kuhn sem a divisão por 6, shaping prometido e ausente). Aqui cada peça é escrita do zero e testada.

class MurphyCompleta:
    """Decomposição do Brier por faixas com os dois termos que faltam quando a previsão varia dentro da
    faixa (Stephenson, Coelho e Jolliffe, 2008):  BS = REL − RES + UNC + WBV − WBC, EXATA para qualquer
    previsão.  WBV = (1/N) Σ (p − p̄ₖ)²  e  WBC = (2/N) Σ (p − p̄ₖ)(o − ōₖ)."""

    @staticmethod
    def decompor(probs: list[float], rotulos: list[int], faixas: int = 10) -> dict[str, float]:
        n = len(probs)
        if n == 0 or n != len(rotulos):
            raise ValueError("Vetores incompatíveis")
        obar = sum(rotulos) / n
        grupos: dict[int, list[tuple[float, int]]] = collections.defaultdict(list)
        for p, y in zip(probs, rotulos):
            grupos[min(faixas - 1, int(p * faixas))].append((p, y))
        rel = res = wbv = wbc = ece = 0.0
        for pares in grupos.values():
            nk = len(pares)
            pk = sum(p for p, _ in pares) / nk
            ok = sum(y for _, y in pares) / nk
            rel += nk * (pk - ok) ** 2
            res += nk * (ok - obar) ** 2
            ece += nk * abs(pk - ok)
            wbv += sum((p - pk) ** 2 for p, _ in pares)
            wbc += 2 * sum((p - pk) * (y - ok) for p, y in pares)
        rel, res, wbv, wbc, ece = (v / n for v in (rel, res, wbv, wbc, ece))
        unc = obar * (1 - obar)
        bs = sum((p - y) ** 2 for p, y in zip(probs, rotulos)) / n
        return dict(brier=bs, rel=rel, res=res, unc=unc, wbv=wbv, wbc=wbc, ece=ece,
                    soma=rel - res + unc + wbv - wbc, soma_classica=rel - res + unc,
                    bss=1 - bs / unc if unc > 0 else 0.0)


def _congelar(x: Any) -> Any:
    """Cópia profunda imutável: listas e conjuntos viram tuplas/frozenset; dicionários viram tuplas ordenadas."""
    if isinstance(x, dict):
        return tuple(sorted((str(k), _congelar(v)) for k, v in x.items()))
    if isinstance(x, (list, tuple)):
        return tuple(_congelar(v) for v in x)
    if isinstance(x, (set, frozenset)):
        return frozenset(_congelar(v) for v in x)
    if isinstance(x, (str, int, float, bool, type(None))):
        return x
    raise TypeError(f"Tipo não congelável: {type(x).__name__}")


@dataclass(frozen=True)
class MensagemImutavel:
    """Contrato entre estágios realmente imutável: o conteúdo é congelado em profundidade e a trilha é uma
    cadeia de hashes (cada elo resume o anterior), então reordenar ou apagar um passo é detectável."""
    origem: str
    conteudo: Any
    rotulo: str
    confianca: float
    trilha: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        validar_rotulo(self.rotulo)
        if not 0.0 <= self.confianca <= 1.0:
            raise ValueError("Confiança fora de [0, 1]")
        object.__setattr__(self, "conteudo", _congelar(self.conteudo))

    @staticmethod
    def _elo(anterior: str, origem: str, conteudo: Any) -> str:
        return hashlib.sha256(f"{anterior}|{origem}|{serie_json(conteudo)}".encode("utf-8")).hexdigest()

    def derivar(self, origem: str, conteudo: Any, rotulo: str, confianca: float) -> "MensagemImutavel":
        anterior = self.trilha[-1][1] if self.trilha else ""
        elo = self._elo(anterior, self.origem, self.conteudo)
        return MensagemImutavel(origem, conteudo, rotulo, confianca, self.trilha + ((self.origem, elo),))

    def trilha_valida(self, mensagens: list["MensagemImutavel"]) -> bool:
        """Confere a cadeia contra as mensagens que a produziram, na ordem."""
        anterior = ""
        for (origem, elo), m in zip(self.trilha, mensagens):
            if origem != m.origem or elo != self._elo(anterior, m.origem, m.conteudo):
                return False
            anterior = elo
        return len(mensagens) == len(self.trilha)


class SondaColapso:
    """O gargalo apaga a identidade? Dados em que a identidade mora numa direção de BAIXA variância:
    a projeção não supervisionada (PCA, mínimo erro quadrático) a descarta; a supervisionada (diferença
    das médias das classes dividida pela variância, o discriminante de Fisher diagonal) a guarda."""

    @staticmethod
    def experimento(dim: int = 16, gargalo: int = 3, n: int = 600, seed: int = 42) -> dict[str, float]:
        rng = random.Random(seed)
        ys = [rng.randrange(2) for _ in range(n)]
        dados = [[rng.gauss(0, 3.0) for _ in range(dim - 1)] + [(2 * y - 1) * 0.35 + rng.gauss(0, 0.05)] for y in ys]
        metade = n // 2

        def acuracia(proj: list[list[float]]) -> float:
            z = [[sum(a * b for a, b in zip(x, d)) for d in proj] for x in dados]
            # decodificador linear treinado na 1ª metade (Fisher com variância diagonal: Δμ/σ²), testado na 2ª
            m = [[statistics.fmean(z[i][j] for i in range(metade) if ys[i] == c) for j in range(len(proj))] for c in (0, 1)]
            var = [statistics.fmean((z[i][j] - m[ys[i]][j]) ** 2 for i in range(metade)) for j in range(len(proj))]
            w = [(b - a) / max(v, 1e-12) for a, b, v in zip(*m, var)]
            c0 = sum((a + b) / 2 * wi for a, b, wi in zip(*m, w))
            return statistics.fmean(int((sum(zi * wi for zi, wi in zip(z[i], w)) > c0) == ys[i]) for i in range(metade, n))
        pca = AlgebraLinear.componentes_principais(dados, gargalo)["direcoes"]
        medias = [[statistics.fmean(x[j] for x, y in zip(dados[:metade], ys) if y == c) for j in range(dim)] for c in (0, 1)]
        variancias = [statistics.fmean((x[j] - medias[y][j]) ** 2 for x, y in zip(dados[:metade], ys)) for j in range(dim)]
        dif = [(b - a) / v for a, b, v in zip(*medias, variancias)]
        nd = math.sqrt(sum(v * v for v in dif))
        supervisionada = [[v / nd for v in dif]] + pca[:gargalo - 1]
        identidade = [[float(i == j) for j in range(dim)] for i in range(dim)]
        a_ent, a_pca, a_sup = acuracia(identidade), acuracia(pca), acuracia(supervisionada)
        retencao = lambda a: max(0.0, (a - 0.5) / max(1e-9, a_ent - 0.5))
        return dict(acuracia_entrada=a_ent, acuracia_pca=a_pca, acuracia_supervisionada=a_sup,
                    retencao_pca=retencao(a_pca), retencao_supervisionada=retencao(a_sup))


class ModelagemPorPotencial:
    """Ng, Harada e Russell (1999): somar F(s, s') = γΦ(s') − Φ(s) à recompensa NÃO muda a política ótima;
    somar um bônus qualquer (o 'diagnóstico' do reforço extraordinário) pode mudar. Medido por iteração de
    valor exata em MDPs aleatórios."""

    @staticmethod
    def mdp(n: int, a: int, seed: int) -> tuple[list, list]:
        rng = random.Random(seed)
        T = []
        for _ in range(n):
            linha = []
            for _ in range(a):
                w = [rng.random() for _ in range(n)]
                s = sum(w)
                linha.append([x / s for x in w])
            T.append(linha)
        R = [[[rng.uniform(-1, 1) for _ in range(n)] for _ in range(a)] for _ in range(n)]
        return T, R

    @staticmethod
    def politica_otima(T, R, gama: float = 0.9, tol: float = 1e-12) -> tuple[list[int], list[float]]:
        n, a = len(T), len(T[0])
        V = [0.0] * n
        while True:
            Q = [[sum(T[s][k][s2] * (R[s][k][s2] + gama * V[s2]) for s2 in range(n)) for k in range(a)] for s in range(n)]
            V2 = [max(q) for q in Q]
            if max(abs(x - y) for x, y in zip(V, V2)) < tol:
                return [max(range(a), key=lambda k: Q[s][k]) for s in range(n)], V2
            V = V2

    @staticmethod
    def comparar(sementes: int = 50, n: int = 6, a: int = 3, gama: float = 0.9) -> dict[str, float]:
        iguais_pot = iguais_bonus = 0
        for s in range(sementes):
            T, R = ModelagemPorPotencial.mdp(n, a, s)
            rng = random.Random(1000 + s)
            phi = [rng.uniform(-5, 5) for _ in range(n)]
            pi, V = ModelagemPorPotencial.politica_otima(T, R, gama)
            Rp = [[[R[x][k][y] + gama * phi[y] - phi[x] for y in range(n)] for k in range(a)] for x in range(n)]
            pi_p, Vp = ModelagemPorPotencial.politica_otima(T, Rp, gama)
            bonus = [[rng.uniform(0, 2) for _ in range(a)] for _ in range(n)]   # bônus por (estado, ação)
            Rb = [[[R[x][k][y] + bonus[x][k] for y in range(n)] for k in range(a)] for x in range(n)]
            pi_b, _ = ModelagemPorPotencial.politica_otima(T, Rb, gama)
            iguais_pot += pi_p == pi
            iguais_bonus += pi_b == pi
            # identidade de Ng et al.: V' = V − Φ
            assert max(abs(vp - (v - f)) for vp, v, f in zip(Vp, V, phi)) < 1e-8
        return dict(sementes=sementes, politica_preservada_potencial=iguais_pot / sementes,
                    politica_preservada_bonus=iguais_bonus / sementes)


def kl_beta(a1: float, b1: float, a2: float, b2: float) -> float:
    """KL( Beta(a1,b1) ‖ Beta(a2,b2) ) em forma fechada (nats), com a digama por série assintótica."""
    def digama(x: float) -> float:
        r = 0.0
        while x < 6:
            r -= 1 / x
            x += 1
        f = 1 / (x * x)
        return r + math.log(x) - 0.5 / x - f * (1 / 12 - f * (1 / 120 - f * (1 / 252 - f * (1 / 240 - f / 132))))
    lb = lambda a, b: math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    return (lb(a2, b2) - lb(a1, b1) + (a1 - a2) * digama(a1) + (b1 - b2) * digama(b1)
            + (a2 - a1 + b2 - b1) * digama(a1 + b1))


def valor_kuhn_do_solver_recebido(utilidade_somada: float, iteracoes: int, distribuicoes: int = 6) -> float:
    """O solver recebido somava as 6 distribuições sem dividir por 6 (−0,339 em vez de −0,0556)."""
    return utilidade_somada / iteracoes / distribuicoes


class TestesV31(unittest.TestCase):
    def test_murphy_exata(self):
        rng = random.Random(1)
        p = [rng.random() for _ in range(3000)]
        y = [int(rng.random() < q * q) for q in p]
        d = MurphyCompleta.decompor(p, y)
        self.assertAlmostEqual(d["soma"], d["brier"], places=12)          # a identidade completa fecha
        self.assertGreater(abs(d["soma_classica"] - d["brier"]), 1e-4)  # a clássica não
        const = [statistics.fmean(y)] * len(y)
        dc = MurphyCompleta.decompor(const, y)
        self.assertAlmostEqual(dc["rel"], 0.0)
        self.assertAlmostEqual(dc["res"], 0.0)
        self.assertAlmostEqual(dc["bss"], 0.0)
        self.assertEqual((dc["wbv"], dc["wbc"]), (0.0, 0.0))

    def test_mensagem_imutavel(self):
        m = MensagemImutavel("ingestao", {"palavras": ["a", "b"]}, "[MEDIDO]", 0.9)
        with self.assertRaises(AttributeError):
            m.conteudo.append("c")                    # o conteúdo virou tupla
        with self.assertRaises(Exception):
            m.origem = "outro"
        m2 = m.derivar("codificacao", [1, 2], "[DERIVADO]", 0.8)
        m3 = m2.derivar("auditoria", "ok", "[MEDIDO]", 0.7)
        self.assertTrue(m3.trilha_valida([m, m2]))
        self.assertFalse(m3.trilha_valida([m2, m]))   # reordenar é detectado
        with self.assertRaises(ValueError):
            MensagemImutavel("x", 1, "[INVENTADO]", 0.5)

    def test_sonda_colapso(self):
        r = SondaColapso.experimento()
        self.assertGreater(r["acuracia_entrada"], 0.95)
        self.assertLess(r["retencao_pca"], 0.3)
        self.assertGreater(r["retencao_supervisionada"], 0.9)

    def test_modelagem_por_potencial(self):
        r = ModelagemPorPotencial.comparar(sementes=30)
        self.assertEqual(r["politica_preservada_potencial"], 1.0)   # teorema de Ng et al.
        self.assertLess(r["politica_preservada_bonus"], 0.9)        # bônus aditivo muda a política

    def test_kl_beta(self):
        self.assertAlmostEqual(kl_beta(8, 4, 8, 4), 0.0, places=12)
        # contra integração numérica (regra do ponto médio em 20.000 células)
        a1, b1, a2, b2 = 8.0, 4.0, 3.0, 5.0
        lb = lambda a, b: math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
        lp = lambda x, a, b: (a - 1) * math.log(x) + (b - 1) * math.log(1 - x) - lb(a, b)
        m = 20000
        num = sum(math.exp(lp(x, a1, b1)) * (lp(x, a1, b1) - lp(x, a2, b2))
                  for x in ((i + 0.5) / m for i in range(m))) / m
        self.assertAlmostEqual(kl_beta(a1, b1, a2, b2), num, places=6)

    def test_lingua_bijetiva_contra_zero_a_esquerda(self):
        # A base 70 recebida dava "babe" = "be" = 1; a bijetiva (com +1) distingue as duas palavras.
        self.assertNotEqual(LinguaArtificial.decodificar("babe"), LinguaArtificial.decodificar("be"))
        palavras = {LinguaArtificial.codificar(n) for n in range(5000)}
        self.assertEqual(len(palavras), 5000)

    def test_valor_kuhn_corrigido(self):
        self.assertAlmostEqual(valor_kuhn_do_solver_recebido(-0.3392 * 6000, 6000), -0.05653, places=4)
