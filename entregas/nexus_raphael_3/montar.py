#!/usr/bin/env python3
"""Monta o NEXUS-RAPHAEL 3.0.0 a partir da 2.2.0 recebida (externos/, intacta) e das extensões em partes/.

Cada correção é uma substituição de texto EXATA que precisa casar uma vez; se o original mudar,
a montagem falha em vez de produzir um arquivo silenciosamente errado.
"""
from pathlib import Path
import sys

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parents[1] / "externos" / "nexus_raphael_v2_0" / "nexus_raphael_v2_0.py.txt"
SAIDA = AQUI / "nexus_raphael.py"
PARTES = ["e1_estatistica_algebra.py", "e2_calibracao_bandidos_texto_dinamica.py", "e3_jogos.py",
          "e4_logica_codificacao_experimentos.py", "e6_auditoria_v30.py"]
TESTES = "e5_testes_cli.py"

CABECALHO = '''"""NEXUS–RAPHAEL 3.1.0: laboratório experimental auditável, offline, só biblioteca padrão.

Execução: python3 nexus_raphael.py teste
          python3 nexus_raphael.py experimento --modo rapido
          python3 nexus_raphael.py kuhn | leduc | velha | sat | calibracao | bandidos | megasena3 | caos
          python3 nexus_raphael.py ciclo --texto "logic and learning"
          python3 nexus_raphael.py estado

O que mudou desde a 2.2.0 (cada item tem teste em TestesExtensao):
  CORRIGIDO
  - Rede removida: não há urllib nem consulta HTTP; permitir_rede=True levanta erro.
  - IC do bootstrap pelos quantis da contagem real de réplicas (os índices fixos [24]/[974]
    quebravam com 500 réplicas e erravam o percentil com 2000).
  - Qui-quadrado da Mega-Sena com o fator 54/59 (6 dezenas distintas por sorteio) e com p-valor.
  - Intervalo da Beta pelos quantis exatos (a aproximação ±1,96σ sai de [0, 1] em amostra pequena).
  - H-M3 com veredito combinado além do por seed; H-M7 com arrependimento pelas médias
    verdadeiras em muitas sementes (cinco sementes e 200 passos de avaliação não decidem nada).
  ACRESCENTADO (funcionalidade real, com teste)
  - Estatística: gama e beta incompletas, χ², t, normal, Wilson, Clopper-Pearson, t pareado,
    binomial exato, sinal, permutação, Holm.
  - Álgebra linear sem numpy: LU com pivô, determinante, inversa, mínimos quadrados (cumeeira),
    Gram-Schmidt, Jacobi, valores singulares, potência, PCA.
  - Calibração (isotônica PAV e Platt), bandidos (ε-guloso, UCB1, Thompson, cota de Lai-Robbins),
    informação (entropia, KL, informação mútua, Levenshtein), modelo de caracteres Witten-Bell,
    dinâmica (RK4, Lorenz, Lyapunov de Benettin, períodos e dobras do mapa logístico).
  - Jogos: pôquer de Kuhn e Leduc, CFR vanilla, com acaso amostrado e com amostragem externa,
    melhor resposta exata e explorabilidade, simplex exato em frações (Kuhn = −1/18 pela forma
    normal 64×64), jogo da velha com alfa-beta e Q-learning.
  - Lógica: Tseitin + DPLL (sem o teto de 16 variáveis), casa dos pombos, transição do 3-SAT.
  - Codificação: base 26 bijetiva, Hamming (7,4), CRC-32, Huffman, LZ78.

  3.1.0 (do texto "NEXUS–RAPHAEL v3.0" recebido, só o que se sustentou, reescrito e testado em TestesV31)
  - Murphy completa: BS = REL − RES + UNC + WBV − WBC, exata para qualquer previsão (a clássica não fecha).
  - MensagemImutavel: conteúdo congelado em profundidade e trilha em cadeia de hashes.
  - SondaColapso: a PCA apaga a identidade de baixa variância; a projeção supervisionada a guarda.
  - ModelagemPorPotencial: o shaping γΦ(s') − Φ(s) preserva a política ótima; o bônus aditivo não.
  - kl_beta em forma fechada, para detectar deriva entre posteriores.

Comentários e textos em português. Dados offline são léxico manual de teste, não fonte primária.
Esta implementação NÃO constitui AGI, ASI, AFI ou evidência de consciência.
"""'''

