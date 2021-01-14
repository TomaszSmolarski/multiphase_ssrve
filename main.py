import glob
import os

from GrainsOptimization.optimization_grains import GrainOptimize
from SplineOptimization.optimization_splines import SplineOptimize
from default_config import task


def remove_previous_results(path):
    file_list = glob.glob(path + 'Results/*.png')
    for filePath in file_list:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


if __name__ == '__main__':

    save_dir_path = task["job"]["save_dir_path"]
    try:
        os.makedirs(save_dir_path + "Results")
    except:
        print("Error while creating file : ", save_dir_path)

    remove_previous_results(save_dir_path)
    optimization_type = task["optimization_type"]

    if optimization_type == "GR":
        optimizator = GrainOptimize(task=task)
        optimizator.optimize()
    elif optimization_type == "SPL":
        optimizator = SplineOptimize(task=task)
        optimizator.optimize()
    else:
        raise Exception('Optimization type should be GR or SPL not: {}. Check task in default_config.py file'
                        .format(optimization_type))
