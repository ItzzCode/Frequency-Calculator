import math

def frequencyToLength(frequency: float) -> float:
    return speedOfSound / (2*f)

def endCorrection(radius: float) -> float:
    return 0.6 * radius

def cutOffFrequency(toneholeRadius: float, \
                    boreRadius: float, \
                    speedOfSound: float, \
                    halfAvgHoleDistance: float, \
                    avgHoleLength: float) -> float:
    return 0.11 * (toneholeRadius / boreRadius) * (speedOfSound / math.sqrt(halfAvgHoleDistance * avgHoleLength))

noteIntervalList: list = [2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19]
holePlacementList: list;
holeDiameterList: list; #(N * [''])[:N]

radius: float = 4.0 / 100 #m
speedOfSound: float = 343.7 #m/s
A: int = 220
lowestFrequency: float = A*2**(1/12)
tubeLength: float = frequencyToLength(lowestFrequency)

print(lowestFrequency, tubeLength - 2*endCorrection(radius))
for i in noteIntervalList:
    note = lowestFrequency*2**(i/12)
    toneholeRadius = 2.5 / 100 #placeholder
    holePlacement = frequencyToLength(note) - endCorrection(radius) - endCorrection(toneholeRadius)
    