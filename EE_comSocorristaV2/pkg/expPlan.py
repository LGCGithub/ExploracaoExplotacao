import numpy as np
from random import randint, shuffle
from state import State

class ExpPlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, homeState, model, name = "none", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do random plan por um unico agente.
        """
        self.walls = []
        self.possibilitiesFix = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
        self.possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
        #shuffle(self.possibilities)
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.model = model
        self.goalPos = goal
        self.actions = []
        self.visited = []
        self.victims = []
        self.timeHome = 0
        self.home = homeState
        self.goHome = 0
        base = State(self.home[0], self.home[1])
        self.visited.append(('N', base))
   
            
    def updateCurrentState(self, state):
         self.currentState = state

    def isPossibleToMove(self, toState):
        """Verifica se eh possivel ir da posicao atual para o estado (lin, col) considerando 
        a posicao das paredes do labirinto e movimentos na diagonal
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """

        # possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]

        result = self.model.isPossibleToMove(self.currentState.row, self.currentState.col, toState.row, toState.col)
        
        ## vai para fora do labirinto
        #if (toState.col < 0 or toState.row < 0):
        #if (toState.col >= self.maxColumns or toState.row >= self.maxRows):
        if result == -1:
            return False
        
        #if len(self.walls) == 0:
        #    return True
        
        ## vai para cima de uma parede
        #if (toState.row, toState.col) in self.walls:
        if result == -2:
            self.addNewWall(toState)
            return False

        ## se ja visitou
        for ps in self.possibilities:
            if (ps, toState) in self.visited:
                return False
    
        ## se for para a base e ainda nao for hora de voltar
        for ps in self.possibilities:
            if (toState.row, toState.col) == (self.home[0], self.home[1]) and self.goHome == 0:
                return False

        return True

    def addNewWall(self, state):
        for wall in self.walls:
            if (state.row, state.col) == (wall[0], wall[1]):
                return
        self.walls.append((state.row, state.col))
        return

    def invert(self, move):
        if move == 'N':
            return 'S'
        elif move == 'S':
            return 'N'
        elif move == 'L':
            return 'O'
        elif move == 'O':
            return 'L'
        elif move == 'NO':
            return 'SE'
        elif move == 'SE':
            return 'NO'
        elif move == 'NE':
            return 'SO'
        elif move == 'SO':
            return 'NE'
        
    def backtrack(self, possibilities, movePos):
        # encontra como chegou la:
        ind = len(self.visited)-1
        while(self.visited[ind][1] != self.currentState):
            ind -= 1
        lastMov = self.visited[ind][0]

        # invertendo a direcao de como chegou la:
        movDirection = self.invert(lastMov)
       
        state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
        if movDirection in self.possibilitiesFix[:3]:
            self.timeHome -= 1
        else:
            self.timeHome -= 1.5

        return movDirection, state


    def nextPosition(self):
         """ Seleciona uma direcao e calcula a posicao futura do agente --> DFS online com backtracking
         @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
         #possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
         movePos = {  "N" : (-1, 0),
                      "S" : (1, 0),
                      "L" : (0, 1),
                      "O" : (0, -1),
                      "NE" : (-1, 1),
                      "NO" : (-1, -1),
                      "SE" : (1, 1),
                      "SO" : (1, -1)}

         if self.timeLeft > self.timeHome and self.goHome != 1: # somando margem para garantir que ele volte a tempo
             self.goHome = 0
             # passa por todos as posicoes e ve qual a primeira possivel:
             for moveDirection in range(len(self.possibilities)):
                movDirection = self.possibilities[moveDirection]
                state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
                if(self.isPossibleToMove(state)):
                    # eh possivel ir para a posicao:
                    if movDirection in self.possibilitiesFix[:3]:
                        self.timeHome += 1
                    else:
                        self.timeHome += 1.5

                    self.visited.append((movDirection, state))
                    return movDirection, state

         # se nenhuma eh possivel, faz backtrack
         if self.timeLeft <= self.timeHome: self.goHome = 1
         return self.backtrack(self.possibilities, movePos)
        

    def chooseAction(self, timeLeft):
        """ Escolhe o proximo movimento de forma ordenada. 
        Eh a acao que vai ser executada pelo agente. 
        @return: tupla contendo a acao (direcao) e uma instância da classe State que representa a posição esperada após a execução
        """

        ## Tenta encontrar um movimento possivel dentro do tabuleiro 
        #result = self.randomizeNextPosition()
        self.timeLeft = timeLeft
        result = self.nextPosition()
        
        return result


    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   
    
     


        
       
        
        
