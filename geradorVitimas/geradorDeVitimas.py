import sys
import os
import time
import random

class Vict_gen:
    def __init__(self, mazeSizeX, mazeSizeY, qtdVictims, tempo_exploracao, tempo_socorrista):
        self.mazeSizeX = mazeSizeX
        self.mazeSizeY = mazeSizeY
        self.Te = tempo_exploracao
        self.Ts = tempo_socorrista
        ##self.qtdVictims = random.randint(5, mazeSizeY)
        self.qtdVictims = qtdVictims
        self.posVictims = []
        self.walls = []
        self.vitalSignals = []
        self.diffAccess = []
        self.generatorVictims()
        self.savePos()
        

    def generateWalls(self):
        walls = []
        qtd = random.randint(10, self.mazeSizeX*4)
        cont = 0
        while cont < qtd:
            row = random.randint(0, self.mazeSizeX-1)
            col = random.randint(0, self.mazeSizeY-1)
            if (row > 0 or col > 0) and (row, col) not in walls:
                self.walls.append((row, col))
                cont += 1
    
    def generatorVictims(self):
        self.generateWalls()
        qtdGen = 0
        while qtdGen < self.qtdVictims:
            pos = (random.randint(0, self.mazeSizeX-1), random.randint(0, self.mazeSizeY-1))
            if pos not in self.posVictims and (pos not in self.walls) and pos != (0,0):
                self.posVictims.append(pos)
                
                g_value = round(random.random(),2)
                gravidade = round(random.random() * 3.0 + 1.0) 

                self.vitalSignals.append([
                    qtdGen + 1,
                    round(random.random(),2),
                    round(random.random(),2),
                    round(random.random(),2),
                    round(random.random(),2),
                    g_value,
                    round(random.random() * 97 + 3,0),
                    int(gravidade)])
                
                qtdGen += 1
                
    def savePos(self):
        arquivo = open(os.path.join(".", "ambiente.txt"), "w")
        strSave = "Te " + str(self.Te) +"\n"
        strSave += "Ts " + str(self.Ts) + "\n"
        strSave += "Base 0,0\n"
        strSave += "XMax " + str(self.mazeSizeX) + "\n"
        strSave += "YMax " + str(self.mazeSizeY) + "\n"
        strSave += "Vitimas"
        for i in self.posVictims:
            strSave += " " + str(i[0]) + "," + str(i[1])
        strSave += "\nParede"
        for i in self.walls:
            strSave += " " + str(i[0]) + "," + str(i[1])
        arquivo.writelines(strSave)
        arquivo.close()
        print("gerou new ambiente.txt\n")

        strSave=""
        sinaisvitais = open(os.path.join(".", "sinaisvitais.txt"), "w")
        for i in self.vitalSignals:
            strSave += str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3]) + " " + str(i[4]) + " " + str(i[5]) + " " + str(i[6]) + " " + str(i[7]) + "\n"
        sinaisvitais.writelines(strSave)
        sinaisvitais.close()
        print("gerou new sinaisvitais.txt\n")



def main():
    nLinhas = 20
    nColunas = 20
    nVitimas = 42
    tempo_exploracao = 600
    tempo_socorrista = 400

    vict = Vict_gen(nLinhas, nColunas, nVitimas, tempo_exploracao, tempo_socorrista)

        
if __name__ == '__main__':
    main()



