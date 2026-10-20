"""Treina os pesos distribuídos com o SYNTHAI-GPT (retomável: rode de novo e continua do checkpoint)."""
import importlib.util, json, sys
from pathlib import Path


def main():
    modulo, dados, saida, passos = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    spec = importlib.util.spec_from_file_location("sg", modulo)
    N = importlib.util.module_from_spec(spec)
    sys.modules["sg"] = N
    spec.loader.exec_module(N)
    texto, licenca = N.Corpus.glosas("wordnet", pasta=dados)
    treino, teste = N.Corpus.dividir(texto)
    if Path(saida).exists():
        g = N.SynthaiGPT.carregar(saida)
        g.retomar_otimizador()
    else:
        g = N.SynthaiGPT(N.TokenizadorCaracteres.de_texto(treino, minimo=100), contexto=32, d=32, camadas=2, cabecas=4)
    log = lambda l: print(json.dumps(l), flush=True)
    g.treinar(treino, passos, lote=16, lr=3e-3, aquecimento=100, semente=1, validacao=teste[:200000],
              a_cada=50, relatorio=log, processos=4, checkpoint=saida)
    print(json.dumps(dict(fim=True, **g.comparar_com_ngrama(treino, teste, ordem=3, janelas=400))), flush=True)


if __name__ == "__main__":
    main()
