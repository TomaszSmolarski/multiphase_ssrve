from GrainsSeeker import ratios_class
from GrainsSeeker import ImageConfig
import cv2
import math


class Grain(ratios_class.Ratios):
    def __init__(self, edge, phase):
        self.edge = edge
        self.phase = phase
        self.domain = []
        self.perimeter = len(edge)  # obwód - długość
        self.area = 0
        self.getArea()
        self.centerOfMass = []
        self.centerOfMassLocal = []
        self.distanceFromCenterPower = 0
        self.distanceFromCenter = 0
        self.minDistanceFromEgdeSum = 0
        self.minDistaceCenterEdge = 0
        self.maxDistaceCenterEdge = 0
        self.maxDistancePoints = 0
        self.maxDistanceVectorCoords = []
        self.VectorPerpendicularLength = 0
        self.LH = 0
        self.LW = 0
        super().__init__()

    def startCalculating(self):
        self.calculateComDistancesHightWidth()
        self.calculateRatios()

    def calculateComDistancesHightWidth(self):
        self.calculateDistancesSumFromCenter()
        self.calculateHeightWidth()
        self.calculateMaxMinFromCenter()
        self.calculateMaxDistanceGrain()
        self.findMinDistSum()
        self.findVectorPerendicular()

    def getArea(self):  # powierzchnia to domain(współrzędne), area to ilosc punktow
        domain = []
        for i in range(ImageConfig.width):
            for j in range(ImageConfig.height):
                if cv2.pointPolygonTest(self.edge, (i, j), measureDist=False) >= 0:
                    domain.append([i, j])
        self.domain = domain
        self.area = len(self.domain)

    def findCoM(self, offsetX=0, offsetY=0):  # srodek ciezkosci
        allx = 0
        ally = 0
        for i in range(self.area):
            allx += self.domain[i][0]  # suma wspołrzędnych x pola
            ally += self.domain[i][1]  # suma wspołrzędnych y pola
        meanX = int(allx / self.area)
        meanY = int(ally / self.area)
        self.centerOfMass.append(meanX)
        self.centerOfMass.append(meanY)
        self.centerOfMassLocal.append(meanX - offsetX*ImageConfig.widthOffset)
        self.centerOfMassLocal.append(meanY - offsetY*ImageConfig.heightOffset)

    def calculateDistancesSumFromCenter(
            self):  # suma odleglosci od srodka ciezkosci, jeden to kazda odleglosc podniesiona do kwadratu
        distanceSumPower = 0
        distanceSum = 0
        for p in self.domain:
            distpower = (self.centerOfMass[0] - p[0]) ** 2 + (self.centerOfMass[1] - p[1]) ** 2
            dist = math.sqrt(distpower)
            # distanceSumPower += self.calculateDistance(p[0], p[1], self.centerOfMass[0], self.centerOfMass[1]) ** 2
            distanceSumPower += distpower
            # distanceSum += self.calculateDistance(p[0], p[1], self.centerOfMass[0], self.centerOfMass[1])
            distanceSum += dist
        self.distanceFromCenter = distanceSum
        self.distanceFromCenterPower = distanceSumPower

    def findMinDistSum(self):  # suma minimalnych odleglosc od krawedzi
        mindist = float('inf')
        for areaPoint in self.domain:
            for edgePoint in self.edge:
                if areaPoint[0] == edgePoint[0][0] and areaPoint[1] == edgePoint[0][1]:
                    continue
                # dist = self.calculateDistance(areaPoint[0], areaPoint[1], edgePoint[0][0], edgePoint[0][1])
                x = (edgePoint[0][0] - areaPoint[0]) ** 2 + (edgePoint[0][1] - areaPoint[0]) ** 2
                dist = math.sqrt(x)
                if dist < mindist:
                    mindist = dist
            self.minDistanceFromEgdeSum += mindist
            mindist = float('inf')

    def calculateHeightWidth(self):  # wysokosc i szerokosc
        maxXdist = -1
        maxYdist = -1
        for edgePoint1 in self.edge:
            for edgePoint2 in self.edge:
                if edgePoint1[0][0] == edgePoint2[0][0] and edgePoint1[0][1] == edgePoint2[0][1]:
                    continue
                x = (edgePoint2[0][0] - edgePoint1[0][0]) ** 2
                y = (edgePoint2[0][1] - edgePoint1[0][1]) ** 2
                # distX = self.calculateDistance(edgePoint1[0][0], 0, edgePoint2[0][0], 0)
                # distY = self.calculateDistance(0, edgePoint1[0][1], 0, edgePoint2[0][1])
                distX = math.sqrt(x)
                distY = math.sqrt(y)
                if distX > maxXdist:
                    maxXdist = distX
                if distY > maxYdist:
                    maxYdist = distY
        self.LW = maxXdist
        self.LH = maxYdist

    def calculateMaxMinFromCenter(self):  # najwieszka i najmniejsza odleglosc miedzy srodkiem i krawedzia
        maxdist = -1
        mindist = float('inf')
        for edgePoint in self.edge:
            x = (self.centerOfMass[0] - edgePoint[0][0]) ** 2 + (self.centerOfMass[1] - edgePoint[0][1]) ** 2
            # dist = self.calculateDistance(edgePoint[0][0], edgePoint[0][1], self.centerOfMass[0], self.centerOfMass[1])
            dist = math.sqrt(x)
            if dist > maxdist:
                maxdist = dist
            if dist < mindist:
                mindist = dist
        self.maxDistaceCenterEdge = maxdist
        self.minDistaceCenterEdge = mindist

    def calculateMaxDistanceGrain(self):  # najwięsza odleglość miedzy punktami ziarna
        maxdist = -1
        coordinates = [0, 0, 0, 0]
        for edgePoint1 in self.edge:
            for edgePoint2 in self.edge:
                if edgePoint1[0][0] == edgePoint2[0][0] and edgePoint1[0][1] == edgePoint2[0][1]:
                    continue
                x = (edgePoint2[0][0] - edgePoint1[0][0]) ** 2 + (edgePoint2[0][1] - edgePoint1[0][1]) ** 2
                # dist = self.calculateDistance(edgePoint1[0][0], edgePoint1[0][1], edgePoint2[0][0], edgePoint2[0][1])
                dist = math.sqrt(x)
                if dist > maxdist:
                    coordinates[0] = edgePoint1[0][0]  # x1
                    coordinates[1] = edgePoint1[0][1]  # y1
                    coordinates[2] = edgePoint2[0][0]  # x2
                    coordinates[3] = edgePoint2[0][1]  # y2
                    maxdist = dist

        self.maxDistancePoints = maxdist
        self.maxDistanceVectorCoords = [coordinates[2] - coordinates[0], coordinates[3] - coordinates[1]]

    # def calculateDistance(self, x1, y1, x2, y2):
    #     distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    #     return distance
    #
    # def calculateDistanceList(self, coordsList):
    #     distance = math.sqrt((coordsList[2] - coordsList[0]) ** 2 + (coordsList[3] - coordsList[1]) ** 2)
    #     return distance

    def findVectorPerendicular(self):
        dst = []
        for edgePoint1 in self.edge:
            for edgePoint2 in self.edge:
                if edgePoint1[0][0] == edgePoint2[0][0] and edgePoint1[0][1] == edgePoint2[0][1]:
                    continue
                vec = [edgePoint2[0][0] - edgePoint1[0][0], edgePoint2[0][1] - edgePoint1[0][1]]
                if ((vec[0] * self.maxDistanceVectorCoords[0]) + (vec[0] * self.maxDistanceVectorCoords[1])) == 0:
                    dst.append(math.sqrt(vec[0] ** 2 + vec[1] ** 2))
        self.VectorPerpendicularLength = max(dst)