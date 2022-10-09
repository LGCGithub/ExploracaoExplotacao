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

        self.map = np.ones((maxRows, maxColumns))
        self.map[self.goalPos.col][self.goalPos.row] = 0
        self.moves = []
   
            
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
        start = State(state.col, state.row)
        target = State(self.goalPos.col, self.goalPos.row)
        self.timeHome = self.AEstrela(start, target)[0][1] + 1.5

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

         print(self.timeHome, self.timeLeft)
         if self.timeHome >= self.timeLeft:
            self.goHome = 1

         if self.goHome == 1 and len(self.moves) == 0:
            start = State(self.currentState.col, self.currentState.row)
            target = State(self.goalPos.col, self.goalPos.row)
            self.criarPlano(start, target)
            
         if self.goHome == 1 and len(self.moves) != 0:
            return self.moves.pop()


         if self.timeLeft > self.timeHome and self.goHome != 1: # somando margem para garantir que ele volte a tempo
             self.goHome = 0
             # passa por todos as posicoes e ve qual a primeira possivel:
             for moveDirection in range(len(self.possibilities)):
                movDirection = self.possibilities[moveDirection]
                state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])
                if(self.isPossibleToMove(state)):
                    # eh possivel ir para a posicao:
                    self.map[state.col][state.row] = 0
                    start = State(state.col, state.row)
                    target = State(self.goalPos.col, self.goalPos.row)
                    self.timeHome = self.AEstrela(start, target)[0][1] + 1.5
                
                    self.visited.append((movDirection, state))
                    return movDirection, state

         # se nenhuma eh possivel, faz backtrack
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
    
    def AEstrela(self, start, target):
        open = []
        closed = []

        def euclidianDistance(p1, p2):
            return ((p1.row - p2.row)**2 + (p1.col - p2.col)**2)**(0.5)

        open.append([start, 0.0, euclidianDistance(start, target), start])

        costs = np.ones((self.maxRows, self.maxColumns)) * 100000.0
        costs[start.row][start.col] = euclidianDistance(start, target) + 0.0

        while len(open) != 0:
            current = min(open, key = lambda t: t[1])
            open.remove(current)
            closed.append(current)

            currentState, currentCostG, currentCostH, currentParent = current

            if currentState == target:
                return current, closed

            currentState = current[0]
            neighbors = []

            neighbors.append(State(currentState.row + 1, currentState.col)) # N
            neighbors.append(State(currentState.row, currentState.col + 1)) # E
            neighbors.append(State(currentState.row - 1, currentState.col)) # S
            neighbors.append(State(currentState.row, currentState.col - 1)) # W

            neighbors.append(State(currentState.row + 1, currentState.col + 1)) # NE
            neighbors.append(State(currentState.row - 1, currentState.col + 1)) # SE
            neighbors.append(State(currentState.row - 1, currentState.col - 1)) # SW
            neighbors.append(State(currentState.row + 1, currentState.col - 1)) # NW

            for neighbor in neighbors:
                closedStates, closedCostsG, closedCostsH, closedParents = list(map(list, zip(*closed)))

                def isTransversable(p1, p2, map):
                    # Horizontal, vertical
                    cost = 1.0

                    if (p2.col < 0 or p2.row < 0):
                        return False, cost

                    if (p2.col >= self.maxColumns or p2.row >= self.maxRows):
                        return False, cost
                
                    if map[p2.row][p2.col] == 1:
                        return False, cost

                    # Diagonal
                    delta_row = p2.row - p1.row
                    delta_col = p2.col - p1.col
                    ## o movimento eh na diagonal
                    if (delta_row != 0 and delta_col != 0):
                        cost = 1.5
                        
                        # Pode dar problema
                        if map[p1.row + delta_row][p1.col] == 1 and map[p1.row][p1.col + delta_col] == 1:
                            return False, cost

                    return True, cost

                transversable, cost = isTransversable(currentState, neighbor, self.map)
                if not transversable or neighbor in closedStates:
                    continue

                openStates = []
                openCosts = []
                openParents = []

                try:
                    openStates, openCostsG, openCostsH, openParents = list(map(list, zip(*open)))
                except:
                    pass

                if neighbor not in openStates or costs[neighbor.row][neighbor.col] > currentCostG + cost:
                    costs[neighbor.row][neighbor.col] = currentCostG + cost
                    if neighbor not in openStates:
                        open.append([neighbor, currentCostG + cost, euclidianDistance(neighbor, target), currentState])
                    else:
                        index = openStates.index(neighbor)
                        open[index][1] = currentCostG + cost
                        open[index][2] = euclidianDistance(neighbor, target)
                        open[index][3] = currentState

        return [(-1, -1, -1, -1), (-1, -1, -1, -1)]
        # Isso nunca deve acontecer
        # Significa que não existe caminho entre a posição atual e o objetivo
        # Mapa mal feito

        # Cria uma lista de ações com base em um start e um target (start -> target)
    # As ações guiam o agente até o target
    # Essencialmente transforma o caminho calculado no A* em algo para ser executado pelo agente
    def criarPlano(self, atual, next):
        
        #atual = self.goalPos
        #victim = self.victims[21][0]
        #victimCoord = State(victim[0], victim[1])
        victimCoord = next
        #print(atual, victimCoord)
        current, closed = self.AEstrela(atual, victimCoord)

        currentState, currentCostG, currentCostH, currentParent = current
        closedStates, closedCostsG, closedCostsH, closedParents = list(map(list, zip(*closed)))

        def getOrientation(parent, current):
            possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
            movePos = [ (-1, 0),
                    (1, 0),
                    (0, 1),
                    (0, -1),
                    (-1, 1),
                    (-1, -1),
                    (1, 1),
                    (1, -1)]

            yp = parent.row
            xp = parent.col
            yc = current.row
            xc = current.col

            for index in range(0, len(movePos)):
                y = movePos[index][1]
                x = movePos[index][0]
                if yp + y == yc and xp + x == xc:
                    return possibilities[index]

        moves = []
        temp = State(currentState.col, currentState.row)
        moves.append((getOrientation(currentParent, currentState), temp)) # Primeiro passo

        while currentParent != currentState:
            index = closedStates.index(currentParent)
            currentState, currentCostG, currentCostH, currentParent = closed[index]
            temp = State(currentState.col, currentState.row)
            moves.append((getOrientation(currentParent, currentState), temp))

        movesAux = []
        for move in moves:
            movesAux.append(move)
        movesAux.pop()

        movesAux.extend(self.moves)
        self.moves = movesAux
     


        
       
        
        
