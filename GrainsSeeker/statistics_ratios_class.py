from GrainsSeeker import ImageConfig as ic, grain_class as gc
import itertools


class Statistics:
    def __init__(self):
        self.imageArea = ic.height*ic.width
        self.borderNeighboursCountRatio = {}
        self.dispertionPhases = {}
        self.onePointProbability = {}

    def blr(self):
        colors = list(ic.colors_map.keys())
        colorsDict = {v: k for k, v in ic.colors_map.items()}

        for pair in itertools.combinations(colors, 2):
            combination = pair[0] + pair[1]
            self.borderNeighboursCountRatio[combination] = 0

        for i in range(ic.height):
            for j in range(ic.width - 1):
                color = [ic.image[i, j, 2], ic.image[i, j, 1], ic.image[i, j, 0]]
                nbcolorright = [ic.image[i, j + 1, 2], ic.image[i, j + 1, 1], ic.image[i, j + 1, 0]]
                if tuple(color) in colorsDict.keys() and tuple(nbcolorright) in colorsDict.keys():
                    phasename = colorsDict[tuple(color)]
                    nbrightphasename = colorsDict[tuple(nbcolorright)]
                    if phasename + nbrightphasename in self.borderNeighboursCountRatio.keys():
                        self.borderNeighboursCountRatio[phasename + nbrightphasename] += 1
                    if nbrightphasename + phasename in self.borderNeighboursCountRatio.keys():
                        self.borderNeighboursCountRatio[nbrightphasename + phasename] += 1

        for i in range(ic.height - 1):
            for j in range(ic.width):
                color = [ic.image[i, j, 2], ic.image[i, j, 1], ic.image[i, j, 0]]
                nbcolorunder = [ic.image[i + 1, j, 2], ic.image[i + 1, j, 1], ic.image[i + 1, j, 0]]
                if tuple(color) in colorsDict.keys() and tuple(nbcolorunder) in colorsDict.keys():
                    phasename = colorsDict[tuple(color)]
                    nbcolorunderphasename = colorsDict[tuple(nbcolorunder)]
                    if phasename + nbcolorunderphasename in self.borderNeighboursCountRatio.keys():
                        self.borderNeighboursCountRatio[phasename + nbcolorunderphasename] += 1
                    if nbcolorunderphasename + phasename in self.borderNeighboursCountRatio.keys():
                        self.borderNeighboursCountRatio[nbcolorunderphasename + phasename] += 1
        allborderpixels = sum(list(self.borderNeighboursCountRatio.values()))
        if allborderpixels != 0:
            for key, value in self.borderNeighboursCountRatio.items():
                self.borderNeighboursCountRatio[key] = value / allborderpixels

    def dispertion(self, grains, scale):
        area = self.imageArea * (scale ** 2)
        for phases in ic.colors_map.keys():
            self.dispertionPhases[phases] = 0
        for gc.Grain in grains:
            self.dispertionPhases[gc.Grain.phase] += 1
        for key, value in self.dispertionPhases.items():
            self.dispertionPhases[key] = value / area

    def onePointProb(self):
        colorsDict = {v: k for k, v in ic.colors_map.items()}
        for phase in ic.colors_map.keys():
            self.onePointProbability[phase] = 0
        for i in range(ic.height):
            for j in range(ic.width):
                color = (ic.image[i, j, 2], ic.image[i, j, 1], ic.image[i, j, 0])
                if color in colorsDict.keys():
                    phasename = colorsDict[color]
                    self.onePointProbability[phasename] += 1
        for key, value in self.onePointProbability.items():
            self.onePointProbability[key] = value / self.imageArea

    def returnRatios(self):
        return {'borderNeighbour': self.borderNeighboursCountRatio,
                'dispertionPhases': self.dispertionPhases,
                'onePointprobability': self.onePointProbability}
