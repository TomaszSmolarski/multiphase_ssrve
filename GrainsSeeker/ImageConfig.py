import cv2
import numpy as np
image = []
imageCopy = []
width = 0
height = 0
colorsNumber = 0
colors_map = {
    'ferrite': (29, 143, 255),
    'bainite': (172, 255, 46),
    'martensite': (255, 0, 0)
}
heightOffset = 0
widthOffset = 0







font = cv2.FONT_HERSHEY_COMPLEX
def drawCountour(contour):  # rysowanie środków konturów
    blank = np.zeros((height, width, 3), np.uint8)  # ilosc wierszy -> ilosc kolumn
    for i in range(width):
        for j in range(height):
            if cv2.pointPolygonTest(contour, (i, j), measureDist=False) >= 0:
                blank[j, i, :] = 255
    # cv2.putText(blank, "Arrow tip", (540, 60), font, 0.5, (255, 0, 0))
    cv2.imshow('bl', blank)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
