#
# Light the area underneath my work desk automatically
#
import gc
import time

import network
from machine import Pin
from neopixel import NeoPixel

strip = None
motion_detected = False
interrupt_pin = None

# GPIO 14 = D5 on board
MOTION_DETECTOR_PIN = 14

# GPIO 0 = D3 on board
LED_STRIP_CONTROL_PIN = 0

NUM_PIXELS = 30
LIGHTS_ON = (255, 255, 255)
LIGHTS_OFF = (0, 0, 0)


def turn_lights_on(duration_hours=1):
    strip.fill(LIGHTS_ON)
    strip.write()
    sleep_seconds = 60 * duration_hours
    time.sleep(sleep_seconds)


def turn_lights_off():
    strip.fill(LIGHTS_OFF)
    strip.write()

def handle_interrupt(pin):
    global motion_detected
    motion_detected = True
    global interrupt_pin
    interrupt_pin = pin


def main():
    #
    # Turn OFF the access point interface
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    #
    # Turn OFF the station interface
    st_if = network.WLAN(network.STA_IF)
    st_if.active(False)

    led = Pin(LED_STRIP_CONTROL_PIN, Pin.OUT)

    global strip
    strip = NeoPixel(led, NUM_PIXELS)

    turn_lights_off()

    pir = Pin(MOTION_DETECTOR_PIN, Pin.IN)
    pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

    while True:
        if motion_detected:
            turn_lights_on(duration_hours=4)
            turn_lights_off()
            #
            # Make sure we do not generate mem leaks over time
            gc.collect()



if __name__ == "__main__":
    main()
