#!/usr/bin/env python
import apa102
import time
import gpiozero

TOTAL_LEDS = 60
BRIGHTNESS = 3  # 0..31
LIGHTNING_TALK_TIME = 300  # in seconds
TIME_OVER_TIME = 5
RAINBOW_ROUNDS_PER_MINUTE = 40

SWITCH_GPIO = 4  # BCM numbering, equals board pin 7


def init_strip():
    """
    Initializes the LED strip
    """
    return apa102.APA102(numLEDs=TOTAL_LEDS, globalBrightness=BRIGHTNESS)


def init_buttons():
    """
    Initializes the button to start the visualization
    """
    return gpiozero.Button(SWITCH_GPIO, bounce_time=0.03)


def show_idle_strip(strip):
    """
    Light up the entire strip, but very dimly
    """
    for led in range(TOTAL_LEDS):
        strip.setPixel(led, 1, 1, 1)
    strip.show()


def rainbow_progress(strip, progress):
    """
    Render one frame of a rainbow effect progress meter
    """

    # We always pretend we're doing the rainbow effect across the entire strip,
    # but then we only set it for an increasing number of LEDs. LEDs with an index
    # below active_leds_cutoff get the rainbow, the others keep being dimly lit.
    active_leds_cutoff = progress * TOTAL_LEDS

    # No progress yet? Avoid division by zero.
    if active_leds_cutoff == 0:
        return

    # An ever-increasing variable that is used to determine where we are in the
    # color wheel for this round (we're only interested in wheel_offset % 256)
    wheel_offset = progress * 256 * (RAINBOW_ROUNDS_PER_MINUTE * LIGHTNING_TALK_TIME / 60)

    # Set colors for all LEDs
    for led in range(TOTAL_LEDS):
        if led < active_leds_cutoff:
            # Boring, this LEDs isn't "active" yet, stays dimly lit.
            strip.setPixel(led, 1, 1, 1)
        else:
            # A value 0..255 of how far along we are in the strip
            position_in_strip = 256 * led / TOTAL_LEDS
            # The final position in the color wheel gets is just the wheel_offset plus current
            # position in strip; modulo 256.
            actual_position = int(wheel_offset + position_in_strip) % 256

            color = strip.wheel(actual_position)
            strip.setPixelRGB(led, color)

    # Now let the strip show the new values
    strip.show()


def visualize_time_elapsing(strip, button):
    """
    Show a progress meter for LIGHTNING_TALK_TIME seconds
    """
    start_of_talk = current_time = time.time()
    end_of_talk = start_of_talk + LIGHTNING_TALK_TIME
    while current_time < end_of_talk:
        elapsed_seconds = current_time - start_of_talk
        progress = elapsed_seconds / LIGHTNING_TALK_TIME
        rainbow_progress(strip, progress)
        current_time = time.time()
        if button.is_pressed:
            print("Aborted early because of button press")
            return True
    return False


def red_alert(strip):
    """
    Turn the entire strip bright red
    """
    for led in range(TOTAL_LEDS):
        strip.setPixel(led, 255, 0, 0)
    strip.show()


def visualize_time_over(strip, button):
    """
    Show a bright red strip for TIME_OVER_TIME seconds
    """
    red_alert(strip)
    start_time = current_time = time.time()
    end_time = start_time + TIME_OVER_TIME
    while current_time < end_time:
        current_time = time.time()
        if button.is_pressed:
            print("Aborted early because of button press")
            return


if __name__ == '__main__':
    # Initialize button and LED strip
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
        aborted_early = visualize_time_elapsing(strip, button)
        if not aborted_early:
            print("Time over!")
            visualize_time_over(strip, button)

        print("Finished")
