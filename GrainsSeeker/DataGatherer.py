from GrainsSeeker import ImageConfig as ic
import pandas as pd

pd.options.display.float_format = '{:.15f}'.format
resultsForEachPhase = []


def createSeriesFromRatios(grains):
    frames = {}
    for phase in ic.colors_map.keys():
        phaseSeries = []
        for Grain in grains:
            if Grain.phase == phase:
                grainSeries = pd.Series(Grain.calculatedRatiosDict)
                phaseSeries.append(grainSeries)
        if phaseSeries:
            phaseFrame = pd.concat(objs=phaseSeries, axis=1)
            phaseFrame = phaseFrame.transpose()
            frames[phase] = phaseFrame.to_dict()
        else:
            frames[phase] = pd.DataFrame().to_dict()
    return frames
