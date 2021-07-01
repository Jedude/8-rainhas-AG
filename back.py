import numpy as np
import random
from random import uniform
#import tkinter as tk
import sys
from operator import attrgetter

probabilidadeMutacao=0.30
nRainhas=8
POPULACAO= 100
populacao=[]
MAX_GERACAO=10000
DIZIMACAO=False

class cromossomo:
    def __init__(self):
        self.posicoes = None
        self.aptidao = None
        self.probabilidadeS = None

    def setPosicoes(self, val):
        self.posicoes = val

    def setAptidao(self, aptidao):
        self.aptidao = aptidao

    def setProbabilidade(self, val):
        self.probabilidadeS = val

    def getPosicoes(self):
        return self.posicoes

    def getAptidao(self):
        return self.aptidao

    def getProbabilidade(self):
        return self.probabilidadeS

#CALCULA APTIDAO DE CADA INIDIVIDUO
def calculaAptidao(cromo=None):
    conflitos=0
    #conflitos horizontais
    conflitosLinhas = abs(len(cromo) - len(np.unique(cromo)))

    #conflitos diagonais
    for i in range(len(cromo)):
        for j in range(i,len(cromo)):
            if (i != j):
                dx = abs(i - j)
                dy = abs(cromo[i] - cromo[j])
                if (dx == dy):
                    conflitos += 1

    conflitos+=conflitosLinhas
    return 28 - conflitos

#GERANDO POPULACÂO INICIAL
def populacaoInicial(tamanho):
    global POPULACAO
    POPULACAO=tamanho
    populacao=[cromossomo() for i in range(tamanho)]
    #individuo=cromossomo()
    for i in range(tamanho):
        """
        #individuo.posicoes=random.sample(range(0, 8), 8)
        individuo.posicoes = np.arange(nRainhas)
        individuo.posicoes = np.random.randint(8, size=8)
        individuo.setAptidao(calculaAptidao(individuo.posicoes))
        populacao.append(individuo)
        """
        teste=np.arange(nRainhas)
        np.random.shuffle(teste)
        list(teste)
        populacao[i].setPosicoes(teste)
        populacao[i].setAptidao(calculaAptidao(populacao[i].posicoes))
    return populacao

def mutacao(filho):
    n=len(filho)
    #print(filho)
    posicao = random.randint(0, n/2-1)
    novoValor = filho[posicao]
    posicao2= random.randint(n/2, n-1)
    #if filho[posicao] != novoValor:
    #    filho[posicao]=novoValor
    #    break
    filho[posicao] = filho[posicao2]
    filho[posicao2]=novoValor
    #print("Mutou")
    #print(filho)
    return filho

def reproducao(pai, mae):
    globals()
    n=len(pai.posicoes)
    c = np.random.randint(1, 7)
    filho = cromossomo()
    filho.posicoes = []
    partepai=[]
    partemae=[]
    for i in range(n):
        if (i < c):
            partepai.append(pai.posicoes[i])
    ppai=set(partepai)
    pmae=set(mae.posicoes)
    te=pmae-ppai
    tp=c
    for i in range(c,n):
        if mae.posicoes[i] not in partepai:
            partemae.append(mae.posicoes[i])
    for i in range(n):
        if mae.posicoes[i] not in partepai and mae.posicoes[i] not in partemae:
            partemae.append(mae.posicoes[i])

    filho.posicoes = np.concatenate((partepai,partemae))
    filho.setAptidao(calculaAptidao(filho.posicoes))
    #print(partepai, partemae)
    #print(filho.posicoes)

    """
    for i in range(n):
        if(i<c):
            filho.posicoes[i]=pai.posicoes[i]
        if(i>=c):
            filho.posicoes[i]=mae.posicoes[i]
    filho.posicoes = np.array(filho.posicoes)
    print(filho.posicoes)
    print(pai.posicoes,mae.posicoes)
    pai.posicoes=np.array(pai.posicoes)
    partepai=pai.posicoes[0:c]
    partemae=mae.posicoes[c:]
    filho.posicoes=np.concatenate((pai.posicoes,mae.posicoes))
    #filho.posicoes.extend(pai.posicoes[0:c])
    #filho.posicoes.extend(mae.posicoes[c:n])
    filho.setAptidao(calculaAptidao(filho.posicoes))
    """
    return filho

