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

def main():
    # Lê arquivo config.txt
    arq = open(os.path.join("config_data","ambiente.txt"),"r")
    
    arq_texto = []
    for line in arq:
        arq_texto.append(line.split(" ")[1:])

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
        #time.sleep(0.3) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()    
    
    # pegando as vitimas:
    # array de victims, com tupla de coords, id e nivel critico (sendo gravidade e a classe):((y,x), id, grav, classe)
    victims = explorador.victims

    # so pra ver elas:
    #print(len(victims))
    #for i in range(len(victims)):
        #print(victims[i])

    # print("==================================")
    # pegando as paredes:
    # array de walls, com tupla de int (x, y)
    walls = explorador.walls

    # so pra ver elas:
    # print(len(walls))
    #for i in range(len(walls)):
     #    print(walls[i])

    visited = []
    
    for movDirection, state in explorador.plan.visited:
        visited.append(state) # State(y, x)
        print(state)

    for victim in victims:
        state = State(victim[0][0], victim[0][1])
        if state not in visited:
            visited.append(state)


    

    # A*  // Feito
    # Matriz de distancias entre vitimas // Feito
    # Algoritmo genético / busca local caixeiro viajante // Feito
    # Executar caminho // Tentando

    socorrista = AgentScrt(model, configDict, base, victims, visited)

    ## Ciclo de raciocínio do agente
    socorrista.deliberate()
    while socorrista.deliberate() != -1:
        model.draw()
        time.sleep(0.3) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()  


if __name__ == '__main__':
    main()
