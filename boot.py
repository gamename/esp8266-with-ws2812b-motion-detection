#
# This is a simple configuration to drive a ws2812b strip of LEDs using a esp2866 microcontroller
#
from time import sleep

import network
from machine import Pin
from neopixel import NeoPixel

motion = False
interrupt_pin = None

# Turn Wi-Fi OFF
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)


def handle_interrupt(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin


# GPIO 0 = D3 on board
PIN_D3 = 0
# GPIO 14 = D5 on board
PIN_D5 = 14

SLEEP_MINUTES = 3
SLEEP_INTERVAL = 60 * SLEEP_MINUTES
NUM_PIXELS = 55
LIGHTS_ON = (255, 255, 255)
LIGHTS_OFF = (0, 0, 0)
led = Pin(PIN_D3, Pin.OUT)
strip = NeoPixel(led, NUM_PIXELS)
strip.fill(LIGHTS_OFF)
strip.write()

pir = Pin(PIN_D5, Pin.IN)

pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

while True:
    if motion:
        strip.fill(LIGHTS_ON)
        strip.write()
        sleep(SLEEP_INTERVAL)
        strip.fill(LIGHTS_OFF)
        strip.write()
        motion = False
