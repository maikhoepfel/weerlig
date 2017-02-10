import colorschemes

total_leds = 60
brightness = 3  # 0..31

for progress in range(1, total_leds+1):
    myCycle = colorschemes.Rainbow(
        numLEDs=progress, pauseValue=0, numStepsPerCycle=255, numCycles=1, globalBrightness=3)
    myCycle.start()
