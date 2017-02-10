import colorschemes

total_leds = 60

myCycle = colorschemes.Rainbow(
    numLEDs=total_leds, pauseValue=0, numStepsPerCycle=255, numCycles=2, globalBrightness=10)
myCycle.start()
