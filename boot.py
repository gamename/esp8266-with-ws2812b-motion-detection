#
# This is a simple configuration to drive a ws2812b strip of LEDs
# using an esp2866 microcontroller
#
from time import sleep

import network
from machine import Pin
from neopixel import NeoPixel

import secrets

motion = False
interrupt_pin = None


def do_connect():
    station_if = network.WLAN(network.STA_IF)
    if not station_if.isconnected():
        print('connecting to network...')
        station_if.active(True)
        station_if.connect('disconnected', secrets.password)
        while not station_if.isconnected():
            pass
    print('network config:', station_if.ifconfig())


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

do_connect()

while True:
    if motion:
        strip.fill(LIGHTS_ON)
        strip.write()
        sleep(SLEEP_INTERVAL)
        strip.fill(LIGHTS_OFF)
        strip.write()
        motion = False
