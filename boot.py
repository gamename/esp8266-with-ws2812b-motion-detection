#
# This is a simple configuration to drive a ws2812b strip of LEDs using a esp2866 microcontroller
#
from machine import Pin
from neopixel import NeoPixel
from time import sleep
import network

motion = False
interrupt_pin = None

# Turn OFF the wifi signal
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
np = NeoPixel(led, NUM_PIXELS)
np.fill(LIGHTS_OFF)
np.write()

pir = Pin(PIN_D5, Pin.IN)

pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

while True:
    if motion:
        # print('Motion detected! Interrupt caused by:', interrupt_pin)
        np.fill(LIGHTS_ON)
        np.write()
        sleep(SLEEP_INTERVAL)
        np.fill(LIGHTS_OFF)
        np.write()
        # print('Motion stopped!')
        motion = False
