"""Aprendizado contínuo NumPy em quatro tarefas sintéticas identificadas.

O benchmark fornece explicitamente o ID da tarefa nas entradas. Diagnósticos
e intervenções usam exclusivamente treino; avaliações ficam reservadas. Este
experimento pequeno não implementa aprendizagem contínua de um LLM.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


@dataclass(frozen=True)
class DadosTarefa:
    tarefa: int
    fase: str
    x: np.ndarray
    y: np.ndarray
    ids: tuple[str, ...]


def gerar_fluxo(semente: int = 23, treino: int = 192, teste: int = 96) -> list[dict[str, DadosTarefa]]:
    """Rotações/permutação de rótulos mudam o domínio; one-hot torna-o task-aware."""
    if not isinstance(semente, int) or isinstance(semente, bool) or semente < 0:
        raise ValueError("semente deve ser um inteiro não negativo")
    if any(not isinstance(n, int) or isinstance(n, bool) or n < 3 for n in (treino, teste)):
        raise ValueError("cada fase precisa de pelo menos três exemplos")
    base = np.array([[1.8, -.9, .7, -.4], [-1.2, 1.5, -.7, .3], [-.6, -.6, .3, 1.5]])
    fluxo = []
    for tarefa in range(4):
        rng_dominio = np.random.default_rng(np.random.SeedSequence([semente, 701, tarefa]))
        rotacao, _ = np.linalg.qr(rng_dominio.normal(size=(4, 4)))
        permutacao = rng_dominio.permutation(3)
        centros = base[permutacao] @ rotacao + rng_dominio.normal(0, .25, size=4)
        fases = {}
        for codigo, fase, n in ((101, "treino", treino), (203, "teste", teste)):
            rng = np.random.default_rng(np.random.SeedSequence([semente, codigo, tarefa]))
            y = np.arange(n, dtype=np.int64) % 3
            rng.shuffle(y)
            x = np.zeros((n, 8), dtype=np.float64)
            x[:, :4] = centros[y] + rng.normal(0, .55, size=(n, 4))
            x[:, 4 + tarefa] = 1.
            ids = tuple(f"{fase}:{tarefa}:{i}" for i in range(n))
            x.setflags(write=False)
            y.setflags(write=False)
            fases[fase] = DadosTarefa(tarefa, fase, x, y, ids)
        fluxo.append(fases)
    return fluxo


class MemoriaReservoir:
    """Reservoir uniforme, com proveniência explícita e cópias isoladas."""
    def __init__(self, capacidade: int = 128, dimensao: int = 8, semente: int = 0):
        if not isinstance(capacidade, int) or isinstance(capacidade, bool) or not 1 <= capacidade <= 4096:
            raise ValueError("capacidade deve estar entre 1 e 4096")
        if not isinstance(dimensao, int) or isinstance(dimensao, bool) or not 1 <= dimensao <= 128:
            raise ValueError("dimensão inválida")
        self.capacidade, self.dimensao = capacidade, dimensao
        self.rng = np.random.default_rng(semente)
        self.registros: list[tuple[np.ndarray, int, str]] = []
        self.vistos = 0
        self.identificadores: set[str] = set()
        # A auditoria de duplicatas também tem orçamento, separado do reservoir.
        self.orcamento_proveniencia = 4096

    def adicionar(self, x: np.ndarray, y: np.ndarray, ids: tuple[str, ...], *, fase: str) -> None:
        xx, yy = np.asarray(x), np.asarray(y)
        if fase != "treino" or xx.ndim != 2 or xx.shape[1] != self.dimensao:
            raise ValueError("replay aceita exclusivamente entradas de treino com dimensão correta")
        if xx.dtype.kind not in "fiu" or not np.isfinite(xx).all():
            raise ValueError("entradas precisam ser números finitos")
        if yy.shape != (len(xx),) or yy.dtype.kind not in "iu" or np.any(yy < 0):
            raise ValueError("rótulos precisam ser inteiros não negativos")
        if len(ids) != len(xx) or any(not isinstance(i, str) or not i.startswith("treino:") for i in ids):
            raise ValueError("proveniência de treino ausente")
        if len(set(ids)) != len(ids) or self.identificadores.intersection(ids):
            raise ValueError("o mesmo exemplo não pode ser contado duas vezes")
        if self.vistos + len(ids) > self.orcamento_proveniencia:
            raise ValueError("orçamento de proveniência esgotado; iniciar uma nova experiência")
        # Validação precede qualquer mutação, inclusive do gerador aleatório.
        for vetor, rotulo, identificador in zip(xx, yy, ids):
            self.vistos += 1
            self.identificadores.add(identificador)
            registro = (np.array(vetor, dtype=np.float64, copy=True), int(rotulo), identificador)
            if len(self.registros) < self.capacidade:
                self.registros.append(registro)
            else:
                indice = int(self.rng.integers(self.vistos))
                if indice < self.capacidade:
                    self.registros[indice] = registro

    def amostrar(self, n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, tuple[str, ...]]:
        if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= 8192 or not self.registros:
            raise ValueError("amostragem precisa de memória não vazia e tamanho positivo")
        indices = rng.integers(len(self.registros), size=n)
        return (np.stack([self.registros[i][0] for i in indices]),
                np.array([self.registros[i][1] for i in indices], dtype=np.int64),
                tuple(self.registros[i][2] for i in indices))


def posto_efetivo(ativacoes: np.ndarray) -> dict[str, float]:
    """exp(H(s/sum(s))) dos valores singulares das ativações centradas."""
    h = np.asarray(ativacoes, dtype=np.float64)
    if h.ndim != 2 or min(h.shape) < 1 or not np.isfinite(h).all():
        raise ValueError("ativações precisam ser uma matriz finita não vazia")
    singulares = np.linalg.svd(h - np.mean(h, axis=0), compute_uv=False)
    soma = float(np.sum(singulares))
    if soma <= np.finfo(float).eps * max(1., float(np.linalg.norm(h))):
        return {"posto_efetivo": 0., "posto_normalizado": 0.}
    p = singulares[singulares > 0] / soma
    efetivo = float(np.exp(-np.sum(p * np.log(p))))
    limite = min(h.shape[0] - 1, h.shape[1])
    return {"posto_efetivo": efetivo, "posto_normalizado": min(1., efetivo / max(1, limite))}


def atividade_dormente(ativacoes: np.ndarray, limiar: float = .12) -> np.ndarray:
    h = np.asarray(ativacoes, dtype=np.float64)
    if h.ndim != 2 or min(h.shape) < 1 or not np.isfinite(h).all() or not 0 <= limiar < 1:
        raise ValueError("atividade ou limiar inválido")
    atividade = np.mean(np.abs(h), axis=0)
    media = float(np.mean(atividade))
    if media <= np.finfo(float).eps:
        return np.ones(h.shape[1], dtype=bool)
    return atividade <= limiar * media


def diagnosticar(rede: Any, x_treino: np.ndarray, limiar: float = .12) -> dict[str, Any]:
    _, ocultas = rede.forward(x_treino)
    return {"norma_pesos": float(math.sqrt(sum(float(np.sum((w * rede.mascaras.get(nome, 1.)) ** 2)) for nome, w in rede.parametros.items() if nome.startswith("W")))),
            "camadas": [dict(posto_efetivo(h), fracao_dormente=float(np.mean(atividade_dormente(h, limiar)))) for h in ocultas]}


def encolher_perturbar(rede: Any, rng: np.random.Generator, encolhimento: float = .995, ruido: float = .002) -> None:
    if not math.isfinite(encolhimento) or not 0 < encolhimento <= 1 or not math.isfinite(ruido) or ruido < 0:
        raise ValueError("parâmetros de shrink-and-perturb inválidos")
    for nome, valor in rede.parametros.items():
        if nome.startswith("W"):
            atualizado = encolhimento * valor + rng.normal(0, ruido, valor.shape)
            mascara = rede.mascaras.get(nome)
            if mascara is not None:
                atualizado *= mascara
            valor[:] = atualizado


def reciclar_dormentes(rede: Any, x_treino: np.ndarray, rng: np.random.Generator,
                      limiar: float = .12, max_por_camada: int = 2) -> list[dict[str, Any]]:
    """Intervenção inspirada em ReDo; não promete preservar todas as saídas."""
    if not isinstance(max_por_camada, int) or isinstance(max_por_camada, bool) or max_por_camada < 0:
        raise ValueError("limite de unidades inválido")
    _, ocultas = rede.forward(x_treino)
    alteracoes = []
    for camada, h in enumerate(ocultas):
        nome_in, nome_out = f"W{camada}", f"W{camada + 1}"
        dormentes = np.flatnonzero(atividade_dormente(h, limiar))
        # Uma unidade podada em todos os caminhos não pode ser reativada sem
        # violar a máscara; não a contamos como regenerada.
        elegiveis = np.ones(h.shape[1], dtype=bool)
        if nome_in in rede.mascaras:
            elegiveis &= np.any(rede.mascaras[nome_in], axis=0)
        if nome_out in rede.mascaras:
            elegiveis &= np.any(rede.mascaras[nome_out], axis=1)
        atividade = np.mean(np.abs(h), axis=0)
        escolhidos = sorted((i for i in dormentes if elegiveis[i]), key=lambda unidade: (atividade[unidade], int(unidade)))[:max_por_camada]
        for unidade in escolhidos:
            incoming, outgoing = rede.parametros[nome_in], rede.parametros[nome_out]
            novo = rng.normal(0, math.sqrt(2. / incoming.shape[0]), incoming.shape[0])
            if nome_in in rede.mascaras:
                novo *= rede.mascaras[nome_in][:, unidade]
            incoming[:, unidade] = novo
            rede.parametros[f"b{camada}"][unidade] = 0.
            outgoing[unidade, :] = 0.
        alteracoes.append({"camada": camada, "dormentes_detectados": int(len(dormentes)),
                           "dormentes_reativaveis": int(np.sum(elegiveis[dormentes])),
                           "unidades_recicladas": [int(i) for i in escolhidos]})
    return alteracoes


def esquecimento(matriz: np.ndarray) -> dict[str, Any]:
    r = np.asarray(matriz, dtype=np.float64)
    if r.ndim != 2 or r.shape[0] != r.shape[1] or len(r) < 2 or not np.isfinite(r).all() or np.any((r < 0) | (r > 1)):
        raise ValueError("R precisa ser uma matriz quadrada de acurácias")
    # Para tarefa j, só etapas em que ela já havia sido aprendida entram no máximo.
    valores = [float(np.max(r[j:-1, j]) - r[-1, j]) for j in range(len(r) - 1)]
    return {"por_tarefa_anterior": valores, "medio": float(np.mean(valores)),
            "definicao": "maior acurácia pós-aprendizado antes da última etapa - acurácia final; negativo indica melhoria"}


def deficit_adaptacao(atual: list[float], virgem: list[float]) -> list[float]:
    a, v = np.asarray(atual, dtype=float), np.asarray(virgem, dtype=float)
    if a.ndim != 1 or len(a) == 0 or a.shape != v.shape or not np.isfinite(a).all() or not np.isfinite(v).all() or np.any((a < 0) | (a > 1) | (v < 0) | (v > 1)):
        raise ValueError("acurácias comparadas precisam de tamanho igual e estar em [0,1]")
    return [float(x) for x in v - a]


def _treinar(rede: Any, dados: DadosTarefa, passos: int, lote: int, rng: np.random.Generator,
             memoria: MemoriaReservoir | None = None) -> None:
    for _ in range(passos):
        replay_n = lote // 2 if memoria is not None and memoria.registros else 0
        indices = rng.integers(len(dados.y), size=lote - replay_n)
        x, y = dados.x[indices], dados.y[indices]
        if replay_n:
            mx, my, _ = memoria.amostrar(replay_n, rng)
            x, y = np.concatenate((x, mx)), np.concatenate((y, my))
        _, gradientes = rede.perda_gradientes(x, y, l2=1e-4)
        rede.aplicar(gradientes, taxa=.045)


def experimento(semente: int = 23, passos: int = 60, capacidade: int = 128, tamanho_lote: int = 32) -> dict[str, Any]:
    from ml_nucleo import RedeMLP, acuracia
    if any(not isinstance(n, int) or isinstance(n, bool) for n in (passos, tamanho_lote)) or not 2 <= passos <= 500 or not 4 <= tamanho_lote <= 128:
        raise ValueError("passos em [2,500] e lote em [4,128]")
    fluxo = gerar_fluxo(semente)
    # Instanciação também valida a capacidade antes do início dos treinos.
    MemoriaReservoir(capacidade, semente=semente)
    inicial = RedeMLP(dimensoes=(8, 32, 16, 3), semente=semente)
    virgens = []
    for tarefa, dados in enumerate(fluxo):
        rede = inicial.copiar()
        rng = np.random.default_rng(np.random.SeedSequence([semente, 811, tarefa]))
        _treinar(rede, dados["treino"], passos, tamanho_lote, rng)
        virgens.append(float(acuracia(rede, dados["teste"].x, dados["teste"].y)))
    resultados = {}
    for metodo in ("sequencial", "replay", "replay_shrink_perturb", "replay_reciclagem"):
        rede = inicial.copiar()
        memoria = None if metodo == "sequencial" else MemoriaReservoir(capacidade, semente=semente + 909)
        matriz, diagnosticos, intervencoes, virgens_pareados = [], [], [], []
        for tarefa, dados in enumerate(fluxo):
            rng = np.random.default_rng(np.random.SeedSequence([semente, 811, tarefa]))
            _treinar(rede, dados["treino"], passos, tamanho_lote, rng, memoria)
            # Controle sem história de pesos, mas com exatamente a mesma mistura
            # de exemplos e orçamento de atualização desta etapa do método.
            # O reservoir é lido, sem alteração, pelos dois treinos.
            controle = inicial.copiar()
            rng_controle = np.random.default_rng(np.random.SeedSequence([semente, 811, tarefa]))
            _treinar(controle, dados["treino"], passos, tamanho_lote, rng_controle, memoria)
            antes = diagnosticar(rede, dados["treino"].x)
            rng_intervencao = np.random.default_rng(np.random.SeedSequence([semente, 919, tarefa]))
            rng_controle_intervencao = np.random.default_rng(np.random.SeedSequence([semente, 919, tarefa]))
            detalhes = []
            if metodo == "replay_shrink_perturb":
                encolher_perturbar(rede, rng_intervencao)
                encolher_perturbar(controle, rng_controle_intervencao)
                detalhes = [{"encolhimento": .995, "desvio_ruido": .002}]
            elif metodo == "replay_reciclagem":
                detalhes = reciclar_dormentes(rede, dados["treino"].x, rng_intervencao)
                reciclar_dormentes(controle, dados["treino"].x, rng_controle_intervencao)
            virgens_pareados.append(float(acuracia(controle, dados["teste"].x, dados["teste"].y)))
            diagnosticos.append({"etapa": tarefa, "fase": "treino", "antes": antes,
                                  "depois": diagnosticar(rede, dados["treino"].x)})
            intervencoes.append({"etapa": tarefa, "fase_diagnostico": "treino", "detalhes": detalhes})
            # Todo teste é observacional: nunca participa de minibatch, replay ou decisões.
            matriz.append([float(acuracia(rede, item["teste"].x, item["teste"].y)) for item in fluxo])
            if memoria is not None:
                memoria.adicionar(dados["treino"].x, dados["treino"].y, dados["treino"].ids, fase="treino")
        r = np.asarray(matriz)
        corrente = [float(r[i, i]) for i in range(4)]
        resultados[metodo] = {"matriz_R": matriz, "acuracia_final_media": float(np.mean(r[-1])),
            "esquecimento": esquecimento(r), "acuracia_tarefa_apos_aprender": corrente,
            "acuracia_virgem_pareado": virgens_pareados,
            "deficit_ante_virgem": deficit_adaptacao(corrente, virgens_pareados),
            "diagnosticos_treino": diagnosticos, "intervencoes": intervencoes,
            "replay": {"capacidade": capacidade if memoria else 0, "retidos": len(memoria.registros) if memoria else 0,
                       "vistos": memoria.vistos if memoria else 0,
                       "ids_retidos": [i for _, _, i in memoria.registros] if memoria else [],
                       "ids_auditoria": len(memoria.identificadores) if memoria else 0,
                       "orcamento_ids_auditoria": memoria.orcamento_proveniencia if memoria else 0,
                       "fases_permitidas": ["treino"]},
            "atualizacoes_sgd": 4 * passos, "atualizacoes_controle_virgem": 4 * passos,
            "controle_virgem": "mesma mistura de minibatches, inicialização e protocolo de intervenção por etapa; sem história de pesos",
            "exemplos_por_minibatch": tamanho_lote}
    return {"experimento": "aprendizagem_continua_task_aware", "semente": semente,
            "benchmark": {"tarefas": 4, "entradas": "4 características + one-hot de tarefa com 4 posições",
                          "classes": 3, "treino_por_tarefa": 192, "teste_por_tarefa": 96,
                          "id_tarefa_disponivel": True, "avaliacao": "teste reservado; não usado para selecionar métodos"},
            "orcamento": {"passos_por_tarefa": passos, "minibatch": tamanho_lote,
                          "mesma_inicializacao": True, "replay_fracao": .5,
                          "observacao": "igual número de atualizações e tamanho de lote; replay substitui parte dos exemplos correntes"},
            "acuracia_virgem_por_tarefa": virgens, "metodos": resultados,
            "limitacoes": ["Quatro tarefas sintéticas task-aware; não mede autonomia ou inteligência geral.",
                           "Déficit de adaptação não demonstra perda irreversível de plasticidade.",
                           "Reciclagem é uma intervenção inspirada em ReDo, não CBP nem reprodução integral do artigo.",
                           "Posto e atividade são diagnósticos, não provas causais de aprendizagem.",
                           "Sem execução de Avalanche, Continual World ou treino de LLM.",
                           "Custos adicionais de diagnósticos/intervenções não igualam tempo de parede entre métodos."]}


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--semente", type=int, default=23)
    parser.add_argument("--passos", type=int, default=60)
    parser.add_argument("--capacidade", type=int, default=128)
    parser.add_argument("--lote", type=int, default=32)
    parser.add_argument("--saida", type=Path)
    opcoes = parser.parse_args(args)
    resultado = experimento(opcoes.semente, opcoes.passos, opcoes.capacidade, opcoes.lote)
    texto = json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False)
    if opcoes.saida:
        Path(opcoes.saida).write_text(texto + "\n", encoding="utf-8")
    print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
