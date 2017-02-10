#!/usr/bin/env python
import apa102
import time

total_leds = 60
brightness = 31  # 0..31
lightning_talk_time = 30 # in seconds

current_step = 0


def init_strip():
    # Initialize the class
    return apa102.APA102(numLEDs=total_leds, globalBrightness=brightness)


def show_idle_strip(strip):
    for led in range(total_leds):
        strip.setPixel(led, 1, 1, 1)
    strip.show()


def set_and_show_strip(strip, progress):
    global current_step
    leds_progress = int(round(progress * total_leds))
    if leds_progress == 0:
        return

    scale_factor = 255 / leds_progress
    start_index = current_step

    for led in range(total_leds):
        if led > leds_progress:
            strip.setPixel(led, 1, 1, 1)
        else:
            led_index = start_index + led * scale_factor
            led_wrapped = int(round(led_index, 0)) % 255
            color = strip.wheel(led_wrapped)
            strip.setPixelRGB(led, color)

    strip.show()
    current_step += 1


def visualize(strip):
    start_of_talk = current_time = time.time()
    end_of_talk = start_of_talk + lightning_talk_time
    while current_time < end_of_talk:
        elapsed_seconds = current_time - start_of_talk
        progress = elapsed_seconds / lightning_talk_time
        set_and_show_strip(strip, progress)
        current_time = time.time()
    print('Finished')

if __name__ == '__main__':
    strip = init_strip()
    show_idle_strip(strip)
    try:
        visualize(strip)
    except KeyboardInterrupt:
        print('User aborted')
    else:
        show_idle_strip(strip)
    finally:
        strip.cleanup()
