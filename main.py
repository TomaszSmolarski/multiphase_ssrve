import glob
import os
from GrainsOptimization.optimization_grains import GrainOptimize
from SplineOptimization.optimization_splines import SplineOptimize
from SplineOptimization import periodic_fun


def remove_previous_results():
    file_list = glob.glob('Results/*.png')
    for filePath in file_list:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


if __name__ == '__main__':
    ratios = []
    colors = {'ferrite': (29, 143, 255),
              'bainite': (172, 255, 46),
              'martensite': (255, 0, 0)}

    remove_previous_results()

    optimizator = SplineOptimize(picture_path='test.png', threads=6, x_size=300, y_size=250, knots_number=12,
                                 pop_size=12,
                                 ratios=ratios, colors=colors, periodic_type_f=periodic_fun.not_period_splines)
    optimizator.optimize()

    optimizator = GrainOptimize(picture_path='testowy.png', threads=6, x_size=150, y_size=150, pop_size=12,
                                              ratios=ratios, colors=colors, starting_points_number=30)
    optimizator.optimize()
    # inspyred.ec.analysis.generation_plot(open("stats.csv", "r"))
