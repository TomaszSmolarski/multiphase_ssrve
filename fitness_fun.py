import math

ratios_weights = {'malinowska': 0.1,
                  'blair bliss': 0.1,
                  'danielsson': 0.001,
                  'haralick': 0.1,
                  'mz': 0.1,
                  'rls': 0.1,
                  'rf': 0.1,
                  'rc1': 0.1,
                  'rc2': 0.1,
                  'rcom': 0.1,
                  'lp1': 0.1,
                  'lp2': 0.1,
                  'lp3': 0.1}


def candidate_fitness(series_from_ratios, stats, target_series_from_ratios, target_stats):
    x = 0
    for target_phase_params, test_phase_params in zip(target_series_from_ratios.values(), series_from_ratios.values()):

        if len(test_phase_params) == 0:
            for ratio in target_phase_params.keys():
                test_phase_params[ratio] = {}

        for target_ratios, test_ratios in zip(target_phase_params.items(), test_phase_params.items()):

            target_ratios_list = list(target_ratios[1].values())
            test_ratios_list = list(test_ratios[1].values())
            target_list_len = len(target_ratios_list)
            test_list_len = len(test_ratios_list)

            list_range = min(target_list_len,test_list_len)
            for nr in range(list_range):
                x += ratios_weights[target_ratios[0]] * pow(test_ratios_list[nr] - target_ratios_list[nr], 2)

            if target_list_len>test_list_len:
                for nr in range(test_list_len, target_list_len):
                    x += ratios_weights[target_ratios[0]] * pow(target_ratios_list[nr], 2)
            elif target_list_len<test_list_len:
                for nr in range(target_list_len, test_list_len):
                    x += ratios_weights[target_ratios[0]] * pow(test_ratios_list[nr], 2)

    for target_stats_elem, test_stats_elem in zip(target_stats.values(), stats.values()):
        for target_stats, test_stats in zip(list(target_stats_elem.values()), list(test_stats_elem.values())):
            x += 0.3 * pow(test_stats - target_stats, 2)

    return 1 / 3 * math.sqrt(x)