SUBSTITUICOES = [
    # versão e cabeçalho
    ('VERSAO = "2.2.0"', 'VERSAO = "3.1.0"'),
    # rede: fora
    ("from urllib.parse import quote\nfrom urllib.request import Request, urlopen\n", ""),
    ('    """Data lake local com fonte e licença; consulta HTTP opcional, sem chave."""\n'
     '    def __init__(self, repo: Repositorio, permitir_rede: bool = False):\n'
     '        self.repo = repo\n',
     '    """Data lake local com fonte e licença. Desde a 3.0.0, sem rede: só o léxico embutido."""\n'
     '    def __init__(self, repo: Repositorio, permitir_rede: bool = False):\n'
     '        if permitir_rede:\n'
     '            raise ValueError("A 3.0.0 é offline: não há consulta de rede")\n'
     '        self.repo = repo\n'),
    ("        return self._consultar_api(palavra.lower()) if self.permitir_rede else []\n", "        return []\n"),
    ('    parser.add_argument("--online", action="store_true", help="Permitir somente fonte lexical documentada")\n', ""),
    ("    cfg = Configuracao(raiz=args.raiz, permitir_rede=args.online)", "    cfg = Configuracao(raiz=args.raiz)"),
    ('                rede_no_codigo="desligada por padrão; não verificada nesta execução",',
     '                rede_no_codigo="ausente (sem urllib/socket; conferido por TestesExtensao.test_sem_rede)",'),
    # IC do bootstrap: quantis pela contagem real de réplicas
    ("        return media, replicas[int(.025*(repeticoes-1))], replicas[int(.975*(repeticoes-1))]",
     "        return media, Estatistica.quantil(replicas, .025), Estatistica.quantil(replicas, .975)"),
    ("        ic = [replicacoes[24],replicacoes[974]]  # 1.000 bootstrap, ~percentis 2.5/97.5",
     "        ic = [Estatistica.quantil(replicacoes, .025), Estatistica.quantil(replicacoes, .975)]"),
    # qui-quadrado da Mega-Sena com p-valor
    ("                         qui_quadrado=qui2, p_valor=None,\n"
     '                         nota="Sem teste p para qui-quadrado no núcleo padrão; nenhum palpite ou vantagem alegada")',
     "                         qui_quadrado=qui2, p_valor=Estatistica.qui2_sf(qui2 / (54 / 59), 59),\n"
     '                         nota="p-valor com o fator 54/59 (6 dezenas distintas por sorteio); nenhum palpite ou vantagem alegada")'),
    # Beta: intervalo exato
    ("    def intervalo_aproximado(self) -> tuple[float, float]:\n",
     "    def intervalo_exato(self, nivel: float = .95) -> tuple[float, float]:\n"
     "        return Estatistica.beta_credivel(self.a, self.b, nivel)\n\n"
     "    def intervalo_aproximado(self) -> tuple[float, float]:\n"),
    # testes: as duas classes
    ("    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestesNexus)\n",
     "    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(TestesNexus),\n"
     "                                unittest.defaultTestLoader.loadTestsFromTestCase(TestesExtensao),\n"
     "                                unittest.defaultTestLoader.loadTestsFromTestCase(TestesV31)])\n"),
    # CLI
    ('                                 "ciclo", "jogo", "lexico", "estado"))',
     '                                 "ciclo", "jogo", "lexico", "estado", "kuhn", "leduc", "velha", "sat",\n'
     '                                 "calibracao", "bandidos", "megasena3", "caos"))'),
    ('    lexico = LagoLexical(repo, cfg.permitir_rede)\n',
     '    if args.comando in COMANDOS_3:\n'
     '        resultado = COMANDOS_3[args.comando](args.modo)\n'
     '        repo.salvar_json(f"{args.comando}.json", resultado)\n'
     '        print(serie_json(resultado))\n'
     '        return 0\n'
     '    lexico = LagoLexical(repo, cfg.permitir_rede)\n'),
]


def montar() -> str:
    texto = BASE.read_text(encoding="utf-8")
    ini = texto.index('"""NEXUS')
    fim = texto.index('"""', ini + 3) + 3
    texto = texto[:ini] + CABECALHO + texto[fim:]
    # o método de rede sai inteiro
    a = texto.index("    def _consultar_api(self, palavra: str)")
    b = texto.index("\nclass Codificador:")
    texto = texto[:a].rstrip() + "\n\n" + texto[b:]
    for velho, novo in SUBSTITUICOES:
        n = texto.count(velho)
        if n != 1:
            sys.exit(f"Substituição casou {n} vezes: {velho[:70]!r}")
        texto = texto.replace(velho, novo)
    extensoes = "".join((AQUI / "partes" / p).read_text(encoding="utf-8") for p in PARTES)
    marca = "class TestesNexus(unittest.TestCase):"
    texto = texto.replace(marca, extensoes.strip() + "\n\n\n" + marca)
    testes = (AQUI / "partes" / TESTES).read_text(encoding="utf-8")
    marca = "def executar_testes() -> dict[str, Any]:"
    texto = texto.replace(marca, testes.strip() + "\n\n\n" + marca)
    return texto


if __name__ == "__main__":
    t = montar()
    SAIDA.write_text(t, encoding="utf-8")
    print(SAIDA, len(t.splitlines()), "linhas")
