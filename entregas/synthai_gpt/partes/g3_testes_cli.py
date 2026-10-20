

class TestesGPT(unittest.TestCase):
    """Testes do motor GPT: gradiente, causalidade, normalização, otimizador, tokenizadores, amostragem, pesos."""

    def _modelo(self, **kw):
        cfg = ConfigGPT(**dict(dict(vocab=7, contexto=6, d=8, camadas=2, cabecas=2, semente=3), **kw))
        m = ModeloGPT(cfg)
        r = random.Random(1)
        for linhas in m.p.values():          # todos os termos diferentes de zero (regra da Parte 30)
            for l in linhas:
                for j in range(len(l)):
                    l[j] += r.gauss(0, 0.3)
        return m

    def test_gradiente_por_diferencas_finitas(self):
        m = self._modelo()
        x, y = [1, 4, 2, 6, 0, 3], [4, 2, 6, 0, 3, 5]
        G = m.zeros()
        m.gradiente(x, y, G)
        pior = 0.0
        for k in m.p:
            for i in range(len(m.p[k])):
                for j in range(len(m.p[k][i])):
                    o = m.p[k][i][j]
                    m.p[k][i][j] = o + 1e-5
                    a = m.perda(x, y)
                    m.p[k][i][j] = o - 1e-5
                    b = m.perda(x, y)
                    m.p[k][i][j] = o
                    pior = max(pior, abs((a - b) / 2e-5 - G[k][i][j]))
        self.assertLess(pior, 1e-7)

    def test_contagem_de_parametros(self):
        for kw in (dict(), dict(camadas=1), dict(d=12, cabecas=3, contexto=5)):
            m = self._modelo(**kw)
            self.assertEqual(m.contar(), m.cfg.parametros())

    def test_causalidade(self):
        m = self._modelo()
        a, _ = m.adiante([1, 2, 3, 4, 5, 6], guardar=False)
        b, _ = m.adiante([1, 2, 3, 0, 0, 0], guardar=False)
        for t in range(3):
            self.assertEqual(a[t], b[t])          # o futuro não muda o passado
        self.assertNotEqual(a[3], b[3])

    def test_probabilidades_somam_um(self):
        m = self._modelo()
        probs, _ = m.adiante([0, 1, 2], guardar=False)
        for p in probs:
            self.assertAlmostEqual(sum(p), 1.0, places=12)

    def test_layernorm(self):
        y, _ = ModeloGPT._ln([[1.0, 2.0, 3.0, 6.0]], [1.0] * 4, [0.0] * 4)
        self.assertAlmostEqual(sum(y[0]), 0.0, places=12)
        self.assertAlmostEqual(sum(v * v for v in y[0]) / 4, 1.0, places=4)

    def test_configuracao_invalida(self):
        with self.assertRaises(ValueError):
            ConfigGPT(vocab=10, d=10, cabecas=3)
        m = self._modelo()
        with self.assertRaises(ValueError):
            m.adiante(list(range(7)))

    def test_decora_um_texto(self):
        # Um texto curto e periódico: o modelo tem de chegar perto de 0 bit (a sequência é determinística).
        texto = "abcabdabcabd" * 8
        tok = TokenizadorCaracteres.de_texto(texto)
        g = SynthaiGPT(tok, contexto=8, d=16, camadas=1, cabecas=2, semente=5)
        antes = g.bits_por_caractere(texto)
        g.treinar(texto, 300, lote=4, lr=1e-2, aquecimento=20)
        depois = g.bits_por_caractere(texto)
        self.assertGreater(antes, 1.5)
        self.assertLess(depois, 0.3)
        self.assertTrue(g.gerar("abcab", 7, temperatura=0).startswith("abcabdabcab"))

    def test_taxa_de_aprendizado(self):
        self.assertAlmostEqual(AdamW.taxa(0, 100, 1.0, 10), 0.1)
        self.assertAlmostEqual(AdamW.taxa(9, 100, 1.0, 10), 1.0)
        self.assertAlmostEqual(AdamW.taxa(100, 100, 1.0, 10), 0.1)
        self.assertAlmostEqual(AdamW.taxa(55, 100, 1.0, 10), 0.55)

    def test_recorte_do_gradiente(self):
        m = self._modelo()
        opt = AdamW(m, lr=0.0, recorte=1.0)
        G = m.zeros()
        G["c"][0][0] = 100.0
        self.assertAlmostEqual(opt.passo(G), 100.0)
        self.assertAlmostEqual(opt.m["c"][0][0], 0.1 * 1.0)   # o momento vê o gradiente recortado à norma 1

    def test_tokenizador_caracteres(self):
        tok = TokenizadorCaracteres.de_texto("olá mundo")
        self.assertEqual(tok.decodificar(tok.codificar("olá mundo")), "olá mundo")
        self.assertEqual(tok.decodificar(tok.codificar("xyz")), "???")

    def test_bpe(self):
        texto = " ".join(d for _, _, d in lexico_embutido())
        tok = TokenizadorBPE.treinar(texto, 60)
        self.assertEqual(len(tok.fusoes), 60)
        self.assertEqual(tok.decodificar(tok.codificar(texto)), texto)
        self.assertLess(len(tok.codificar(texto)), 0.8 * len(texto))
        tok2 = tokenizador_de_estado(json.loads(json.dumps(tok.estado())))
        self.assertEqual(tok2.codificar(texto), tok.codificar(texto))

    def test_amostragem(self):
        p = [0.5, 0.3, 0.15, 0.05]
        self.assertEqual(Amostragem.filtrar(p, temperatura=0), [1.0, 0.0, 0.0, 0.0])
        d = Amostragem.filtrar(p, top_k=2)
        self.assertAlmostEqual(d[0], 0.5 / 0.8)
        self.assertEqual(d[2:], [0.0, 0.0])
        d = Amostragem.filtrar(p, top_p=0.8)
        self.assertEqual(sum(1 for v in d if v > 0), 2)
        d = Amostragem.filtrar(p, temperatura=1.0)
        self.assertTrue(all(abs(a - b) < 1e-12 for a, b in zip(d, p)))
        quente = Amostragem.filtrar(p, temperatura=2.0)
        self.assertGreater(Informacao.entropia(quente), Informacao.entropia(p))
        d = Amostragem.filtrar(p, penalidade=2.0, recentes=[0])
        self.assertLess(d[0], 0.5)
        rng = random.Random(3)
        c = collections.Counter(Amostragem.sortear(p, rng) for _ in range(20000))
        self.assertAlmostEqual(c[0] / 20000, 0.5, delta=0.02)

    def test_salvar_carregar_e_selo(self):
        import tempfile
        tok = TokenizadorCaracteres.de_texto("abc def ghi\n")
        g = SynthaiGPT(tok, contexto=6, d=8, camadas=1, cabecas=2)
        with tempfile.TemporaryDirectory() as dirt:
            arq = str(Path(dirt) / "p.json")
            g.salvar(arq)
            h = SynthaiGPT.carregar(arq)
            self.assertEqual(h.modelo.p, g.modelo.p)
            self.assertEqual(h.gerar("ab", 5, temperatura=0), g.gerar("ab", 5, temperatura=0))
            bruto = json.loads(Path(arq).read_text(encoding="utf-8"))
            bruto["conteudo"]["pesos"]["c"][0][0] += 1.0
            Path(arq).write_text(json.dumps(bruto), encoding="utf-8")
            with self.assertRaises(ValueError):
                SynthaiGPT.carregar(arq)

    def test_retomar_treino_igual_ao_continuo(self):
        import tempfile
        texto = "o gato subiu no telhado e o rato correu\n" * 4
        tok = TokenizadorCaracteres.de_texto(texto)
        cont = SynthaiGPT(tok, contexto=8, d=8, camadas=1, cabecas=2)
        cont.treinar(texto, 6, lote=2, a_cada=3)
        with tempfile.TemporaryDirectory() as dirt:
            arq = str(Path(dirt) / "c.json")
            a = SynthaiGPT(tok, contexto=8, d=8, camadas=1, cabecas=2)
            a.treinar(texto, 6, lote=2, a_cada=3, checkpoint=arq, ate=3)
            b = SynthaiGPT.carregar(arq)
            b.retomar_otimizador()
            b.treinar(texto, 6, lote=2, a_cada=3)
        for k in cont.modelo.p:
            for la, lb in zip(cont.modelo.p[k], b.modelo.p[k]):
                for u, v in zip(la, lb):
                    self.assertAlmostEqual(u, v, places=12)

    def test_paralelo_igual_ao_serial(self):
        texto = "uma frase curta para testar o paralelo\n" * 3
        tok = TokenizadorCaracteres.de_texto(texto)
        a = SynthaiGPT(tok, contexto=8, d=8, camadas=1, cabecas=2)
        b = SynthaiGPT(tok, contexto=8, d=8, camadas=1, cabecas=2)
        pa = a.treinar(texto, 2, lote=4)
        pb = b.treinar(texto, 2, lote=4, processos=2)
        self.assertAlmostEqual(pa[-1], pb[-1], places=10)
        self.assertAlmostEqual(a.modelo.p["c"][0][0], b.modelo.p["c"][0][0], places=10)

    def test_corpus(self):
        texto, licenca = Corpus.glosas("embutido")
        self.assertIn("CC0", licenca)
        tr, te = Corpus.dividir(texto)
        self.assertTrue(set(tr.splitlines()).isdisjoint(set(te.splitlines()) - {""}))

    def test_linha_de_base_ngrama(self):
        texto, _ = Corpus.glosas("embutido")
        tr, te = Corpus.dividir(texto, 0.2)
        g = SynthaiGPT(TokenizadorCaracteres.de_texto(tr), contexto=16, d=8, camadas=1, cabecas=2)
        r = g.comparar_com_ngrama(tr, te, janelas=10)
        self.assertLess(r["ngrama_bpc"], r["uniforme_bpc"])
        self.assertGreater(r["gpt_bpc"], r["ngrama_bpc"])   # sem treino, o GPT perde para o n-grama


