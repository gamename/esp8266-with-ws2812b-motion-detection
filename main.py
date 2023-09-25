#
#
#
import gc
import time

import network
from machine import Pin, reset
from neopixel import NeoPixel
from ota import OTAUpdater

import secrets

motion = False
interrupt_pin = None

# GPIO 14 = D5 on board
MOTION_DETECTOR_PIN = 14

# GPIO 0 = D3 on board
LED_STRIP_CONTROL_PIN = 0

SLEEP_MINUTES = 240

NETWORK_SLEEP_INTERVAL = 10
NETWORK_MAX_CONNECTION_ATTEMPTS = 10

PAUSE_BETWEEN_SENSING = 60 * SLEEP_MINUTES

OTA_UPDATE_GITHUB_CHECK_INTERVAL = 14400  # seconds (4 hours)

OTA_UPDATE_GITHUB_REPOS = {
    "gamename/esp8266-with-ws2812b-motion-detection": ["boot.py", "main.py"],
    "gamename/micropython-over-the-air-utility": ["ota.py"]
}


NUM_PIXELS = 30
LIGHTS_ON = (255, 255, 255)
LIGHTS_OFF = (0, 0, 0)


def wifi_connect(wlan):
    """
    Connect to Wi-Fi

    :param: watchdog - a watchdog timer
    :param: wlan - a Wi-Fi network handle

    Returns:
        Nothing
    """
    print("WIFI: Attempting network connection")
    wlan.active(True)
    time.sleep(NETWORK_SLEEP_INTERVAL)
    counter = 0
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    while not wlan.isconnected():
        print(f'WIFI: Attempt: {counter}')
        time.sleep(NETWORK_SLEEP_INTERVAL)
        counter += 1
        if counter > NETWORK_MAX_CONNECTION_ATTEMPTS:
            print("WIFI: Network connection attempts exceeded. Restarting")
            time.sleep(1)
            reset()
    print("WIFI: Successfully connected to network")


def handle_interrupt(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin


def main():
    #
    # Set up a timer to force reboot on system hang
    network.hostname(secrets.HOSTNAME)
    #
    # Turn OFF the access point interface
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    #
    # Turn ON and connect the station interface
    wlan = network.WLAN(network.STA_IF)
    wifi_connect(wlan)

    led = Pin(LED_STRIP_CONTROL_PIN, Pin.OUT)
    strip = NeoPixel(led, NUM_PIXELS)
    strip.fill(LIGHTS_OFF)
    strip.write()

    pir = Pin(MOTION_DETECTOR_PIN, Pin.IN)
    pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

    ota_updater = OTAUpdater(secrets.GITHUB_USER,
                             secrets.GITHUB_TOKEN,
                             OTA_UPDATE_GITHUB_REPOS)
    ota_timer = time.time()
    while True:
        if motion:
            strip.fill(LIGHTS_ON)
            strip.write()
            time.sleep(PAUSE_BETWEEN_SENSING)
            strip.fill(LIGHTS_OFF)
            strip.write()

        ota_elapsed = int(time.time() - ota_timer)
        if ota_elapsed > OTA_UPDATE_GITHUB_CHECK_INTERVAL:
            #
            # The update process is memory intensive, so make sure
            # we have all the resources we need.
            gc.collect()
            # micropython.mem_info()
            if ota_updater.updated():
                print("MAIN: Restarting device after update")
                time.sleep(1)  # Gives the system time to print the above msg
                reset()
            ota_timer = time.time()




if __name__ == "__main__":
    main()
