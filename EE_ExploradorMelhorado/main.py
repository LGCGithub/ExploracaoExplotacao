import sys
import os
import time
import numpy as np

## Importa as classes que serao usadas
sys.path.append(os.path.join("pkg"))
from model import Model
from agentExp import AgentExp

from agentScrt import AgentScrt
from state import State


## Metodo utilizado para permitir que o usuario construa o labirindo clicando em cima
def buildMaze(model):
    model.drawToBuild()
    step = model.getStep()
    while step == "build":
        model.drawToBuild()
        step = model.getStep()
    ## Atualiza o labirinto
    model.updateMaze()

def setVictimsList(model, maze):
    vict = maze.victims #matriz
    victimsList = []
    for row in range(len(vict)):
        for col in range(len(vict[row])):
            id = vict[row][col]
            if id != 0: #tem vitima
                (coll, roww) = (col, row)
                coord = (coll, roww)
                vitalInfo = model.getVictimVitalSignals(id)
                vitalInfo = vitalInfo[0]
                grav = vitalInfo[len(vitalInfo) - 2]
                classe = vitalInfo[len(vitalInfo) - 1]
                victim = (coord, id, grav, classe)
                victimsList.append(victim)
    return victimsList

def getVictimsByGrav(victims):
    vicByGrav = [0, 0, 0, 0]
    for victim in victims:
        gravClass = int(victim[3])
        vicByGrav[gravClass - 1] += 1

    return vicByGrav

def calculateStat(victimsByGrav, victims):
    vcByGrv = getVictimsByGrav(victims)
    vg = 0
    div = 0
    for i in range(len(vcByGrv)):
        vg += (len(vcByGrv)-i)*vcByGrv[i]
        div += (len(victimsByGrav)-i)*victimsByGrav[i]

    vg = vg / div
    return vg


def main():
    # Lê arquivo config.txt
    arq = open(os.path.join("config_data","ambiente.txt"),"r")
    
    arq_texto = []
    for line in arq:
        arq_texto.append(line.split(" ")[1:])
        # arq_texto.append(line.split(",")[1:])

    configDict = {}

    configDict["Te"] = int(arq_texto[0][0])
    configDict["Ts"] = int(arq_texto[1][0])
    configDict["maxCol"] = int(arq_texto[3][0])
    configDict["maxLin"] = int(arq_texto[4][0])

    base = (int(arq_texto[2][0].split(",")[0]), int(arq_texto[2][0].split(",")[1]))

    print("dicionario config: ", configDict)

    # Cria o ambiente (modelo) = Labirinto com suas paredes
    mesh = "square"

    ## nome do arquivo de configuracao do ambiente - deve estar na pasta <proj>/config_data
    loadMaze = "ambiente"

    model = Model(configDict["maxLin"], configDict["maxCol"], mesh, loadMaze)
    buildMaze(model)

    model.maze.board.posAgent = base
    model.maze.board.posGoal = base
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model.setAgentPos(model.maze.board.posAgent[0],model.maze.board.posAgent[1])
    model.setGoalPos(model.maze.board.posGoal[0],model.maze.board.posGoal[1])  
    model.draw()

    # Cria um agente
    explorador = AgentExp(model, configDict, base)

    ## Ciclo de raciocínio do agente
    explorador.deliberate()
    while explorador.deliberate() != -1:
        model.draw()
        time.sleep(0.05) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()    
    
    # pegando as vitimas: array de victims, com tupla de coords, id e nivel critico (sendo gravidade e a classe):((y,x), id, grav, classe)
    victimsExp = explorador.victims

    walls = explorador.walls

    visited = []
    
    for movDirection, state in explorador.plan.visited:
        visited.append(state) # State(y, x)
        #print(state)

    for victim in victimsExp:
        state = State(victim[0][1], victim[0][0])
        if state not in visited:
            visited.append(state)

    # A*  // Feito
    # Matriz de distancias entre vitimas // Feito
    # Algoritmo genético / busca local caixeiro viajante // Feito
    # Executar caminho // Feito

    socorrista = AgentScrt(model, configDict, base, victimsExp, visited)


    ## Ciclo de raciocínio do agente
    socorrista.deliberate()
    while socorrista.deliberate() != -1:
        model.draw()
        time.sleep(0.1) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()  

    victimsSav = socorrista.victimsSaved

    allVictims = setVictimsList(model, model.maze)

    nVitTotal = len(allVictims)
    nVitTotalGrav = getVictimsByGrav(allVictims)
    nVitExp = len(victimsExp)
    nVitSav = len(victimsSav)
    tempTotExp = explorador.maxT
    tempTotSav = socorrista.maxT
    tempExp = (explorador.maxT - explorador.tl)
    tempSav = (socorrista.maxT - socorrista.ts)

    pve = nVitExp / nVitTotal
    tev = tempExp / nVitExp
    veg = calculateStat(nVitTotalGrav, victimsExp)

    pvs = nVitSav / nVitTotal
    tvs = tempSav / nVitSav
    vsg = calculateStat(nVitTotalGrav, victimsSav)

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    print('~~~ Metricas: ~~~')
    print('Numero total de vitimas: ', nVitTotal)
    print('Tempo total para exploracao: ', tempTotExp)
    print('Tempo total para salvamento: ', tempTotSav)

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    print('~~~ Resultados do explorador: ~~~')
    print('ve =', nVitExp, ' te =', tempExp)
    print('pve = ', pve, ' tev = ', tev)
    print('veg = ', veg)

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    print('~~~ Resultados do socorrista: ~~~')
    print('vs =', nVitSav, ' ts =', tempSav)
    print('pvs = ', pvs, ' tvs = ', tvs)
    print('vsg = ', vsg)



if __name__ == '__main__':
    main()
