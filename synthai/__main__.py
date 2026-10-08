"""Demonstração: `python3 -m synthai` põe a mesma SYNTHAI, sem nenhuma mudança, em três tipos de tarefa (P284)."""

from .agente import Synthai
from .metacognicao import normalizado
from .mundos import MundoBandido, MundoSequencial
from .referencias import Acaso, Guloso, Oraculo

TAREFAS = {
    "escolha única": (lambda s: MundoSequencial(s, passos=1, n_acoes=200), 1000),
    "sequencial": (lambda s: MundoSequencial(s), 400),
    "bandido": (lambda s: MundoBandido(s), 20),
}


def avaliar(semente=1, tarefas=TAREFAS):
    tabela = {}
    for nome, (fazer, n) in tarefas.items():
        linha = {}
        for cls in (Acaso, Guloso, Oraculo, Synthai):
            mundo = fazer(semente)
            agente = cls(semente).calibrar(mundo)
            linha[cls.__name__] = mundo.rodar(agente, n)
        linha["normalizado"] = normalizado(linha["Synthai"]["retorno"], linha["Acaso"]["retorno"],
                                           linha["Oraculo"]["retorno"])
        tabela[nome] = linha
    return tabela


if __name__ == "__main__":
    for nome, linha in avaliar().items():
        print(f"{nome:14s}", "  ".join(f"{k} {v['retorno']:8.2f}" for k, v in linha.items() if k != "normalizado"),
              f"  normalizado {linha['normalizado']:.3f}")
