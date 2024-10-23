# all lengths in meters unless otherwise noted

import math

def avg(aList: list) -> float:
    return sum(aList) / len(aList)

def frequencyToLength(frequency: float) -> float:
    return speedOfSound / (2 * frequency)

def endCorrection(radius: float) -> float:
    return 0.6 * radius

# TODO: Debug why the current return vals are so low (200-400 instead of 1000+)
def cutOffFrequency(avgHoleRadius: float, \
                    boreRadius: float, \
                    speedOfSound: float, \
                    halfAvgHoleDistance: float, \
                    avgHoleLength: float) -> float:
    return 0.11 * (avgHoleRadius / boreRadius) * (speedOfSound / math.sqrt(halfAvgHoleDistance * avgHoleLength))

tubeRadius: float = 6.0 / 100 #m
speedOfSound: float = 343.7 #m/s
A: int = 220 #Hz
lowestFrequency: float = A*2**(1/12) #Hz, set to Bb
tubeLength: float = frequencyToLength(lowestFrequency) - 2*endCorrection(tubeRadius)

noteIntervals: list = [2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19]
holePlacements: list = []
holeRadii: list = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]; 
#(N * [''])[:N]

for i, interval in enumerate(noteIntervals):
    note = lowestFrequency * 2**(interval/12)
    holeRadius = holeRadii[i]
    holePlacement = frequencyToLength(note) - endCorrection(tubeRadius) - endCorrection(holeRadius)
    holePlacements.append(holePlacement)

holeDistances: list = []
for i in range(len(holePlacements)-1):
        holeDistances.append(math.fabs(holePlacements[i + 1] - holePlacements[i]))

print(holePlacements)

cutOff = cutOffFrequency(avg(holeRadii), tubeRadius, speedOfSound, avg(holeDistances)/2, avg(holePlacements))

print(cutOff)