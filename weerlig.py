#!/usr/bin/env python
import apa102
import time
import RPi.GPIO as GPIO
import gpiozero

total_leds = 60
brightness = 31  # 0..31
lightning_talk_time = 30 # in seconds
rounds_per_minute = 40

SWITCH_GPIO = 4  # BCM numbering, equals board pin 7


def init_strip():
    # Initialize the class
    return apa102.APA102(numLEDs=total_leds, globalBrightness=brightness)


def init_buttons():
    # Let pins confirm to board numbering
    return gpiozero.Button(SWITCH_GPIO, bounce_time=0.1)


def show_idle_strip(strip):
    for led in range(total_leds):
        strip.setPixel(led, 1, 1, 1)
    strip.show()


def set_and_show_strip(strip, progress):
    active_leds_cutoff = progress * total_leds

    if active_leds_cutoff == 0:
        return

    wheel_offset = progress * 256 * (rounds_per_minute * lightning_talk_time / 60)

    for led in range(total_leds):
        current_position = 256 * led / total_leds
        actual_position = int(wheel_offset + current_position) % 256

        color = strip.wheel(actual_position)

        if led > active_leds_cutoff:
            strip.setPixel(led, 1, 1, 1)
        else:
            strip.setPixelRGB(led, color)

    strip.show()


def visualize(strip, button):
    start_of_talk = current_time = time.time()
    end_of_talk = start_of_talk + lightning_talk_time
    while current_time < end_of_talk:
        elapsed_seconds = current_time - start_of_talk
        progress = elapsed_seconds / lightning_talk_time
        set_and_show_strip(strip, progress)
        current_time = time.time()
        if button.is_pressed:
            print("Aborted because of button press")
            return


if __name__ == '__main__':
    # Initialize
    strip = init_strip()
    button = init_buttons()

    while True:
        # Power up strip in initial state
        show_idle_strip(strip)

        print("Waiting for button press")
        button.wait_for_press()
        button.wait_for_release()

        print("Starting")
        # Aborts early if button is pressed
        visualize(strip, button)

        print("Finished")


        #TODO strip.cleanup()
