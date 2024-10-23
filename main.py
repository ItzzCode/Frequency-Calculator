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

inputMode = input("Use default values? (Y/n): ").lower() == "n"

tubeRadius: float = 1.5 / 100 #m, don't set to wide lest cutOffFrequency() errors
tubeOuterWidth: float = 1 / 100 #m
speedOfSound: float = 343.7 #m/s
A: int = 220 #Hz
stepsFromA: int = 8 #set to F
noteIntervals: list = [2, 4, 5, 7, 9, 11, 12] #14, 16, 17, 19]

#holeRadii, Placements, & Frequencies are in furthest to closest order from place of articulation
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

if inputMode:
    anInput = input(f"Enter the radius of the tube (cm, default: {tubeRadius*100:.0f}): ")
    if anInput != "":
        tubeRadius = float(anInput) / 100
    
    anInput = input(f"Enter the outer width of the tube (cm, default: {tubeOuterWidth*100:.0f}): ")
    if anInput != "":
        tubeOuterWidth = float(anInput) / 100

    anInput = input(f"Enter the speed of sound (m/s, default: {speedOfSound}): ")
    if anInput != "":
        speedOfSound = float(anInput)

    anInput = input(f"Enter the frequency of concert A (Hz, default: {A}): ")
    if anInput != "":
        A = int(anInput)

    anInput = input(f"Enter the number of steps from A (default: {stepsFromA}): ")
    if anInput != "":
        stepsFromA = int(anInput)

    anInput = input(f"Enter the number of holes (defaults: \n\t\
        Holes: {len(noteIntervals)}\n\t\
        Steps from fundamental: {noteIntervals}\n\t\
        Hole radii: {holeRadii}\n): ")
    if anInput != "":
        noteIntervals = []
        holeRadii = []
        for i in range(int(anInput)):
            anInput = input(f"Enter the radius of hole {i+1} (cm): ")
            holeRadii.append(float(anInput) / 100)
            
            anInput = input(f"Enter the steps from fundamental of hole {i+1}: ")
            noteIntervals.append(int(anInput))

lowestFrequency: float = A * 2**(8/12) #Hz
tubeLength: float = frequencyToLength(lowestFrequency) - 2 * endCorrection(tubeRadius)
holePlacements: list = []
holeFrequencies: list = []

print()

for i, interval in enumerate(noteIntervals):
    note = lowestFrequency * 2**(interval/12)
    holeRadius = holeRadii[i]
    holePlacement = frequencyToLength(note) - endCorrection(tubeRadius) - endCorrection(holeRadius) - tubeOuterWidth
    holePlacements.append(holePlacement)
    holeFrequencies.append(note)

holeDistances: list = []
for i in range(len(holePlacements)-1):
        holeDistances.append(math.fabs(holePlacements[i + 1] - holePlacements[i]))

if len(holePlacements) != 0:
    cutOff = cutOffFrequency(avg(holeRadii[:len(holeDistances)-1]), tubeRadius, speedOfSound, avg(holeDistances)/2, avg(holePlacements))

print("F - Fundamental; C - Cut-Off Frequency")
for i, holePlacement in enumerate(holePlacements[::-1]):
    print(f"{i+1}: {holePlacement*100:5.2f}cm{holeFrequencies[::-1][i]:>9.2f}Hz")
print(f"F: {tubeLength*100:6.2f}cm{lowestFrequency:>10.2f}Hz")
if "cutOff" in globals():
    print(f"C: {cutOff:>16.2f}Hz")