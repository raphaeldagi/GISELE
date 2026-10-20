class TestesExtensao(unittest.TestCase):
    """Testes da 3.0.0. Cada um confere uma peça contra um número de forma fechada, um teorema
    ou um caminho de cálculo independente (nunca contra a própria saída gravada)."""

    # ---------- correções ----------
    def test_sem_rede(self):
        import ast
        arvore = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        proibidos = {"urllib", "socket", "http", "requests", "subprocess", "ftplib", "smtplib"}
        for no in ast.walk(arvore):
            if isinstance(no, ast.Import):
                self.assertFalse({a.name.split(".")[0] for a in no.names} & proibidos)
            if isinstance(no, ast.ImportFrom):
                self.assertNotIn((no.module or "").split(".")[0], proibidos)
            if isinstance(no, ast.Call) and isinstance(no.func, ast.Name):
                self.assertNotIn(no.func.id, {"eval", "exec", "__import__"})
        self.assertFalse(hasattr(LagoLexical, "_consultar_api"))

    def test_rede_recusada(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            repo = Repositorio(Configuracao(raiz=d))
            with self.assertRaises(ValueError):
                LagoLexical(repo, permitir_rede=True)

    def test_bootstrap_qualquer_numero_de_replicas(self):
        # Na 2.2.0, replicas[974] estourava com 500 réplicas.
        dados = [float(i % 7) for i in range(50)]
        for r in (10, 500, 1000, 2000):
            m, inf, sup = AvaliadorProbabilistico.bootstrap_ganho(dados, [0.0] * 50, 3, r)
            self.assertLessEqual(inf, m)
            self.assertLessEqual(m, sup)
        m, inf, sup = Estatistica.bootstrap_media(dados, 1, 500)
        self.assertLess(inf, m)
        self.assertLess(m, sup)

    def test_quantil_tipo7(self):
        self.assertEqual(Estatistica.quantil([1, 2, 3, 4], 0.5), 2.5)
        self.assertEqual(Estatistica.quantil([5], 0.9), 5)
        self.assertAlmostEqual(Estatistica.quantil(list(range(101)), 0.025), 2.5)

    def test_qui2_megasena_fator(self):
        # Simulação independente da média de Σ(c−e)²/e: o fator 54/59 vem de 60·(1 − 6/60).
        rng = random.Random(11)
        valores = []
        for _ in range(300):
            c = collections.Counter(x for _ in range(200) for x in rng.sample(range(1, 61), 6))
            valores.append(sum((c[x] - 20) ** 2 / 20 for x in range(1, 61)))
        m = statistics.fmean(valores)
        dp = statistics.stdev(valores) / math.sqrt(len(valores))
        self.assertLess(abs(m - 54) / dp, 3.5)
        self.assertGreater(abs(m - 59) / dp, 3.5)

    def test_megasena_corrigida(self):
        r = ExperimentosCorrigidos.megasena(1200, 42, 500)
        self.assertTrue(0 < r["p_valor"] < 1)
        self.assertLessEqual(r["ic95_bootstrap"][0], r["media_delta"])
        self.assertLessEqual(r["media_delta"], r["ic95_bootstrap"][1])
        self.assertTrue(r["ic95_bootstrap"][0] < 0 < r["ic95_bootstrap"][1])
        self.assertTrue(r["veredito"].startswith("INCONCLUSIVA"))

    def test_beta_intervalo_exato(self):
        b = BetaBernoulli()
        b.observar(1)
        b.observar(1)
        lo, hi = b.intervalo_exato()
        # Beta(3,1): F(x) = x³, logo os quantis são 0,025^(1/3) e 0,975^(1/3).
        self.assertAlmostEqual(lo, 0.025 ** (1 / 3), places=9)
        self.assertAlmostEqual(hi, 0.975 ** (1 / 3), places=9)
        self.assertLess(hi, 1.0)

    def test_h_m3_combinado(self):
        r = ExperimentosCorrigidos.h_m3(1500, [0, 1, 2], 300)
        self.assertEqual(r["seeds"], 3)
        lo, hi = r["ic95_combinado"]
        self.assertTrue(lo < r["ganho_combinado"] < hi)
        # Ganho de Brier teórico: Var global − Var condicional = 0,25 − 0,1275 = 0,1225.
        self.assertTrue(lo < 0.1225 < hi + 0.01)

    def test_h_m7_muitas_sementes(self):
        r = ExperimentosCorrigidos.h_m7(60)
        self.assertEqual(r["seeds"], 60)
        self.assertGreater(r["t_pareado"]["p_bilateral"], 0.01)

    # ---------- estatística ----------
    def test_distribuicoes(self):
        self.assertAlmostEqual(Estatistica.qui2_sf(3.841458820694124, 1), 0.05, places=10)
        self.assertAlmostEqual(Estatistica.t_quantil(0.975, 10), 2.2281388519649, places=8)
        self.assertAlmostEqual(Estatistica.normal_quantil(0.975), 1.959963984540054, places=9)
        self.assertAlmostEqual(Estatistica.gama_inferior_regularizada(1, 2), 1 - math.exp(-2), places=12)
        # Beta(2,5) em 0,3: I = Σ_{j=2}^{6} C(6,j) 0,3^j 0,7^(6−j).
        exato = sum(math.comb(6, j) * .3 ** j * .7 ** (6 - j) for j in range(2, 7))
        self.assertAlmostEqual(Estatistica.beta_regularizada(.3, 2, 5), exato, places=12)
        self.assertAlmostEqual(Estatistica.t_cdf(0.0, 7), 0.5, places=12)

    def test_intervalos_binomiais(self):
        lo, hi = Estatistica.clopper_pearson(0, 10)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 1 - 0.025 ** 0.1, places=9)
        lo, hi = Estatistica.wilson(7, 10)
        self.assertTrue(lo < 0.7 < hi)
        lo2, hi2 = Estatistica.clopper_pearson(7, 10)
        self.assertLess(lo2, lo)  # o exato é conservador
        self.assertGreater(hi2, hi)

    def test_testes_de_hipotese(self):
        self.assertEqual(Estatistica.binomial_exato(5, 10), 1.0)
        self.assertAlmostEqual(Estatistica.binomial_exato(0, 10), 2 / 1024)
        r = Estatistica.t_pareado([1, 2, 3, 4], [0, 1, 2, 3.5])
        self.assertAlmostEqual(r["media"], 0.875)
        self.assertEqual(Estatistica.holm({"a": .01, "b": .04, "c": .03}), {"a": True, "c": False, "b": False})
        # Doze diferenças iguais: só os 2 sinais uniformes de 2¹² empatam com o observado (p exato 1/2048).
        p = Estatistica.permutacao_pareada([1.0] * 12, [0.0] * 12, 2, 2000)
        self.assertLess(p, 0.01)
        self.assertEqual(Estatistica.sinal([1, -1, 0, 2])["empates"], 1)
        q = Estatistica.qui2_uniformidade([10, 10, 10, 10])
        self.assertEqual(q["estatistica"], 0.0)
        self.assertAlmostEqual(q["p_valor"], 1.0)

    # ---------- álgebra linear ----------
    def test_algebra(self):
        a = [[2, 1, 0], [1, 3, 1], [0, 1, 4]]
        self.assertAlmostEqual(AlgebraLinear.determinante(a), 18.0)
        inv = AlgebraLinear.inversa(a)
        prod = AlgebraLinear.produto(a, inv)
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(prod[i][j], float(i == j), places=12)
        x = AlgebraLinear.resolver(a, [1, 2, 3])
        self.assertTrue(all(abs(u - v) < 1e-12 for u, v in zip(AlgebraLinear.aplicar(a, x), [1, 2, 3])))
        coef = AlgebraLinear.minimos_quadrados([[1, t] for t in range(5)], [1 + 2 * t for t in range(5)])
        self.assertAlmostEqual(coef[0], 1.0)
        self.assertAlmostEqual(coef[1], 2.0)
        ridge = AlgebraLinear.minimos_quadrados([[1, t] for t in range(5)], [1 + 2 * t for t in range(5)], 10.0)
        self.assertLess(abs(ridge[1]), 2.0)

    def test_autovalores(self):
        valores, _ = AlgebraLinear.jacobi([[2, 1], [1, 2]])
        self.assertEqual([round(v, 12) for v in sorted(valores)], [1.0, 3.0])
        self.assertAlmostEqual(AlgebraLinear.potencia([[2, 1], [1, 2]])[0], 3.0)
        # [[3,0],[4,5]]: AᵀA = [[25,20],[20,25]], autovalores 45 e 5.
        sv = AlgebraLinear.valores_singulares([[3, 0], [4, 5]])
        self.assertAlmostEqual(sv[0], math.sqrt(45))
        self.assertAlmostEqual(sv[1], math.sqrt(5))
        q, r = AlgebraLinear.gram_schmidt([[1, 1], [1, 0], [0, 1]])
        qtq = AlgebraLinear.produto(AlgebraLinear.transposta(q), q)
        self.assertAlmostEqual(qtq[0][1], 0.0)
        self.assertAlmostEqual(qtq[1][1], 1.0)

    def test_pca(self):
        rng = random.Random(4)
        dados = []
        for _ in range(400):
            t = rng.gauss(0, 3)
            dados.append([t, 2 * t + rng.gauss(0, .1), rng.gauss(0, .1)])
        r = AlgebraLinear.componentes_principais(dados, 1)
        self.assertGreater(r["fracao_explicada"], 0.99)
        d = r["direcoes"][0]
        self.assertAlmostEqual(abs(d[1] / d[0]), 2.0, places=2)

    # ---------- calibração, bandidos, informação, texto, dinâmica ----------
    def test_calibracao(self):
        r = Calibracao.experimento()
        self.assertLess(r["ece_isotonica"], r["ece_antes"] / 3)
        self.assertLess(r["ece_platt"], r["ece_antes"] / 3)
        self.assertLess(r["brier_isotonica"], r["brier_antes"])
        degraus = Calibracao.isotonica([.1, .2, .3, .4], [0, 1, 0, 1])
        valores = [v for _, v in degraus]
        self.assertEqual(valores, sorted(valores))

    def test_bandidos(self):
        r = Bandidos.comparar(sementes=range(12), passos=1500)
        m = r["medias_arrependimento"]
        self.assertLess(m["thompson"], m["epsilon"])
        self.assertLess(m["thompson"], m["ucb1"])
        # c = Σ Δ/KL para (0,75; 0,55; 0,50): conta de Lai–Robbins.
        kl = lambda p, q: p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))
        self.assertAlmostEqual(Bandidos.lai_robbins([.75, .55, .5]), .2 / kl(.55, .75) + .25 / kl(.5, .75))

    def test_informacao(self):
        self.assertAlmostEqual(Informacao.entropia([.5, .5]), 1.0)
        self.assertAlmostEqual(Informacao.kl([.3, .7], [.3, .7]), 0.0)
        self.assertGreater(Informacao.kl([.3, .7], [.5, .5]), 0)
        self.assertEqual(Informacao.levenshtein("kitten", "sitting"), 3)
        pares = [(i % 2, i % 2) for i in range(100)]
        self.assertAlmostEqual(Informacao.informacao_mutua(pares), 1.0)
        self.assertAlmostEqual(Informacao.informacao_mutua([(i % 2, i // 2 % 2) for i in range(100)]), 0.0, places=2)
        self.assertEqual(Informacao.jaccard({1, 2}, {2, 3}), 1 / 3)

    def test_modelo_de_caracteres(self):
        texto = " ".join(d for _, _, d in lexico_embutido())
        corte = len(texto) * 4 // 5
        m = ModeloCaracteres(3).treinar(texto[:corte])
        bpc = m.bits_por_caractere(texto[corte:])
        self.assertLess(bpc, math.log2(len(set(texto))) - 1)  # aprende alguma coisa fora da amostra
        self.assertGreater(bpc, 1.0)
        # A uniforme da base reparte a massa entre o alfabeto e UM símbolo não visto: soma exata 1.
        self.assertNotIn("\x00", m.alfabeto)
        self.assertAlmostEqual(sum(m.prob("the", c) for c in m.alfabeto) + m.prob("the", "\x00"), 1.0, places=12)
        self.assertEqual(len(m.gerar(50, 1)), 50)

    def test_dinamica(self):
        x = Dinamica.rk4(lambda v: [-v[0]], [1.0], 0.01, 100)[-1][0]
        self.assertLess(abs(x - math.exp(-1)), 1e-9)
        self.assertEqual([Dinamica.periodo_logistico(r) for r in (2.8, 3.2, 3.5, 3.55)], [1, 2, 4, 8])
        self.assertIsNone(Dinamica.periodo_logistico(3.9))
        dobras = Dinamica.feigenbaum()
        self.assertAlmostEqual(dobras[0], 3.0, places=2)
        self.assertAlmostEqual(dobras[1], 1 + math.sqrt(6), places=2)
        self.assertTrue(4.3 < (dobras[1] - dobras[0]) / (dobras[2] - dobras[1]) < 5.0)
        lam = Dinamica.lyapunov_benettin(Dinamica.lorenz(), [1.0, 1.0, 1.0], passos=5000)
        self.assertTrue(0.75 < lam < 1.05)  # literatura: 0,9056

    # ---------- jogos ----------
    def test_regras_kuhn_e_leduc(self):
        self.assertEqual(AnaliseJogo.conjuntos(JogoKuhn), (6, 6))
        self.assertEqual(AnaliseJogo.conjuntos(JogoLeduc), (144, 144))
        self.assertEqual(len(JogoLeduc.DISTRIBUICOES), 120)
        self.assertEqual(JogoLeduc.terminal("rf", 0, 1, 2), 1.0)
        self.assertEqual(JogoLeduc.terminal("cc/rc", 0, 1, 0), 5.0)  # o jogador 1 pareou com a pública
        self.assertEqual(JogoLeduc.terminal("cc/cc", 1, 1, 0), 0.0)
        self.assertEqual(JogoLeduc.contribuicoes("rrc/rrc"), [13, 13])  # 1 + 2 + 2 + 4 + 4
        for c in range(3):
            for d in range(3):
                if c != d:
                    self.assertEqual(JogoKuhn.terminal("pbb", c, d), PokerKuhn.premio((c, d), "kbc"))

    def test_kuhn_cfr_equilibrio(self):
        cfr = CFR(JogoKuhn).vanilla(2000)
        perfil = cfr.media()
        self.assertLess(abs(AnaliseJogo.valor(JogoKuhn, perfil) + 1 / 18), 2e-3)
        self.assertLess(AnaliseJogo.explorabilidade(JogoKuhn, perfil), 0.02)
        # Jogador 2 único em Kuhn: com a dama paga 1/3 da aposta; com o valete blefa 1/3 após passe.
        self.assertAlmostEqual(perfil[(1, "b")][1], 1 / 3, delta=0.03)
        self.assertAlmostEqual(perfil[(0, "p")][1], 1 / 3, delta=0.03)

    def test_kuhn_mccfr(self):
        externo = CFR(JogoKuhn).amostragem_externa(20000, 1)
        acaso = CFR(JogoKuhn).acaso_amostrado(20000, 1)
        self.assertLess(AnaliseJogo.explorabilidade(JogoKuhn, externo.media()), 0.03)
        self.assertLess(AnaliseJogo.explorabilidade(JogoKuhn, acaso.media()), 0.03)
        self.assertEqual(acaso.nos, 20000 * 9)  # 9 nós por árvore de uma distribuição

    def test_estrategia_fixa_2_2_0_e_exploravel(self):
        fixa = AnaliseJogo.estrategia_fixa_kuhn_2_2_0()
        self.assertGreater(AnaliseJogo.explorabilidade(JogoKuhn, fixa), 0.3)
        self.assertAlmostEqual(AnaliseJogo.explorabilidade(JogoKuhn, {}), 11 / 12)

    def test_simplex(self):
        r = Simplex.resolver_jogo([[1, -1], [-2, 3]])
        from fractions import Fraction as F
        self.assertEqual(r["valor"], F(1, 7))
        self.assertEqual(r["linhas"], [F(5, 7), F(2, 7)])
        self.assertEqual(r["colunas"], [F(4, 7), F(3, 7)])
        valor, x, _ = Simplex.maximizar([[1, 1], [1, 3]], [4, 6], [3, 2])
        self.assertEqual((valor, x), (F(12), [F(4), F(0)]))
        self.assertEqual(Simplex.resolver_jogo(Simplex.kuhn_forma_normal())["valor"], F(-1, 18))

    def test_leduc_cfr_melhora(self):
        uniforme = AnaliseJogo.explorabilidade(JogoLeduc, {})
        cfr = CFR(JogoLeduc).vanilla(20)
        depois = AnaliseJogo.explorabilidade(JogoLeduc, cfr.media())
        self.assertLess(depois, uniforme / 5)
        self.assertEqual(cfr.nos, 20 * 10200)

    def test_velha(self):
        self.assertEqual(VelhaAvancada.alfa_beta(), valor_velha("." * 9))
        self.assertEqual(VelhaAvancada.estados_por_camadas(), contar_estados_velha())
        aprendida = VelhaAvancada.treinar_q(20000, 3)
        livres = lambda t: [i for i, c in enumerate(t) if c == "."]
        rng = random.Random(9)
        aleatoria = VelhaAvancada.avaliar(lambda t: rng.choice(livres(t)), 1000, 4)
        self.assertGreater(aprendida["vitorias"], aleatoria["vitorias"] + 0.15)
        self.assertLess(aprendida["derrotas"], 0.05)

    # ---------- lógica e codificação ----------
    def test_dpll_concorda_com_tabela_verdade(self):
        rng = random.Random(5)
        contagem = collections.Counter()
        for _ in range(150):
            fs = [LogicaSAT.formula_aleatoria(rng, 4, 3) for _ in range(3)]
            a = Logica.satisfativel(fs)["estado"]
            self.assertEqual(LogicaSAT.satisfativel(fs)["estado"], a)
            contagem[a] += 1
        self.assertGreater(contagem["CONSISTENTE"], 10)
        self.assertGreater(contagem["CONTRADITORIO"], 10)

    def test_sat_alem_de_16_variaveis(self):
        cadeia = " & ".join(f"(x{i} -> x{i + 1})" for i in range(40))
        self.assertEqual(Logica.satisfativel([cadeia, "x0"])["estado"], "INCONCLUSIVO")
        self.assertEqual(LogicaSAT.satisfativel([cadeia, "x0"])["estado"], "CONSISTENTE")
        self.assertEqual(LogicaSAT.satisfativel([cadeia, "x0", "!x40"])["estado"], "CONTRADITORIO")
        for n in (3, 4, 5):
            self.assertFalse(LogicaSAT.dpll(LogicaSAT.pombos(n))["satisfativel"])
        self.assertTrue(LogicaSAT.dpll([[1, 2], [-1, 2], [-2, 3]])["satisfativel"])

    def test_transicao_3sat(self):
        r = LogicaSAT.transicao_3sat(25, [2.0, 8.0], 20, 1)
        self.assertEqual(r[2.0], 1.0)
        self.assertEqual(r[8.0], 0.0)

    def test_codificacoes_numericas(self):
        import zlib
        for palavra in ("a", "z", "aa", "logic", "zz", "dictionary"):
            self.assertEqual(CodificacaoNumerica.de_base26(CodificacaoNumerica.base26_bijetiva(palavra)), palavra)
        self.assertEqual(CodificacaoNumerica.base26_bijetiva("aa"), 27)
        self.assertEqual([CodificacaoNumerica.de_base26(n) for n in range(1, 30)],
                         sorted([CodificacaoNumerica.de_base26(n) for n in range(1, 30)], key=lambda s: (len(s), s)))
        for dados in (b"", b"123456789", "olá".encode()):
            self.assertEqual(CodificacaoNumerica.crc32(dados), zlib.crc32(dados))

    def test_hamming_corrige_um_bit(self):
        for n in range(16):
            w = CodificacaoNumerica.hamming74_codificar(n)
            self.assertEqual(CodificacaoNumerica.hamming74_decodificar(w), (n, 0))
            for b in range(7):
                self.assertEqual(CodificacaoNumerica.hamming74_decodificar(w ^ (1 << b)), (n, b + 1))

    def test_compressao(self):
        texto = " ".join(d for _, _, d in lexico_embutido())
        h = CodificacaoNumerica.huffman(texto)
        self.assertTrue(h["entropia"] <= h["media"] < h["entropia"] + 1)
        self.assertEqual(CodificacaoNumerica.huffman_decodificar(h["bits"], h["codigos"]), texto)
        pares = CodificacaoNumerica.lz78(texto)
        self.assertEqual(CodificacaoNumerica.lz78_decodificar(pares), texto)
        self.assertLess(len(pares), len(texto) / 3)


def _cmd_kuhn(modo: str) -> dict[str, Any]:
    n = {"rapido": 2000, "padrao": 10000, "intensivo": 50000}[modo]
    from fractions import Fraction as F
    saida = dict(versao=VERSAO, valor_exato_simplex=str(Simplex.resolver_jogo(Simplex.kuhn_forma_normal())["valor"]),
                 explorabilidade_estrategia_2_2_0=AnaliseJogo.explorabilidade(JogoKuhn, AnaliseJogo.estrategia_fixa_kuhn_2_2_0()))
    for nome, cfr in (("vanilla", CFR(JogoKuhn).vanilla(n)),
                      ("acaso", CFR(JogoKuhn).acaso_amostrado(n * 6, 1)),
                      ("externo", CFR(JogoKuhn).amostragem_externa(n * 3, 1))):
        p = cfr.media()
        saida[nome] = dict(nos=cfr.nos, valor=AnaliseJogo.valor(JogoKuhn, p),
                           explorabilidade=AnaliseJogo.explorabilidade(JogoKuhn, p),
                           dama_paga=p[(1, "b")][1], valete_blefa=p[(0, "p")][1])
    saida["valor_teorico"] = float(F(-1, 18))
    saida["rotulo"] = "[MEDIDO]"
    return saida


def _cmd_leduc(modo: str) -> dict[str, Any]:
    n = {"rapido": 30, "padrao": 200, "intensivo": 1000}[modo]
    cfr = CFR(JogoLeduc).vanilla(n)
    p = cfr.media()
    return dict(versao=VERSAO, iteracoes=n, nos=cfr.nos, conjuntos=AnaliseJogo.conjuntos(JogoLeduc),
                explorabilidade_uniforme=AnaliseJogo.explorabilidade(JogoLeduc, {}),
                explorabilidade=AnaliseJogo.explorabilidade(JogoLeduc, p),
                valor_jogador_1=AnaliseJogo.valor(JogoLeduc, p), rotulo="[MEDIDO]")


def _cmd_velha(modo: str) -> dict[str, Any]:
    n = {"rapido": 20000, "padrao": 100000, "intensivo": 400000}[modo]
    return dict(versao=VERSAO, valor_alfa_beta=VelhaAvancada.alfa_beta(),
                estados=VelhaAvancada.estados_por_camadas(), q_learning=VelhaAvancada.treinar_q(n, 3),
                rotulo="[MEDIDO]")


def _cmd_sat(modo: str) -> dict[str, Any]:
    nvar = {"rapido": 25, "padrao": 40, "intensivo": 60}[modo]
    razoes = [2.0, 3.0, 3.5, 4.0, 4.27, 4.5, 5.0, 6.0, 8.0]
    pombos = {n: LogicaSAT.dpll(LogicaSAT.pombos(n))["decisoes"] for n in range(2, 7)}
    return dict(versao=VERSAO, variaveis=nvar, fracao_satisfativel=LogicaSAT.transicao_3sat(nvar, razoes, 30, 1),
                decisoes_casa_dos_pombos=pombos, rotulo="[MEDIDO]")


def _cmd_calibracao(modo: str) -> dict[str, Any]:
    return dict(versao=VERSAO, **Calibracao.experimento(n={"rapido": 3000, "padrao": 20000, "intensivo": 100000}[modo]))


def _cmd_bandidos(modo: str) -> dict[str, Any]:
    s = {"rapido": 30, "padrao": 100, "intensivo": 300}[modo]
    r = Bandidos.comparar(sementes=range(s))
    r["lai_robbins_c"] = Bandidos.lai_robbins([.75, .55, .5])
    r["cota_assintotica_2000"] = r["lai_robbins_c"] * math.log(2000)
    return dict(versao=VERSAO, **r)


def _cmd_megasena3(modo: str) -> dict[str, Any]:
    n = {"rapido": 1200, "padrao": 2900, "intensivo": 10000}[modo]
    return dict(versao=VERSAO, origem="[SINTÉTICO]", **ExperimentosCorrigidos.megasena(n, 42, 2000),
                h_m3=ExperimentosCorrigidos.h_m3(1500, list(range(5))),
                h_m7=ExperimentosCorrigidos.h_m7({"rapido": 200, "padrao": 1000, "intensivo": 5000}[modo]))


def _cmd_caos(modo: str) -> dict[str, Any]:
    passos = {"rapido": 5000, "padrao": 20000, "intensivo": 100000}[modo]
    dobras = Dinamica.feigenbaum()
    razoes = [(dobras[i + 1] - dobras[i]) / (dobras[i + 2] - dobras[i + 1]) for i in range(len(dobras) - 2)]
    return dict(versao=VERSAO, lyapunov_lorenz=Dinamica.lyapunov_benettin(Dinamica.lorenz(), [1.0, 1.0, 1.0], passos=passos),
                lyapunov_logistico_r4=Geometria.lyapunov_logistico(4.0), ln2=math.log(2),
                dobras_de_periodo=dobras, razoes_feigenbaum=razoes, rotulo="[MEDIDO]")


COMANDOS_3 = dict(kuhn=_cmd_kuhn, leduc=_cmd_leduc, velha=_cmd_velha, sat=_cmd_sat, calibracao=_cmd_calibracao,
                  bandidos=_cmd_bandidos, megasena3=_cmd_megasena3, caos=_cmd_caos)
