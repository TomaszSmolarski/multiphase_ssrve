task = {
    "name": "DP800",
    "picture_path": "Tests_results/200x200/DP800_2fr200x200.png",
    # SPL-splines/GR-grain grown
    "optimization_type": "SPL",
    "job": {
        "x_size": 200,
        "y_size": 200,
        "threads": 4,
        "pop_size": 24,
        "ratios_periodic": False,
        "activation_value": 0.25,
        "ratios": [],  #'Malinowska', 'Blair Bliss','Danielsson', 'Haralick'
        "save_dir_path": "Results/0",#"Tests_results/200x200_test/SPL_9_p24_M_BB_D_H/2/"
        "colors": {'ferrite': (29, 143, 255), 'bainite': (172, 255, 46), 'martensite': (255, 0, 0)},
        "max_evaluations": 2000,
        "max_generations": 50
    },
    "GR": {
        "starting_points_number": 40,
        "periodic": True,
    },
    "SPL": {
        "knots_number": 12,
        "number_of_shapes": 9,
        "periodic": True,
    },
    # PSO-particle swarm optimization/DEA-differential evolutionary algorithm
    "optimization_method": "DEA",
    "PSO": {
        "inertia": 0.5,  # default 0.5
        "cognitive_rate": 1.4,  # default 2.1
        "social_rate": 1.4  # default 2.1
    },
    "DEA": {
        "tournament_size": 2,
        "crossover_rate": 0.2,
        "num_crossover_points": 1,
        "mutation_rate": 0.285,
        "gaussian_mean": 0,
        "gaussian_stdev": 1
    },
    # optional set {} if not defined
    "target_series_from_ratios": {
        'ferrite': {'malinowska': {0: -0.0700312075588504, 1: 1.263293081643118, 2: -0.13298044955509547,
                                   3: -0.11858527037431676, 4: 0.11703838512401155, 5: 0.11336074698511878,
                                   6: -0.22547323572574718, 7: 0.02517853806912651, 8: -0.06939304574398064,
                                   9: -0.17898356029153917, 10: 0.0321693384823154, 11: -0.15371562467836553,
                                   12: -0.022286147717187954, 13: -0.2536473348197692, 14: -0.3214629605213791,
                                   15: -0.4015865793978509, 16: -0.34852998412944014, 17: 0.03956264078674998,
                                   18: -0.20699551287082796, 19: 1.134880947845876, 20: -0.495373495595968,
                                   21: -0.1856624801618001},
                    'blair bliss': {0: 0.8491610994474089, 1: 0.8747632541138893, 2: 0.8950639579505617,
                                    3: 0.9260742710912693, 4: 0.8240955839193898, 5: 0.8014970674562196,
                                    6: 0.9429544809488408, 7: 0.886761851028171, 8: 0.9201238055302449,
                                    9: 0.8905226918594006, 10: 0.833100399193548, 11: 0.8969316330968431,
                                    12: 0.8980455755310544, 13: 0.9181998964779959, 14: 0.8618138243044018,
                                    15: 0.9213177319235614, 16: 0.9047160526381612, 17: 0.8806915252259399,
                                    18: 0.9571995743460935, 19: 0.7265000286714455, 20: 0.9973557010035818,
                                    21: 0.9136217497080007},
                    'danielsson': {0: 24.27605110412888, 1: 63215240.904926986, 2: 17.4130971903373,
                                   3: 111.23062695906717, 4: 4363.488950823215, 5: 126.32576149828958,
                                   6: 670.5017966683357, 7: 1834.4911150426738, 8: 557.9208011232935,
                                   9: 2.578936194770511, 10: 3832.4766054813667, 11: 163.0557482695207,
                                   12: 143.47032967913168, 13: 7.95298370586152, 14: 1.5218720912040322,
                                   15: 0.8827166285569045, 16: 3.7396284374589714, 17: 594.7575022080957,
                                   18: 319.30631819921825, 19: 96671.4982937887, 20: 0.25986684687974787,
                                   21: 7.654777733903049},
                    'haralick': {0: 0.9150215114536479, 1: 0.9320312348087033, 2: 0.9223886880761456,
                                 3: 0.9283886258776651, 4: 0.9054314479272227, 5: 0.9068203378014716,
                                 6: 0.9280509709674546, 7: 0.9190644429336876, 8: 0.9254762723012904,
                                 9: 0.911307655089388, 10: 0.9094757471938377, 11: 0.9221703770865375,
                                 12: 0.9186381598223357, 13: 0.9232812739930267, 14: 0.906008318078254,
                                 15: 0.9057775112950971, 16: 0.9132258032650096, 17: 0.9118159365207843,
                                 18: 0.9313016573544098, 19: 0.9187836304546237, 20: 0.9176629354822471,
                                 21: 0.9184030142899219}},
        'bainite': {'malinowska': {0: -0.1987978175658086, 1: 0.42686608955104344, 2: -0.12237175892571239,
                                   3: -0.021870030389548045, 4: 0.08496359118134134, 5: -0.17014989542044334,
                                   6: -0.1494522003387374, 7: 0.785985455574193},
                    'blair bliss': {0: 0.8548763151459271, 1: 0.8172485842695115, 2: 0.9035658581792374,
                                    3: 0.8877166459769272, 4: 0.754659610402875, 5: 0.9508454509970015,
                                    6: 0.7639163073729235, 7: 0.7049701606056089},
                    'danielsson': {0: 10.81391816767251, 1: 78416.86372845681, 2: 57.20287655062082,
                                   3: 42.69617190148621, 4: 23.246967347260554, 5: 6.190431159881081,
                                   6: 1.2555858318453106, 7: 335636.0175127979},
                    'haralick': {0: 0.8966070576918486, 1: 0.9251382516165365, 2: 0.9224852714697783,
                                 3: 0.9165097989101834, 4: 0.8795433269841609, 5: 0.9282536320304333,
                                 6: 0.8870382806777359, 7: 0.9118638801349552}},
        'martensite': {'malinowska': {0: -0.06697839792315985, 1: 0.02381535341592289, 2: 0.8044703497001762,
                                      3: -0.04634554598220786, 4: 0.22241076435347185, 5: 0.10373283912439502,
                                      6: -0.060918038414769504, 7: 0.3041732928139358, 8: -0.4015865793978509,
                                      9: -0.10669982604938588, 10: -0.1856624801618001, 11: 0.11705307362391859,
                                      12: -0.033027771513118864, 13: 0.10479025167253453, 14: 0.20184364800749255,
                                      15: -0.3195617602709899, 16: 0.11666401213788324, 17: -0.09371462085257687,
                                      18: -0.2460699561348656, 19: 0.19106689860081882, 20: -0.012668228791426484,
                                      21: 0.14605720158539515, 22: 0.7418665858129749, 23: 0.4884879137699434,
                                      24: -0.34852998412944014, 25: -0.015153557396228257, 26: -0.17650837698604205,
                                      27: 1.3410141580256982, 28: -0.3755565593465301},
                       'blair bliss': {0: 0.8293230482516477, 1: 0.9369577012489525, 2: 0.5447097484312085,
                                       3: 0.8726862383781341, 4: 0.7856289269835497, 5: 0.9283104850465319,
                                       6: 0.9415679552950689, 7: 0.7866088668571899, 8: 0.9213177319235614,
                                       9: 0.9388682181065122, 10: 0.8889806600672195, 11: 0.8438439941274319,
                                       12: 0.9019931252564111, 13: 0.8757952235216031, 14: 0.7814030115036906,
                                       15: 0.9812682638840241, 16: 0.7809075318921339, 17: 0.83725566747521,
                                       18: 0.872260433893952, 19: 0.7149256870102654, 20: 0.8993784482218083,
                                       21: 0.802297105775149, 22: 0.764283232492647, 23: 0.6698226134419512,
                                       24: 0.8462843753216345, 25: 0.8916875567760539, 26: 0.9175672449232951,
                                       27: 0.6768886187327964, 28: 0.8505477996612626},
                       'danielsson': {0: 6.014479562906572, 1: 102.3904936145948, 2: 58.42142704757329,
                                      3: 37.91072938839008, 4: 2192.7573915353196, 5: 1000.8294663518204,
                                      6: 28.230341180305977, 7: 459.32714262052417, 8: 1.931526258719187,
                                      9: 12.354892705067586, 10: 148.32259581761608, 11: 809.268980551181,
                                      12: 341.8656975426778, 13: 41.19217852238726, 14: 12121.476640676812,
                                      15: 2.322589979037975, 16: 1772.1780563391312, 17: 49.83082417245072,
                                      18: 1.9683586876356223, 19: 262.21527616643306, 20: 474.2329591628827,
                                      21: 1049.7743134666803, 22: 19499.946498608053, 23: 114301.97696255571,
                                      24: 23.25716705509355, 25: 210.92757412267042, 26: 85.67929895109708,
                                      27: 65615.80510956292, 28: 1.0019534000439043},
                       'haralick': {0: 0.9118988086885281, 1: 0.9286414142080469, 2: 0.9207271649071311,
                                    3: 0.9204107312824618, 4: 0.896373651076098, 5: 0.9257354762557753,
                                    6: 0.9272835386747612, 7: 0.8898182900280688, 8: 0.9057775112950971,
                                    9: 0.9295757972046553, 10: 0.9099690169828563, 11: 0.9102825693857607,
                                    12: 0.9216393089090356, 13: 0.9199229400335542, 14: 0.8963282656672665,
                                    15: 0.9228446887735862, 16: 0.9010056646173649, 17: 0.9128371081729448,
                                    18: 0.9098421297527967, 19: 0.8933313421321961, 20: 0.9160288154087265,
                                    21: 0.9045938847123793, 22: 0.9296301501185245, 23: 0.9032118357735555,
                                    24: 0.9081424977895727, 25: 0.9134982379538628, 26: 0.9223814865430568,
                                    27: 0.9154225536588262, 28: 0.89876876267444}}},
    "target_stats": {'borderNeighbour': {'ferritebainite': 0.18475836431226766, 'ferritemartensite': 0.6721189591078067,
                                         'bainitemartensite': 0.14312267657992564},
                     'dispertionPhases': {'ferrite': 0.00055, 'bainite': 0.0002, 'martensite': 0.000725},
                     'onePointprobability': {'ferrite': 0.7466, 'bainite': 0.094625, 'martensite': 0.158775}}

}

ratios_weights = {'malinowska': 1,
                  'blair bliss': 1,
                  'danielsson': 0.0001,
                  'haralick': 1,
                  'mz': 1,
                  'rls': 1,
                  'rf': 1,
                  'rc1': 1,
                  'rc2': 1,
                  'rcom': 1,
                  'lp1': 1,
                  'lp2': 1,
                  'lp3': 1}
