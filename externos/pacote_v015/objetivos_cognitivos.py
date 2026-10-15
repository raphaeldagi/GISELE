"""Objetivos quadráticos SPD concretos; não modelos gerais de mundo/cognição."""
import math
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True,init=False,eq=False)
class QuadraticaAnisotropica:
    dimensao: int
    condicao: float
    matriz: np.ndarray
    def __init__(self,dimensao=8,condicao=10.,semente=31001):
        if type(dimensao) is not int or not 3<=dimensao<=64 or isinstance(condicao,bool) or not isinstance(condicao,(int,float)) or not math.isfinite(condicao) or not 1<=condicao<=1000 or type(semente) is not int or not 0<=semente<2**32:raise ValueError('Objetivo fora do orçamento.')
        rng=np.random.default_rng(semente);q,_=np.linalg.qr(rng.normal(size=(dimensao,dimensao)))
        a=(q*np.geomspace(1.,float(condicao),dimensao))@q.T;a=(a+a.T)/2
        object.__setattr__(self,'dimensao',dimensao);object.__setattr__(self,'condicao',float(condicao))
        object.__setattr__(self,'matriz',np.frombuffer(a.astype('<f8').tobytes(),dtype='<f8').reshape(a.shape))
    def __deepcopy__(self,memo):return self # objeto e buffer imutáveis
    @classmethod
    def de_matriz(cls,matriz,condicao):
        a=np.asarray(matriz,dtype=float)
        if a.ndim!=2 or a.shape[0]!=a.shape[1] or not 3<=len(a)<=64 or not np.isfinite(a).all() or not np.allclose(a,a.T,rtol=0,atol=1e-12):raise ValueError('Matriz inválida.')
        eig=np.linalg.eigvalsh(a)
        if eig[0]<1-1e-8 or eig[-1]>1000+1e-8 or isinstance(condicao,bool) or not isinstance(condicao,(int,float)) or not math.isfinite(condicao) or not 1<=condicao<=1000 or not np.isclose(eig[-1]/eig[0],condicao,rtol=1e-8):raise ValueError('Espectro inválido.')
        o=object.__new__(cls);object.__setattr__(o,'dimensao',len(a));object.__setattr__(o,'condicao',float(condicao))
        object.__setattr__(o,'matriz',np.frombuffer(a.astype('<f8').tobytes(),dtype='<f8').reshape(a.shape));return o
    def _diff(self,v,alvo):
        v=np.asarray(v,dtype=float);a=np.asarray(alvo,dtype=float)
        if v.shape!=(self.dimensao,) or a.shape!=v.shape or not np.isfinite(v).all() or not np.isfinite(a).all():raise ValueError('Vetores inválidos.')
        return v-a
    def custo(self,v,alvo):
        d=self._diff(v,alvo);f=float(d@self.matriz@d)
        if not math.isfinite(f) or f<0:raise ValueError('Custo não finito/negativo.')
        return f
    def gradiente(self,v,alvo):return 2*self.matriz@self._diff(v,alvo)
