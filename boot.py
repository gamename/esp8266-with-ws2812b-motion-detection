#
#
#
import time

import network
from machine import Pin
from neopixel import NeoPixel

import secrets

motion = False
interrupt_pin = None

# GPIO 14 = D5 on board
MOTION_DETECTOR_PIN = 14

# GPIO 15 = D8 on board
LED_STRIP_CONTROL_PIN = 15

SLEEP_MINUTES = 3

NETWORK_SLEEP_SECONDS = 10

PAUSE_BETWEEN_SENSING = 60 * SLEEP_MINUTES

NUM_PIXELS = 30
LIGHTS_ON = (255, 255, 255)
LIGHTS_OFF = (0, 0, 0)


def wifi_connect(hostname):
    network.hostname(hostname)
    station_if = network.WLAN(network.STA_IF)
    station_if.active(True)
    time.sleep(NETWORK_SLEEP_SECONDS)
    while not station_if.isconnected():
        station_if.connect(secrets.SSID, secrets.PASSWORD)
        time.sleep(NETWORK_SLEEP_SECONDS)
    return True


def handle_interrupt(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin


def main():
    led = Pin(LED_STRIP_CONTROL_PIN, Pin.OUT)
    strip = NeoPixel(led, NUM_PIXELS)
    strip.fill(LIGHTS_OFF)
    strip.write()

    pir = Pin(MOTION_DETECTOR_PIN, Pin.IN)
    pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

    if wifi_connect(secrets.HOSTNAME):
        while True:
            if motion:
                strip.fill(LIGHTS_ON)
                strip.write()
                time.sleep(PAUSE_BETWEEN_SENSING)
                strip.fill(LIGHTS_OFF)
                strip.write()
                motion = False
