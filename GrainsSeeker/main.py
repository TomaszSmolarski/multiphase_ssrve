import cv2
from GrainsSeeker import RatiosConfig as rc
from GrainsSeeker import ImageConfig, statistics_ratios_class as src, DataGatherer as dg
from GrainsSeeker.grain_class import Grain
import numpy as np


def makePeriodicalImage():
    phaseLayersPeriodical = np.zeros((ImageConfig.height * 3, ImageConfig.width * 3, len(ImageConfig.colors_map)),
                                     np.uint8)
    for i in range(0, 3):
        for y in range(ImageConfig.height):
            yOffset = ImageConfig.height * i
            for j in range(0, 3):
                for x in range(ImageConfig.width):
                    xOffset = ImageConfig.width * j
                    phaseLayersPeriodical[y + yOffset, x + xOffset, 0] = ImageConfig.image[y, x, 0]
                    phaseLayersPeriodical[y + yOffset, x + xOffset, 1] = ImageConfig.image[y, x, 1]
                    phaseLayersPeriodical[y + yOffset, x + xOffset, 2] = ImageConfig.image[y, x, 2]

    cv2.imshow('bl', phaseLayersPeriodical)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ImageConfig.image = phaseLayersPeriodical


def findContoursAndCalculateRatios(layer, phase, background, grains, periodical):
    if phase == background:
        return
    ret, thresh = cv2.threshold(layer, 1, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    centersOfMass = []
    for i in range(len(contours)):
        isEdge = False
        #print('ziarno ', i, ' faza ', phase)
        if len(contours[i]) > 1:
            if periodical:
                for j in range(len(contours[i])):
                    if contours[i][j][0][0] == 0 or contours[i][j][0][1] == 0:
                        isEdge = True
                    if contours[i][j][0][0] == ImageConfig.widthOffset * 3 - 1 or contours[i][j][0][
                        1] == ImageConfig.heightOffset * 3 - 1:
                        isEdge = True
                    if contours[i][j][0][0] == ImageConfig.widthOffset * 3 or contours[i][j][0][
                        1] == ImageConfig.heightOffset * 3:
                        isEdge = True
            if isEdge:
                continue
            gr = Grain(contours[i], phase)
            if gr.area > gr.perimeter:
                xOffset = int(contours[i][0][0][0] / ImageConfig.widthOffset)
                yOffset = int(contours[i][0][0][1] / ImageConfig.heightOffset)
                gr.findCoM(xOffset, yOffset)
                if gr.centerOfMassLocal not in centersOfMass:
                    centersOfMass.append(gr.centerOfMassLocal)
                    grains.append(gr)


def mainFunction(image, ratios=[], colors={}, background='', periodical=False):
    grains = []
    if colors:
        ImageConfig.colors_map = colors
    if ratios:
        rc.ratiosToCalculateList = ratios
    rc.tolowercase()

    # ImageConfig.heightOffset, ImageConfig.widthOffset = image.shape[:2]
    ImageConfig.image = image
    ImageConfig.height, ImageConfig.width = ImageConfig.image.shape[:2]
    ImageConfig.imageCopy = image
    if periodical:
        makePeriodicalImage()
        ImageConfig.heightOffset, ImageConfig.widthOffset = ImageConfig.imageCopy.shape[:2]
        ImageConfig.height, ImageConfig.width = ImageConfig.image.shape[:2]
    else:
        ImageConfig.heightOffset, ImageConfig.widthOffset = ImageConfig.image.shape[:2]

    PhaseLayers = np.zeros((ImageConfig.height, ImageConfig.width, len(ImageConfig.colors_map)), np.uint8)
    index = 0
    for color in ImageConfig.colors_map.values():
        for i in range(ImageConfig.width):
            for j in range(ImageConfig.height):
                if ImageConfig.image[j, i, 0] == color[2] and ImageConfig.image[j, i, 1] == color[1] and \
                        ImageConfig.image[
                            j, i, 2] == color[0]:  # BGR nie RGB
                    PhaseLayers[j, i, index] = 255
        # layer = PhaseLayers[:, :, index]
        # cv2.imshow('bl', layer)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        index = index + 1

    # DLA KAŻDEJ FAZY WYWOŁANIE FUNKCJI SZUKAJĄCEJ ZIAREN
    for phase in range(len(ImageConfig.colors_map)):
        phaseName = list(ImageConfig.colors_map.keys())
        findContoursAndCalculateRatios(PhaseLayers[:, :, phase], phaseName[phase], background, grains, periodical)
    if ratios:
        for grain in grains:
            grain.startCalculating()

    ImageConfig.image = ImageConfig.imageCopy
    ImageConfig.height, ImageConfig.width = ImageConfig.image.shape[:2]
    st = src.Statistics()
    st.blr()
    st.dispertion(grains, 1)
    st.onePointProb()
    return dg.createSeriesFromRatios(grains), st.returnRatios()
