"""Gradientes, isolamento, orçamento adversarial e limites da observação recursiva."""
import asyncio
import unittest
from unittest.mock import patch
import numpy as np
import sete_camadas as s


class TestesSeteCamadas(unittest.TestCase):
    def artefato(self):return s.Artefato(s.RedeSeteCamadas(20,6),np.random.default_rng(27).normal(size=4))

    def test_identidade_cosseno_duplicado(self):
        xs=np.array([[1,0,0,0],[0,1,0,0],[-1,0,0,0]])
        f,_,_=s.geometria(xs,[1,0,0,0])
        np.testing.assert_allclose(f[:,4],[1,0,-1]);np.testing.assert_allclose(f[:,5],[1,-1,1])

    def test_origem_e_referencia_nula(self):
        f,dc,_=s.geometria(np.zeros((1,4)),np.zeros(4))
        self.assertTrue(np.isfinite(f).all());np.testing.assert_array_equal(dc,0)

    def test_referencia_recursiva(self):
        v=s.vetor_recursivo([1,0,0,0],[0,1,0,0])
        self.assertAlmostEqual(np.linalg.norm(v),1)
        with self.assertRaises(ValueError):s.vetor_recursivo(v,v,2)

    def test_derivada_geometrica(self):
        x=np.array([[.4,.7,-.2,1.1]]);r=np.array([.3,-.2,.8,.1]);h=1e-6
        f,dc,c=s.geometria(x,r)
        for j in range(4):
            xp=x.copy();xm=x.copy();xp[0,j]+=h;xm[0,j]-=h
            fp=s.geometria(xp,r)[0];fm=s.geometria(xm,r)[0]
            self.assertAlmostEqual(float((fp[0,4]-fm[0,4])/(2*h)),dc[0,j],places=7)
            self.assertAlmostEqual(float((fp[0,5]-fm[0,5])/(2*h)),float(4*c[0,0]*dc[0,j]),places=7)

    def test_sete_mapas_e_gradientes_pesos(self):
        r=s.RedeSeteCamadas(7,6);x=np.random.default_rng(3).normal(size=(3,6));y=np.array([[1],[0],[1]])
        _,g,_=r.gradientes(x,y);self.assertEqual(len(r.parametros),7);h=1e-6
        for i,(w,b) in enumerate(r.parametros):
            for arr,grad,idx in ((w,g[i][0],(0,0)),(b,g[i][1],(0,0))):
                old=arr[idx];arr[idx]=old+h;lp=r.gradientes(x,y)[0]
                arr[idx]=old-h;lm=r.gradientes(x,y)[0];arr[idx]=old
                self.assertAlmostEqual((lp-lm)/(2*h),grad[idx],places=7)

    def test_gradiente_entrada_composta(self):
        a=self.artefato();x,y=s.dados(8,4);g=a.gradiente_entrada(x,y);h=1e-6
        for i in range(4):
            for j in range(4):
                xp=x.copy();xm=x.copy();xp[i,j]+=h;xm[i,j]-=h
                lp=a.rede.gradientes(s.geometria(xp,a.referencia)[0],y)[0]
                lm=a.rede.gradientes(s.geometria(xm,a.referencia)[0],y)[0]
                self.assertAlmostEqual((lp-lm)/(2*h),g[i,j],places=7)

    def test_ataque_zero_preserva_entrada(self):
        x,y=s.dados(8,15);np.testing.assert_array_equal(self.artefato().atacar(x,y,0),x)

    def test_orcamento_ataque(self):
        x,y=s.dados(8,15);a=self.artefato().atacar(x,y,.15)
        self.assertLessEqual(float(np.max(np.abs(a-x))),.15+1e-12)

    def test_ataque_guarda_pior_caso(self):
        a=self.artefato();x,y=s.dados(120,400);ad=a.atacar(x,y,.5)
        def perdas(v):
            z=a.rede.frente(s.geometria(v,a.referencia)[0])[0]
            return np.logaddexp(0,z)-y*z
        self.assertTrue(np.all(perdas(ad)>=perdas(x)-1e-12))
        self.assertLessEqual(s.avaliar(a,x,y,.5)['adversa'],s.avaliar(a,x,y,.5)['acuracia'])

    def test_snapshot_imutavel_e_isolado(self):
        a=self.artefato();f=a.congelada();old=f.rede.parametros[0][0].copy()
        a.rede.parametros[0][0][0,0]+=1
        np.testing.assert_array_equal(f.rede.parametros[0][0],old)
        with self.assertRaises(ValueError):f.rede.parametros[0][0][0,0]=9
        with self.assertRaises(ValueError):f.referencia[0]=9

    def test_equivalencia_sincrona_assincrona(self):
        a=self.artefato();b=a.copia();x,y=s.dados(44,50)
        sync=asyncio.run(s.avaliar_par(a,b,x,y,.15,'sincrono'))
        async_=asyncio.run(s.avaliar_par(a,b,x,y,.15,'assincrono'))
        self.assertEqual(sync,async_)

    def test_calibrador_faixas_e_contagem(self):
        c=s.Confiabilidade();p=np.array([[.01],[.99],[.5]]);y=np.array([[0],[1],[0]])
        c.ajustar(p,y);q=c.prever(p)
        self.assertEqual(float(c.contagens.sum()),3)
        self.assertTrue(((q>=0)&(q<=1)).all())
        self.assertAlmostEqual(q[0,0],.75)

    def test_metacognicao_evidencia_unica(self):
        m=s.MetaRecursiva();base=dict(acuracia=.8,adversa=.6)
        cand=dict(acuracia=.82,adversa=.7,brier=.1,brier_confiabilidade=.2,probabilidade_media=.5,probabilidade_acerto=.8)
        r=m.observar(1,base,cand,True,'versa');self.assertEqual(m.sucessos+m.falhas,3)
        with self.assertRaises(ValueError):m.observar(1,base,cand,True,'versa')
        self.assertTrue(0<=r['metacognicao_dentro_da_probabilidade']<=1)

    def test_dez_niveis_e_percurso_invertido(self):
        m=s.MetaRecursiva();base=dict(acuracia=.8,adversa=.6)
        cand=dict(acuracia=.82,adversa=.7,brier=.1,brier_confiabilidade=.2,probabilidade_media=.5,probabilidade_acerto=.8)
        r=m.observar(1,base,cand,True,'reversa');node=r['resultado_metacognitivo'];ids=[]
        while node:ids.append(node['nivel']);node=node['observa']
        self.assertEqual(ids,list(range(10,0,-1)));self.assertEqual(r['percurso'],ids)

    def test_inversao_de_perguntas(self):
        m=s.MetaRecursiva();a=m.plano(1,'versa');b=m.plano(2,'reversa')
        self.assertNotEqual(a['pergunta'],b['pergunta'])
        self.assertEqual(a['papeis'][0],'lógica criativa pergunta')
        self.assertEqual(b['papeis'][0],'criatividade lógica pergunta')

    def test_revisao_recursiva_detecta_erro_anterior(self):
        node=dict(nivel=1,resultado=dict(prob_acerto=1.2),observa=None)
        r=s.MetaRecursiva.revisar_anterior(node)
        self.assertFalse(r['consistente']);self.assertTrue(r['motivos'])
        node['resultado']['prob_acerto']=.8
        self.assertTrue(s.MetaRecursiva.revisar_anterior(node)['consistente'])

    def test_treino_reduz_perda(self):
        a=self.artefato();x,y=s.dados(10,128);f=s.geometria(x,a.referencia)[0]
        before=a.rede.gradientes(f,y)[0];a.treinar(x,y,25,.12,.25,.15,3)
        self.assertLess(a.rede.gradientes(f,y)[0],before)

    def test_configuracao_limitada(self):
        with self.assertRaises(ValueError):s.Configuracao(ciclos=1000).validar()
        with self.assertRaises(ValueError):s.Configuracao(epsilon=float('nan')).validar()

    def test_confirmacao_uma_vez_apos_selecao(self):
        calls=[];original=s.dados
        def gerar(seed,n):calls.append(seed);return original(seed,n)
        with patch.object(s,'dados',side_effect=gerar):
            r=asyncio.run(s.executar(s.Configuracao(ciclos=2,epocas=2)))
        self.assertEqual(calls,[53,65,79,95]);self.assertTrue(r['confirmacao_consultada_uma_vez'])
        self.assertEqual([t['modo'] for t in r['tracos']],['sincrono','assincrono'])


if __name__=='__main__':unittest.main(verbosity=2)
