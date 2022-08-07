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

SLEEP_MINUTES = 1
SLEEP_INTERVAL = 60 * SLEEP_MINUTES
NUM_PIXELS = 30
ON = (255, 255, 255)
OFF = (0, 0, 0)
led = Pin(PIN_D3, Pin.OUT)
np = NeoPixel(led, NUM_PIXELS)
np.fill(OFF)
np.write()

pir = Pin(PIN_D5, Pin.IN)

pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

while True:
    if motion:
        # print('Motion detected! Interrupt caused by:', interrupt_pin)
        np.fill(ON)
        np.write()
        sleep(SLEEP_INTERVAL)
        np.fill(OFF)
        np.write()
        # print('Motion stopped!')
        motion = False
