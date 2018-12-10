# round.py

from random import randint
from simulate import Simulation
from ga import Gene, GeneInfo, GeneEvolve

class Generation(object):
    """
    Let gene evolves.
    """
    def __init__(self, mapLayout, carmap, cars, geneNumber, roundNumber):
        self.mapLayout = mapLayout
        self.carmap = carmap
        self.cars = cars
        self.geneNumber = geneNumber
        self.roundNumber = roundNumber
        self.genes = [] # i_th entry represents i_th generation
        self.results = []
        self.initialFirstGenes()

    def initialFirstGenes(self):
        for _ in range(self.geneNumber):
                                    # [(intersecion #, [in_road to this intersecion])]
            self.genes.append(Gene(self.mapLayout.getTrafficLights()))

    def run(self):
        for i in range(self.roundNumber):
            result = []
            print('Generation ' + str(i + 1) + ':')
            for g in self.genes:
                print('\tGene String ' + g.geneStr)
                self.carmap.updateGeneInfo(GeneInfo(g))
                simulation = Simulation(self.cars, self.carmap)
                (total, average) = simulation.run(False, 10000)
                print('\tTotal: ' + str(total) + ' Average: ' + str(average) + '\n')
                if average == -1:
                    self.carmap.clearAllCars()
                    continue
                result.append((average, g))
            result.sort(key = lambda x:x[0])
            self.addResults(result[0:int(self.geneNumber / 2 )+ 1])
            self.evolve(result[0:int(self.geneNumber / 2 )+ 1])
        return self.results

    def evolve(self, result):
        newGene = []
        length = len(result) - 1
        for _ in range(self.geneNumber):
            (g1, g2) = (randint(0, length), randint(0, length))
            g = GeneEvolve.evolve(result[g1][1], result[g2][1])
            newGene.append(g)
        self.genes = newGene

    def addResults(self, result):
        # append min and max
        self.results.append((result[0][0], result[0][1].geneStr))
        self.results.append((result[-1][0], result[-1][1].geneStr))
