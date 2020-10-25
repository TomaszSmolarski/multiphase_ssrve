import glob
import os

import inspyred

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
    #remove_previous_results()
    '''
    tests paths description:
    SPL/GR - splines/grains optimization:
    in SPL:     
        kn - knots numbers   
    in GR:
        spn - starting_points_number
        
    p - population size
    (n)rp - (not) ratios periodic
    (n)p - (not) periodic type in new image       
       
    PSO/GA - optimization type
    in PSO:
        me - max evaluates
        ns - neighborhood_size
        i - inertia
        cr - cognitive_rate
        sr - social_rate
    in GA:
        mr - mutation_rate
        ncp - num_crossover_points
        cr - crossover_rate
        ns - num_selected
        
    ratios (in dir with image dimensions):
        M -'Malinowska',
        BB - 'Blair Bliss',
        D -'Danielsson',
        H - 'Haralick
        rest as in default file
    pi - points interpolate
    rp - random points
    '''
    ratios = []
    colors = {'ferrite': (29, 143, 255),
              'bainite': (172, 255, 46),
              'martensite': (255, 0, 0)}
    "Tests_results/250x250_M_BB/SPL_kn12_p16_nrp_np_PSO_me1000_ns3_i0,5_cr1,4_sr1,4/"
    #test_path = "Tests_results/250x250/SPL_kn12_p16_nrp_np_PSO_me1000_ns3_i0,5_cr1,4_sr1,4/2rp/"
    #test_path = "Tests_results/250x250/GR_spn40_p16_nrp_np_GA_me1000_mr0,25_ncp4_cr0,2_ns20/1rp/"
    #test_path = "Tests_results/250x250/SPL_kn12_p16_nrp_np_GA_me1000_mr0,4_ncp3_cr0,3_ns16/1rp/"
    test_path = "Tests_results/250x250/SPL_kn12_p16_nrp_np_DEA_me1000_mr0,3_ncp3_cr1,0_ns16/1rp/"

    try:
        os.makedirs(test_path + "Results")
    except:
        print("Error while creating file : ", test_path)

    optimizator = SplineOptimize(picture_path='Tests_results/DP800_2fr250x250.png',
                                 periodic_type_f=periodic_fun.not_period_splines, ratios_periodic=d_ratios_periodic,
                                 threads=8, x_size=250, y_size=250, knots_number=12, pop_size=16,
                                 ratios=ratios, colors=colors, save_dir_path=test_path)
    optimizator.optimize()

    '''

    optimizator = GrainOptimize(picture_path='Tests_results/DP800_2fr250x250.png', periodic_type_f=period_grid,
                                ratios_periodic=d_ratios_periodic,  threads=8, x_size=250,
                                y_size=250, pop_size=16,
                                ratios=ratios, colors=colors, starting_points_number=40, save_dir_path=test_path)
    optimizator.optimize()
    '''


