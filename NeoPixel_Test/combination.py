from neopixel import NeoPixel
from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)
led.value(1)

np = 7
pin = 15

strip = NeoPixel(Pin(pin), np)

# we use the same brightness for each color
brightness = 25
delay = .25
# here we define variables for each color
#SINGLES: red = (0,brightness, 0) #JEWEL: red = (brightness,0,0)
red = (brightness,0,0) 


while True:
    for i in range(1, np):
        strip[i] = red
        strip.write()
        sleep(.1)
        strip[i] = (0,0,0)
        
    
    


