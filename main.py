"""
Turn on lights under my desk
"""
import time

import network
import ntptime
from machine import Pin, reset
from neopixel import NeoPixel

import secrets

# GPIO 14 = D5 on board
MOTION_DETECTOR_PIN = 14

# GPIO 0 = D3 on board
LED_STRIP_CONTROL_PIN = 0

NUM_PIXELS = 30
LIGHTS_ON = (255, 255, 255)
LIGHTS_OFF = (0, 0, 0)

FOUR_HOURS = 4 * 3600  # in seconds


def wifi_connect(wlan, ssid, password, connection_attempts=10, sleep_seconds_interval=3):
    """
    Start a Wi-Fi connection

    :param wlan: A network handle
    :type wlan: network.WLAN
    :param ssid: Wi-Fi SSID
    :type ssid: str
    :param password: Wi-Fi password
    :type password: str
    :param connection_attempts: How many times should we attempt to connect?
    :type connection_attempts: int
    :param sleep_seconds_interval: Sleep time between attempts
    :type sleep_seconds_interval: int
    :return: Nothing
    :rtype: None
    """
    print("WIFI: Attempting network connection")
    wlan.active(True)
    time.sleep(sleep_seconds_interval)
    counter = 1
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print(f'WIFI: Attempt {counter} of {connection_attempts}')
        time.sleep(sleep_seconds_interval)
        counter += 1
        if counter > connection_attempts:
            print("WIFI: Max connection attempts exceeded. Resetting microcontroller")
            time.sleep(0.5)
            reset()
    print("WIFI: Successfully connected to network")


def main():
    print("MAIN: Set Hostname.")
    network.hostname(secrets.HOSTNAME)
    #
    print("MAIN: Turn OFF the access point interface")
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    #
    print("MAIN: Turn ON and connect the station interface")
    wlan = network.WLAN(network.STA_IF)
    wifi_connect(wlan, secrets.SSID, secrets.PASSWORD)

    print("MAIN: Sync system time with NTP")
    try:
        ntptime.settime()
        print("MAIN: System time set successfully.")
    except Exception as e:
        print(f"MAIN: Error setting system time: {e}")
        time.sleep(0.5)
        reset()

    led = Pin(LED_STRIP_CONTROL_PIN, Pin.OUT)

    strip = NeoPixel(led, NUM_PIXELS)
    strip.fill(LIGHTS_OFF)
    strip.write()

    pir = Pin(MOTION_DETECTOR_PIN, Pin.IN)

    start_time = None

    print("MAIN: Starting event loop")
    while True:
        motion_detected = bool(pir.value())

        if motion_detected and not start_time:
            print("MAIN: Record the start time when motion is first detected")
            start_time = time.time()

            print("MAIN: Turn on the LED strip")
            strip.fill(LIGHTS_ON)
            strip.write()

        elif start_time and time.time() - start_time >= FOUR_HOURS:
            print("MAIN: Time is up.  Reset start time.")
            start_time = None

            print("MAIN: Turn lights off")
            strip.fill(LIGHTS_OFF)
            strip.write()

        if not wlan.isconnected():
            print("MAIN: Restart network connection")
            wifi_connect(wlan, secrets.SSID, secrets.PASSWORD)

        time.sleep(0.5)


if __name__ == "__main__":
    main()
