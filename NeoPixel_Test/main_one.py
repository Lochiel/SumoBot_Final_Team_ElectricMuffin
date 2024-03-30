import T2_NeoPixel_Ring
import random
from neopixel import NeoPixel
from machine import Pin
from time import sleep

#Be sure to upload the T2_NeoPixel_Ring file to the pico first

led = Pin("LED", Pin.OUT)

## This is the 3rd method
Demo1 = T2_NeoPixel_Ring.Demo(1, 12)

while True:
    led.toggle()
    Demo1.update()
    sleep(2)