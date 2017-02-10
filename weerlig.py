import apa102
from time import sleep

total_leds = 60
brightness = 3  # 0..31

lightning_talk_time = 300 # in seconds

# Initialize the class
strip = apa102.APA102(numLEDs=total_leds, globalBrightness=brightness)
# Strip goes black
strip.clearStrip()
strip.show()

for progress in range(0, total_leds):
    strip.setPixel(progress, 255, 255, 255)
    strip.show()
    sleep(lightning_talk_time/total_leds)

strip.cleanup()



