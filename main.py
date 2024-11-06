# all lengths in meters unless otherwise noted

import math

def avg(aList: list) -> float:
    return sum(aList) / len(aList)

def frequencyToLength(frequency: float) -> float:
    return speedOfSound / (2 * frequency)

def endCorrection(radius: float) -> float:
    return 0.6 * radius

# DIDN'T: Debug why the current return vals are so low (200-400 instead of 1000+)
def cutOffFrequency(avgHoleRadius: float, \
                    boreRadius: float, \
                    speedOfSound: float, \
                    halfAvgHoleDistance: float, \
                    avgEffectiveLength: float) -> float:
    print(avgHoleRadius, boreRadius, speedOfSound, halfAvgHoleDistance, avgEffectiveLength)
    return 0.11 * (avgHoleRadius / boreRadius) * (speedOfSound / math.sqrt(halfAvgHoleDistance * avgEffectiveLength))

inputMode = input("Use default values? (Y/n): ").lower() == "n"

tubeRadius: float = 1.5 / 100 #m, don't set to wide lest cutOffFrequency() errors
tubeWallWidth: float = 0.5 / 100 #m
speedOfSound: float = 343.7 #m/s
octave: int = 3 #NOT scientific notation octaves, i.e. start on A
A4: int = 440 #Hz
stepsFromA: int = 8 #set to F
noteIntervals: list = [2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19] #Major scale up to octave + fifth

#holeRadii, Placements, & Frequencies are in furthest to closest order from place of articulation
holeRadii: list = [ 
    0.5,
    0.5,
    0.5,
    0.5,
    0.5,
    0.5,
    0.5,
    0.5,
    0.5,
    0.5,
    0.5
] #The values you see are in cm, logic-wise, holeRadii are in m
holeRadii = list(map(lambda a: a / 100, holeRadii))

if inputMode:
    anInput = input(f"Enter the radius of the tube (cm, default: {tubeRadius*100:.0f}): ")
    if anInput != "":
        tubeRadius = float(anInput) / 100
    
    anInput = input(f"Enter the outer width of the tube (cm, default: {tubeWallWidth*100:.0f}): ")
    if anInput != "":
        tubeWallWidth = float(anInput) / 100

    anInput = input(f"Enter the speed of sound (m/s, default: {speedOfSound}): ")
    if anInput != "":
        speedOfSound = float(anInput)

    anInput = input(f"Enter the octave of the note (default: {octave}): ")
    if anInput != "":
        octave = int(anInput)

    anInput = input(f"Enter the frequency of concert A (Hz, default: {A4}): ")
    if anInput != "":
        A4 = int(anInput)

    anInput = input(f"Enter the number of steps from A (octaves starting at A, default: {stepsFromA}): ")
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

lowestFrequency: float = A4 * 2**(octave-4) * 2**(stepsFromA/12) #Hz
tubeLength: float = frequencyToLength(lowestFrequency) - 2 * endCorrection(tubeRadius)
holePlacements: list = []
holeFrequencies: list = []
holeConflicts: list = []

print()

for i, interval in enumerate(noteIntervals):
    note = lowestFrequency * 2**(interval/12)
    holeRadius = holeRadii[i]
    holePlacement = frequencyToLength(note) - endCorrection(tubeRadius) - endCorrection(holeRadius) - tubeWallWidth
    holePlacements.append(holePlacement)
    holeFrequencies.append(note)

holeDistances: list = []
for i in range(len(holePlacements)-1):
        holeDistance = math.fabs(holePlacements[i + 1] - holePlacements[i])
        holeConflicts[i] = holeDistance - holeRadii[i] - holeRadii[i+1] < 0
        holeDistances.append(holeDistance)

if len(holePlacements) not in [0, 1]:
    cutOff = cutOffFrequency(
        avg(holeRadii[:len(holeDistances)-1]),
        tubeRadius,
        speedOfSound,
        avg(holeDistances)/2,
        # for more information on what this means, see
        # https://www.phys.unsw.edu.au/jw/reprints/crossfingering.pdf, page 2266
        # after you finish reading, please tell me what it means,
        # i haven't a clue
        avg(list(map(lambda b: b + 1.5 * tubeRadius, holePlacements))) 
    )

print("F - Fundamental; C - Cut-Off Frequency")
print("\"Mouthpiece\"")

for i, holePlacement in enumerate(holePlacements[::-1]):
    print(f"{i+1:>2}: {holePlacement*100:6.2f}cm\
{holeFrequencies[::-1][i]:>10.2f}Hz" + \
          (f"{holeDistances[::-1][i]*100:>8.2f}cm" if i < len(holeDistances) else "") +\
         (f"{'!':>10}" if holeConflicts[::-1][i] else ""))
print(f" F: {tubeLength*100:6.2f}cm{lowestFrequency:>10.2f}Hz")

if "cutOff" in globals():
    print(f" C: {cutOff:>18.2f}Hz")
print("\"Bell\"")
