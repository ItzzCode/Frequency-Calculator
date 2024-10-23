# all lengths in meters unless otherwise noted

import math

def avg(aList: list) -> float:
    return sum(aList) / len(aList)

def frequencyToLength(frequency: float) -> float:
    return speedOfSound / (2 * frequency)

def endCorrection(radius: float) -> float:
    return 0.6 * radius

# DID: Debug why the current return vals are so low (200-400 instead of 1000+)
# REMEDY: Do not add more elements to holeRadii than there are holes
def cutOffFrequency(avgHoleRadius: float, \
                    boreRadius: float, \
                    speedOfSound: float, \
                    halfAvgHoleDistance: float, \
                    avgHoleLength: float) -> float:
    return 0.11 * (avgHoleRadius / boreRadius) * (speedOfSound / math.sqrt(halfAvgHoleDistance * avgHoleLength))

tubeRadius: float = 1.5 / 100 #m, don't set to wide lest cutOffFrequency() errors
tubeOuterWidth: float = 1 / 100 #m
speedOfSound: float = 343.7 #m/s
A: int = 220 #Hz
lowestFrequency: float = A*2**(8/12) #Hz, set to F
tubeLength: float = frequencyToLength(lowestFrequency) - 2*endCorrection(tubeRadius)

noteIntervals: list = [2, 4, 5, 7, 9, 11, 12] #14, 16, 17, 19]

#goes from furthest to closest from place of articulation
holePlacements: list = []
holeRadii: list = [ 
    0.1,
    0.1,
    0.1,
    0.1,
    0.1,
    0.1,
    0.1,
    0.1
]; 
holeFrequencies: list = []

#(N * [''])[:N]

for i, interval in enumerate(noteIntervals):
    note = lowestFrequency * 2**(interval/12)
    holeRadius = holeRadii[i]
    holePlacement = frequencyToLength(note) - endCorrection(tubeRadius) - endCorrection(holeRadius) - tubeOuterWidth
    holePlacements.append(holePlacement)
    holeFrequencies.append(note)

holeDistances: list = []
for i in range(len(holePlacements)-1):
        holeDistances.append(math.fabs(holePlacements[i + 1] - holePlacements[i]))

cutOff = cutOffFrequency(avg(holeRadii[:len(holeDistances)-1]), tubeRadius, speedOfSound, avg(holeDistances)/2, avg(holePlacements))

for i, holePlacement in enumerate(holePlacements[::-1]):
    print(f"{i+1}: {holePlacement*100:5.2f}cm{holeFrequencies[::-1][i]:>9.2f}Hz")
print(f"F: {tubeLength*100:5.2f}cm{lowestFrequency:>9.2f}Hz")
print(f"C: {cutOff:>16.2f}Hz")