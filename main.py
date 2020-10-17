import glob
import os
from GrainsOptimization.optimization_grains import GrainOptimize
from SplineOptimization.optimization_splines import SplineOptimize
from SplineOptimization import periodic_fun
from GrainsOptimization.periodic_fun import not_period_grid, period_grid
from default_config import d_ratios_periodic


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

    optimizator = SplineOptimize(picture_path='test.png',
                                 periodic_type_f=periodic_fun.not_period_splines,ratios_periodic=d_ratios_periodic,
                                 threads=6, x_size=200, y_size=150, knots_number=12, pop_size=12,
                                 ratios=ratios, colors=colors)
    optimizator.optimize()

    optimizator = GrainOptimize(picture_path='testowy.png', periodic_type_f=period_grid,
                                ratios_periodic=d_ratios_periodic,  threads=6, x_size=150,
                                y_size=150, pop_size=12,
                                ratios=ratios, colors=colors, starting_points_number=30)
    optimizator.optimize()

    # inspyred.ec.analysis.generation_plot(open("stats.csv", "r"))
