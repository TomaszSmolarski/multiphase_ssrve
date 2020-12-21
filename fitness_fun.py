import math
from default_config import ratios_weights
from statistics import median


def calculate_candidate_mean_square_error(series_from_ratios, stats, target_series_from_ratios, target_stats):
    x = 0
    number_of_coefficients = 0
    stats_weight = 1
    for target_phase_params, test_phase_params in zip(target_series_from_ratios.values(), series_from_ratios.values()):
        for target_ratios, test_ratios in zip(target_phase_params.items(), test_phase_params.items()):
            if target_ratios[1]:
                target_ratios_median = median(list(target_ratios[1].values()))
            else:
                target_ratios_median = 0
            if test_ratios[1]:
                test_ratios_median = median(list(test_ratios[1].values()))
            else:
                test_ratios_median = 1
            x += ratios_weights[target_ratios[0]] * pow(test_ratios_median - target_ratios_median, 2)

    for target_stats_elem, test_stats_elem in zip(target_stats.values(), stats.values()):
        for target_stats, test_stats in zip(list(target_stats_elem.values()), list(test_stats_elem.values())):
            x += stats_weight * pow(test_stats - target_stats, 2)
            number_of_coefficients += 1
    return (1 / number_of_coefficients) * math.sqrt(x)