def gerarIndividuo():
    individuo=cromossomo()
    ar = np.arange(nRainhas)
    np.random.shuffle(ar)
    list(ar)
    individuo.setPosicoes(ar)
    individuo.setAptidao(calculaAptidao(individuo.posicoes))
    return individuo

def escolherPais():
    globals()
    pai,mae= None, None
    somaAptidao = np.sum([i.aptidao for i in populacao])
    aptidaoPop=[]
    testeP=0
    for i in populacao:
        try:
            i.probabilidadeS = i.aptidao / (somaAptidao * 1.0)
            #print(i.probabilidade)
        except:
            print("erro soma")
            i.probabilidadeS=0.0
        aptidaoPop.append(i.probabilidadeS)
    #print(aptidaoPop)
    while(True):
        while (True):
            #randomP=np.random.rand()
            try:
                #menor = min(aptidaoPop)
                maior = max(aptidaoPop)
                testeP = uniform(0, maior)
                #print(testeP)
            except:
                print("erro Probabilidade")
                testeP=0
            paisPromissores = [i for i in populacao if i.probabilidadeS >= testeP]
            try:
                tp = np.random.randint(len(paisPromissores))
                pai = paisPromissores[tp]
                #print("pai: ",pai.posicoes)
                break
            except:
                pass
        while (True):
            #randomM=np.random.rand()
            try:
                menor = min(aptidaoPop)
                maior = max(aptidaoPop)
                testeP = uniform(0, maior)
                # print(testeP)
            except:
                testeP=0
                print("erro Probabilidade 423")
            maesPromissores = [i for i in populacao if i.probabilidadeS >= testeP]
            try:
                t = np.random.randint(len(maesPromissores))
                mae = maesPromissores[t]
                #print("mae: ",mae.posicoes)
                break
            except:
                pass
        if(not(np.array_equal(mae.posicoes,pai.posicoes))):
            break
    aptidaoPop.clear()
    #print("pai:",pai.posicoes)
    #print("mae:",mae.posicoes)
    return pai, mae
def gerarPopulacao(geracoes):
    globals()
    novaPopulacao=[]
    for i in range(POPULACAO):
        #try:
        pai, mae = escolherPais()
        crianca= cromossomo()
        crianca = reproducao(pai, mae)
        random = np.random.rand()
        if(DIZIMACAO):
            for j in range(len(novaPopulacao)):
                if crianca.posicoes in novaPopulacao[j].posicoes:
                    crianca = gerarIndividuo()
        if (probabilidadeMutacao >= random):
            crianca = mutacao(crianca.posicoes)
        try:
            crianca.setAptidao(calculaAptidao(crianca.posicoes))
            novaPopulacao.append(crianca)
            #print("crianca: ", crianca.posicoes)
        except:
            #print("Erro reproducao")
            i-=1
        #except:
            #print("erro reproducao")
    #print(len(novaPopulacao))
    return novaPopulacao


#populacao=populacaoInicial(10)
geracoes=1
DIZIMACAO=True
resultado=[0,0,0,0,0,0,0,0]

def AG():
    global geracoes
    global populacao
    global resultado
    resolver = True
    populacao = populacaoInicial(POPULACAO)
    while (resolver):
        for i in populacao:
            #print("teste 4")
            #print(i.posicoes)
            if i.aptidao== 28:
                resultado= i.posicoes
                print("resultado:" ,resultado)
                print("Quantidade de gerações: ",geracoes)
                print("Quantidade de individuos: ",geracoes*POPULACAO)
                resolver=False
                break
        #print("geracoes: ",geracoes)
        populacao = gerarPopulacao(geracoes)
        geracoes += 1

        if geracoes >= MAX_GERACAO:
            resolver = False

AG()




