import glob
import os

import inspyred

from GrainsOptimization.optimization_grains import GrainOptimize
from SplineOptimization.optimization_splines import SplineOptimize
from SplineOptimization import periodic_fun
from GrainsOptimization.periodic_fun import not_period_grid, period_grid
from default_config import d_ratios_periodic


def remove_previous_results(path):
    file_list = glob.glob(path+'Results/*.png')
    for filePath in file_list:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


if __name__ == '__main__':

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
       
    PSO/GA/DEA - optimization type
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
    in DEA:
        ts - tournament_size
        cr - crossover_rate 
        mr - mutation_rate
        gm - gaussian_mean
        gs - gaussian_stdev
        
    ratios (in dir with image dimensions):
        M -'Malinowska',
        BB - 'Blair Bliss',
        D -'Danielsson',
        H - 'Haralick
        rest as in default file
    pi - points interpolate
    rp - random points
    tr - truncation_replacement
    cr - crowding_replacement
    bc - blend_crossover
    gm - gaussian_mutation
    rs - rank_selection
    us - uniform selection
    '''

    # ratios = ['Malinowska', 'Blair Bliss']
    ratios = []
    colors = {'ferrite': (29, 143, 255),
              'bainite': (172, 255, 46),
              'martensite': (255, 0, 0)}

    # test_path = "Tests_results/250x250/SPL_kn12_p16_nrp_np_PSO_me1000_ns3_i0,5_cr1,4_sr1,4/2rp/"
    # test_path = "Tests_results/250x250/GR_spn40_p16_nrp_np_GA_me1000_mr0,25_ncp4_cr0,2_ns20/1rp/"
    # test_path = "Tests_results/250x250/SPL_kn12_p16_nrp_np_GA_me1000_mr0,4_ncp3_cr0,3_ns16/1rp/"
    # test_path = "Tests_results/250x250/SPL_kn12_p16_nrp_np_DEA_me1000_mr0,4_ts4_gm1_gs0_cr1_ns16/1rp/"
    # test_path = "Tests_results/150x150/SPL_kn12_p32_nrp_np_DEA_me1000_mr0,5_ts4_gm1_gs0_cr0,2_ns32_tr_bcgm_rs/1/"
    #test_path = "Tests_results/200x200/_/SPL_kn12_p16_nrp_np_DEA_me1000_ts2_gm1_gs0_cr0,2_mr0,3_ns16_tr_bcgm_ts/3_0-200/"

    for nr in range(4):
        test_path = "Tests_results/200x200_2/_/SPL_kn12_p16_nrp_np_DEA_me1000_ts2_gm1_gs0_cr0,2_mr0,3_ns16_tr_bcgm_ts/{}_0-200/".format(nr)
        try:
            os.makedirs(test_path + "Results")
        except:
            print("Error while creating file : ", test_path)
        remove_previous_results(test_path)
        p_path = 'Tests_results/200x200/DP800_2fr200x200.png'

        optimizator = SplineOptimize(picture_path=p_path,
                                 periodic_type_f=periodic_fun.not_period_splines, ratios_periodic=d_ratios_periodic,
                                 threads=8, x_size=200, y_size=200, knots_number=12, pop_size=16,
                                 ratios=ratios, colors=colors, save_dir_path=test_path)
        optimizator.optimize()

    '''
    optimizator = GrainOptimize(picture_path=p_path, periodic_type_f=not_period_grid,
                                ratios_periodic=d_ratios_periodic,  threads=8, x_size=200,
                                y_size=200, pop_size=16,
                                ratios=ratios, colors=colors, starting_points_number=40, save_dir_path=test_path)
    optimizator.optimize()
    '''
