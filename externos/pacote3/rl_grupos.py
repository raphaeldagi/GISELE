"""GRPO de uma decisão: bandido contextual linear, NumPy e recompensa verificável.

Não treina LLMs. A comparação fixa ações amostradas, não o número de grupos,
passes de otimização, tempo ou FLOPs. G=2 não é tratado como estimador não viesado.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Sequence

import numpy as np


def _inteiro(valor, minimo: int, maximo: int, nome: str) -> int:
    if isinstance(valor, (bool, np.bool_)) or not isinstance(valor, (int, np.integer)):
        raise ValueError(f'{nome} deve ser inteiro.')
    if not minimo <= int(valor) <= maximo:
        raise ValueError(f'{nome} fora dos limites [{minimo}, {maximo}].')
    return int(valor)


def _real(valor, minimo: float, maximo: float, nome: str) -> float:
    if isinstance(valor, (bool, np.bool_)) or not np.isscalar(valor):
        raise ValueError(f'{nome} deve ser escalar numérico.')
    try:
        resultado = float(valor)
    except (TypeError, ValueError):
        raise ValueError(f'{nome} deve ser numérico.') from None
    if not np.isfinite(resultado) or not minimo <= resultado <= maximo:
        raise ValueError(f'{nome} fora dos limites.')
    return resultado


def _vetor(valor, tamanho: int, nome: str) -> np.ndarray:
    a = np.asarray(valor, dtype=np.float64)
    if a.shape != (tamanho,) or not np.all(np.isfinite(a)):
        raise ValueError(f'{nome}: forma ou valores inválidos.')
    return a


def _imutavel(a: np.ndarray) -> np.ndarray:
    """Base bytes impede até a reativação de writeable, além de copiar o estado."""
    a = np.ascontiguousarray(a)
    return np.frombuffer(a.tobytes(), dtype=a.dtype).reshape(a.shape)


def log_softmax(logits: np.ndarray) -> np.ndarray:
    a = np.asarray(logits, dtype=np.float64)
    if a.ndim != 1 or len(a) != 3 or not np.all(np.isfinite(a)):
        raise ValueError('São necessários três logits finitos.')
    with np.errstate(over='ignore', invalid='ignore'):
        deslocado = a - np.max(a)
    if not np.all(np.isfinite(deslocado)):
        raise ValueError('Diferença entre logits fora do intervalo numérico suportado.')
    return deslocado - np.log(np.exp(deslocado).sum())


def vantagens_grupo(recompensas: np.ndarray, epsilon: float = 1e-8) -> np.ndarray:
    """Normalização populacional por grupo; grupo sem contraste gera vantagem zero."""
    eps = _real(epsilon, 1e-12, 1., 'epsilon')
    r = np.asarray(recompensas, dtype=np.float64)
    if r.ndim != 1 or not 2 <= len(r) <= 64 or not np.all(np.isfinite(r)):
        raise ValueError('Recompensas: vetor finito de 2 a 64 elementos.')
    # Testar constância antes da média/desvio evita overflow desnecessário.
    if np.all(r == r[0]):
        return np.zeros_like(r)
    # Recompensas da API podem cobrir toda a faixa float64. Calcular média e
    # variância em r/max(|r|) mantém os valores intermediários limitados.
    escala = float(np.max(np.abs(r)))
    normalizadas = r / escala
    centro = normalizadas - normalizadas.mean()
    desvio = float(np.sqrt(np.mean(centro*centro)))
    # Epsilon mantém as unidades originais. Evitar eps/escala quando escala é
    # subnormal também impede overflow no denominador.
    if escala >= eps:
        vantagens = centro / (desvio + eps/escala)
    else:
        razao = escala/eps
        vantagens = (centro*razao) / (1. + desvio*razao)
    if not np.all(np.isfinite(vantagens)):
        raise ValueError('Normalização de vantagens não finita.')
    return vantagens


@dataclass(frozen=True)
class Contexto:
    id: str
    fase: str
    features: np.ndarray

    def __post_init__(self):
        if self.fase not in ('treino', 'validacao', 'teste') or not self.id.startswith(self.fase + ':'):
            raise ValueError('Identificador e fase incompatíveis.')
        object.__setattr__(self, 'features', _imutavel(_vetor(self.features, 5, 'features')))


def gerar_contextos(semente: int = 31, tamanhos: Sequence[int] = (128, 64, 128)) -> dict[str, tuple[Contexto, ...]]:
    s = _inteiro(semente, 0, 2**32 - 1, 'semente')
    if len(tamanhos) != 3:
        raise ValueError('Três tamanhos são necessários.')
    saida = {}
    for indice, (fase, n) in enumerate(zip(('treino', 'validacao', 'teste'), tamanhos)):
        n = _inteiro(n, 1, 1024, 'tamanho')
        rng = np.random.default_rng(np.random.SeedSequence([s, indice, 971]))
        pontos = rng.uniform(-1., 1., size=(n, 2))
        saida[fase] = tuple(Contexto(f'{fase}:{i}', fase,
            np.array([1., x, y, x*y, x*x-y*y])) for i, (x, y) in enumerate(pontos))
    # Separação de IDs e entradas, antes de qualquer treinamento.
    ids = [c.id for grupo in saida.values() for c in grupo]
    entradas = [c.features.tobytes() for grupo in saida.values() for c in grupo]
    if len(ids) != len(set(ids)) or len(entradas) != len(set(entradas)):
        raise ValueError('Contextos sobrepostos entre fases.')
    return saida


_ORACULO = _imutavel(np.array([
    [.1, -.1, 0.], [1., -1., .2], [.2, .7, -1.],
    [.25, -.3, .1], [.1, .05, -.15],
]))


def acao_otima(contexto: Contexto) -> int:
    """Oráculo do ambiente, usado para recompensas e avaliação, nunca no gradiente."""
    return int(np.argmax(contexto.features @ _ORACULO))


def verificar_recompensa(contexto: Contexto, acao: int) -> float:
    a = _inteiro(acao, 0, 2, 'acao')
    return float(a == acao_otima(contexto))


@dataclass(frozen=True)
class RolloutGrupo:
    contexto_id: str
    features: np.ndarray
    acoes: np.ndarray
    recompensas: np.ndarray
    vantagens: np.ndarray
    log_velha: np.ndarray
    log_referencia: np.ndarray

    def __post_init__(self):
        if not isinstance(self.contexto_id, str) or not self.contexto_id.startswith('treino:'):
            raise ValueError('Rollouts de treinamento exigem contexto de treino.')
        x = _vetor(self.features, 5, 'features')
        a = np.asarray(self.acoes)
        if a.ndim != 1 or not 2 <= len(a) <= 64 or a.dtype.kind not in 'iu' or np.any((a < 0) | (a > 2)):
            raise ValueError('Ações inteiras entre 0 e 2; grupo de 2 a 64.')
        r = _vetor(self.recompensas, len(a), 'recompensas')
        vantagens = _vetor(self.vantagens, len(a), 'vantagens')
        if np.any((r < 0) | (r > 1)):
            raise ValueError('Recompensas devem estar em [0,1].')
        if not np.allclose(vantagens, vantagens_grupo(r), rtol=1e-10, atol=1e-12):
            raise ValueError('Vantagens não correspondem às recompensas deste grupo.')
        logs = []
        for nome in ('log_velha', 'log_referencia'):
            l = _vetor(getattr(self, nome), 3, nome)
            if abs(float(np.exp(l).sum()) - 1.) > 1e-10 or np.any(l > 1e-12):
                raise ValueError('Log-probabilidades não normalizadas.')
            logs.append(l)
        for nome, valor in zip(('features', 'acoes', 'recompensas', 'vantagens', 'log_velha', 'log_referencia'),
                               (x, a.astype(np.int64), r, vantagens, *logs)):
            object.__setattr__(self, nome, _imutavel(valor))


def _pesos(pesos) -> np.ndarray:
    p = np.asarray(pesos, dtype=np.float64)
    if p.shape != (5, 3) or not np.all(np.isfinite(p)):
        raise ValueError('Pesos devem ter forma (5,3) e valores finitos.')
    return p


def coletar_grupo(pesos: np.ndarray, referencia: np.ndarray, contexto: Contexto,
                  grupo: int, rng: np.random.Generator) -> RolloutGrupo:
    g = _inteiro(grupo, 2, 64, 'grupo')
    if contexto.fase != 'treino':
        raise ValueError('Não se coleta atualização em validação ou teste.')
    velha = log_softmax(contexto.features @ _pesos(pesos))
    ref = log_softmax(contexto.features @ _pesos(referencia))
    acoes = rng.choice(3, size=g, p=np.exp(velha))
    recompensas = np.array([verificar_recompensa(contexto, int(a)) for a in acoes])
    return RolloutGrupo(contexto.id, contexto.features, acoes, recompensas,
                        vantagens_grupo(recompensas), velha, ref)


def objetivo_e_gradiente(pesos: np.ndarray, rollout: RolloutGrupo,
                        clipping: float = .2, beta_kl: float = .025) -> tuple[float, np.ndarray, dict]:
    """Perda = -mean(min(r*A, clip(r)*A)) + beta*KL(pi||referência).

    KL exata para as três ações, não um estimador por ações amostradas. Rollout e
    vantagens permanecem fixos ao diferenciar, inclusive nos passes posteriores.
    """
    clip = _real(clipping, 1e-6, .9, 'clipping')
    beta = _real(beta_kl, 0., 1., 'beta_kl')
    w = _pesos(pesos)
    x = rollout.features
    logp = log_softmax(x @ w)
    p = np.exp(logp)
    delta = logp[rollout.acoes] - rollout.log_velha[rollout.acoes]
    if np.any(np.abs(delta) > 600):
        raise ValueError('Razão de importância fora do intervalo numérico suportado.')
    razoes = np.exp(delta)
    vant = rollout.vantagens
    cortadas = np.clip(razoes, 1.-clip, 1.+clip)
    termos = np.minimum(razoes*vant, cortadas*vant)
    # Só o ramo que limita uma vantagem positiva/negativa tem derivada zero.
    ativas = ~(((vant > 0.) & (razoes > 1.+clip)) | ((vant < 0.) & (razoes < 1.-clip)))
    dlogits = np.zeros(3)
    for acao, razao, vantagem, ativa in zip(rollout.acoes, razoes, vant, ativas):
        if ativa:
            score = -p.copy()
            score[acao] += 1.
            dlogits -= (razao * vantagem / len(vant)) * score
    log_diff = logp - rollout.log_referencia
    kl = float(np.dot(p, log_diff))
    dlogits += beta * p * (log_diff - kl)
    loss = -float(termos.mean()) + beta*kl
    grad = np.outer(x, dlogits)
    if not np.isfinite(loss) or not np.all(np.isfinite(grad)):
        raise ValueError('Objetivo ou gradiente não finito.')
    return loss, grad, dict(kl_exata=kl, fracao_cortada=float(np.mean(~ativas)),
        surrogate=float(termos.mean()), razao_minima=float(razoes.min()), razao_maxima=float(razoes.max()))


def avaliar(pesos: np.ndarray, contextos: Sequence[Contexto]) -> dict:
    if not contextos:
        raise ValueError('Avaliação exige contextos.')
    w = _pesos(pesos)
    retornos, corretas = [], []
    for c in contextos:
        p = np.exp(log_softmax(c.features @ w))
        otima = acao_otima(c)
        retornos.append(float(p[otima]))
        corretas.append(int(np.argmax(p) == otima))
    return dict(contextos=len(contextos), retorno_esperado_exato=float(np.mean(retornos)),
                acuracia_gulosa=float(np.mean(corretas)), retorno_oraculo=1.)


def treinar(contextos: Sequence[Contexto], grupo: int = 8, orcamento_acoes: int = 4096,
            semente: int = 41, taxa: float = .15, passes: int = 3,
            clipping: float = .2, beta_kl: float = .025) -> tuple[np.ndarray, dict]:
    g = _inteiro(grupo, 2, 64, 'grupo')
    budget = _inteiro(orcamento_acoes, 8, 32768, 'orcamento_acoes')
    seed = _inteiro(semente, 0, 2**32-1, 'semente')
    lr = _real(taxa, 1e-5, 1., 'taxa')
    epochs = _inteiro(passes, 1, 8, 'passes')
    clip = _real(clipping, 1e-6, .9, 'clipping')
    beta = _real(beta_kl, 0., 1., 'beta_kl')
    if budget % g or not contextos or any(c.fase != 'treino' for c in contextos):
        raise ValueError('Orçamento deve ser múltiplo de G; somente contextos de treino.')
    # Inicialização igual para ambos os grupos, referência congelada uniforme.
    pesos = np.zeros((5, 3))
    referencia = _imutavel(pesos)
    escolha = np.random.default_rng(np.random.SeedSequence([seed, 367]))
    amostragem = np.random.default_rng(np.random.SeedSequence([seed, g, 991]))
    sem_contraste = 0
    soma_recompensas = 0.
    fracoes = []
    for _ in range(budget // g):
        contexto = contextos[int(escolha.integers(len(contextos)))]
        rollout = coletar_grupo(pesos, referencia, contexto, g, amostragem)
        sem_contraste += int(not np.any(rollout.vantagens))
        soma_recompensas += float(rollout.recompensas.sum())
        for _ in range(epochs):
            _, grad, info = objetivo_e_gradiente(pesos, rollout, clip, beta)
            pesos -= lr*grad
            fracoes.append(info['fracao_cortada'])
    return pesos, dict(grupo=g, acoes_amostradas=budget, grupos_coletados=budget//g,
        updates_gradiente=epochs*(budget//g), passes_por_rollout=epochs,
        grupos_sem_contraste=sem_contraste, retorno_observado_treino=soma_recompensas/budget,
        fracao_cortada_media=float(np.mean(fracoes)), taxa=lr, beta_kl=beta,
        clipping=clip, rede_de_valor=False, pesos_finitos=bool(np.all(np.isfinite(pesos))))


def experimento(semente: int = 31, orcamento_acoes: int = 4096, repeticoes: int = 3) -> dict:
    seed = _inteiro(semente, 0, 2**32-4, 'semente')
    budget = _inteiro(orcamento_acoes, 8, 32768, 'orcamento_acoes')
    nrep = _inteiro(repeticoes, 1, 8, 'repeticoes')
    if budget % 8:
        raise ValueError('A comparação G=2/G=8 exige orçamento múltiplo de 8.')
    fases = gerar_contextos(seed)
    splits = {}
    for fase, contextos in fases.items():
        digest = hashlib.sha256()
        for c in contextos:
            digest.update(c.id.encode()); digest.update(c.features.tobytes())
        splits[fase] = dict(contextos=len(contextos), sha256=digest.hexdigest())
    resultados = []
    for replica in range(nrep):
        seed_treino = seed + replica
        for grupo in (2, 8):
            pesos, treino = treinar(fases['treino'], grupo, budget, seed_treino)
            resultados.append(dict(replica=replica, semente=seed_treino, **treino,
                avaliacoes={fase: avaliar(pesos, ctx) for fase, ctx in fases.items()},
                pesos_sha256=hashlib.sha256(pesos.tobytes()).hexdigest()))
    resumo = {}
    for grupo in (2, 8):
        linhas = [r for r in resultados if r['grupo'] == grupo]
        valores = [r['avaliacoes']['teste']['retorno_esperado_exato'] for r in linhas]
        resumo[str(grupo)] = dict(retorno_teste_media=float(np.mean(valores)),
            retorno_teste_desvio_populacional=float(np.std(valores)),
            acuracia_teste_media=float(np.mean([r['avaliacoes']['teste']['acuracia_gulosa'] for r in linhas])),
            acoes_por_replica=budget, updates_por_replica=linhas[0]['updates_gradiente'])
    return dict(modulo='rl_grupos', versao=1, ambiente='bandido contextual sintético de uma decisão',
        politica='softmax linear de cinco features, três ações', semente=seed,
        referencia='uniforme congelada', vantagem='(r-media)/(std_populacional+1e-8)',
        objetivo='surrogate clipped + KL exata(pi_atual || pi_referencia)',
        separacao=splits, validacao_usada_para_ajuste=False, teste_usado_para_ajuste=False,
        baseline_uniforme={fase: avaliar(np.zeros((5, 3)), ctx) for fase, ctx in fases.items()},
        resultados=resultados, resumo=resumo,
        limites=[
            'Nenhum LLM, treinamento de tokens, rede crítica, PPO completo ou RL off-policy.',
            'G=2 e G=8 têm ações iguais; número de contextos, updates, tempo e FLOPs diferem.',
            'Vantagem normalizada pelo próprio grupo pode introduzir viés; G=2 não elimina esse viés.',
            'KL é exata somente neste pequeno espaço de três ações; não prova estabilidade global.',
            'Contextos disjuntos vêm da mesma distribuição sintética; não demonstra transferência de domínio.',
            'Retornos esperados são exatos nos conjuntos finitos; médias de sementes não são garantia estatística.',
        ])


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--semente', type=int, default=31)
    parser.add_argument('--orcamento-acoes', type=int, default=4096)
    parser.add_argument('--repeticoes', type=int, default=3)
    parser.add_argument('--saida', type=Path)
    ns = parser.parse_args(args)
    resultado = experimento(ns.semente, ns.orcamento_acoes, ns.repeticoes)
    texto = json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False)
    if ns.saida:
        ns.saida.parent.mkdir(parents=True, exist_ok=True)
        ns.saida.write_text(texto + '\n', encoding='utf-8')
    print(texto)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
