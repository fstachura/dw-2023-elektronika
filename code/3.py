from machine import Pin
import time

button = Pin(16, Pin.IN, pull=Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)
led.value(0)

while True:
    print(button.value())
    led.value(button.value())
    time.sleep(0.1)