def principal_gpt(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="SYNTHAI_GPT.py gpt", description="SYNTHAI-GPT: treinar, gerar e avaliar")
    ap.add_argument("acao", choices=("ficha", "treinar", "gerar", "proximo", "avaliar"))
    ap.add_argument("--pesos", default="synthai_gpt_pesos.json")
    ap.add_argument("--corpus", default="wordnet", help="wordnet | ownpt | embutido | caminho de um .txt")
    ap.add_argument("--dados", default=None, help="pasta com wordnet30_sinsets.tsv.gz / ownpt_sinsets.tsv.gz")
    ap.add_argument("--tokenizador", choices=("caracteres", "bpe"), default="caracteres")
    ap.add_argument("--fusoes", type=int, default=200)
    ap.add_argument("--contexto", type=int, default=32)
    ap.add_argument("--d", type=int, default=32)
    ap.add_argument("--camadas", type=int, default=2)
    ap.add_argument("--cabecas", type=int, default=4)
    ap.add_argument("--passos", type=int, default=300)
    ap.add_argument("--lote", type=int, default=16)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--processos", type=int, default=1)
    ap.add_argument("--texto", default="a ")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--temperatura", type=float, default=0.8)
    ap.add_argument("--top_k", type=int, default=0)
    ap.add_argument("--top_p", type=float, default=0.95)
    ap.add_argument("--semente", type=int, default=0)
    a = ap.parse_args(argv)

    def corpus():
        if a.corpus in ("wordnet", "ownpt", "embutido"):
            return Corpus.glosas(a.corpus, pasta=a.dados)
        return Corpus.arquivo(a.corpus)
    if a.acao == "treinar":
        texto, licenca = corpus()
        treino, teste = Corpus.dividir(texto)
        if Path(a.pesos).exists():
            g = SynthaiGPT.carregar(a.pesos)
            g.retomar_otimizador()
        else:
            tok = (TokenizadorBPE.treinar(treino[:500_000], a.fusoes) if a.tokenizador == "bpe"
                   else TokenizadorCaracteres.de_texto(treino, minimo=max(1, len(treino) // 100_000)))
            g = SynthaiGPT(tok, contexto=a.contexto, d=a.d, camadas=a.camadas, cabecas=a.cabecas)
        g.treinar(treino, a.passos, lote=a.lote, lr=a.lr, validacao=teste[:100_000], a_cada=max(1, a.passos // 20),
                  relatorio=lambda l: print(serie_json(l), flush=True), processos=a.processos, checkpoint=a.pesos)
        g.salvar(a.pesos, dict(corpus=a.corpus, licenca_dados=licenca))
        print(serie_json(dict(pesos=a.pesos, **g.comparar_com_ngrama(treino, teste))))
        return 0
    g = SynthaiGPT.carregar(a.pesos)
    if a.acao == "ficha":
        print(serie_json(dict(**g.ficha(), metadados={k: v for k, v in g.metadados.items() if k != "otimizador"},
                              historico=g.historico[-3:])))
    elif a.acao == "gerar":
        print(g.gerar(a.texto, a.n, a.temperatura, a.top_k, a.top_p, semente=a.semente))
    elif a.acao == "proximo":
        print(serie_json(g.proximo(a.texto, 10)))
    else:
        texto, _ = corpus()
        treino, teste = Corpus.dividir(texto)
        print(serie_json(g.comparar_com_ngrama(treino, teste, janelas=400)))
    return 0


def principal_unificado() -> int:
    """SYNTHAI_GPT.py gpt <ação> ... | SYNTHAI_GPT.py teste | SYNTHAI_GPT.py lab <comando do NEXUS> ..."""
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "ajuda"):
        print(__doc__)
        return 0
    if args[0] == "gpt":
        return principal_gpt(args[1:])
    if args[0] == "teste":
        import io
        suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(c)
                                    for c in (TestesNexus, TestesExtensao, TestesV31, TestesGPT)])
        fluxo = io.StringIO()
        r = unittest.TextTestRunner(stream=fluxo, verbosity=2).run(suite)
        print(fluxo.getvalue())
        print(serie_json(dict(produto="SYNTHAI-GPT", versao=VERSAO_GPT, testes=r.testsRun,
                              falhas=len(r.failures), erros=len(r.errors), sucesso=r.wasSuccessful())))
        return 0 if r.wasSuccessful() else 1
    if args[0] == "lab":
        sys.argv = [sys.argv[0]] + args[1:]
        return principal()
    print("Comando desconhecido. Use: gpt | teste | lab", file=sys.stderr)
    return 2
