import glob
import os
import inspyred
from optimization import Optimize


def remove_previous_results():
    file_list = glob.glob('Results/*.png')
    for filePath in file_list:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


if __name__ == '__main__':
    ratios = ['Malinowska','Blair Bliss']
    colors = {'ferrite': (29, 143, 255),
              'bainite': (172, 255, 46),
              'martensite': (255, 0, 0)}

    remove_previous_results()
    optimizator = Optimize(picture_path='testowy.png',threads=6, x_size=150, y_size=100, knots_number=12, pop_size=12,
                           ratios=ratios, colors=colors)
    optimizator.optimize()

    #inspyred.ec.analysis.generation_plot(open("stats.csv", "r"))