from neopixel import NeoPixel
from machine import Pin
import random

_MAX_VALUE = 255 #Max value of the LED.
# NeoPixels accept a max color of 255, but that is very bright and can wash out colors
_MED_VALUE = 128 #For a medium amount of color
_LOW_VALUE = 32 #Just a touch of color


def _randColorGenerator(red=(0,_MAX_VALUE), green=(0,_MAX_VALUE), blue=(0,_MAX_VALUE)):
    R = random.randrange(red[0],red[1])
    G = random.randrange(green[0],green[1])
    B = random.randrange(blue[0],blue[1])
    return (R,G,B)

def _randColor():
    possibleColors = (_randRed, _randGreen, _randBlue)
    color = random.choice(possibleColors)()
    return color

def _randRed():
    return _randColorGenerator((_MAX_VALUE,_MAX_VALUE),(0,_MED_VALUE),(0,_MED_VALUE))

def _randGreen():
    return _randColorGenerator((0,_MED_VALUE),(_MAX_VALUE,_MAX_VALUE),(0,_MED_VALUE))

def _randBlue():
    return _randColorGenerator((0,_MED_VALUE),(0,_MED_VALUE),(_MAX_VALUE,_MAX_VALUE))

def _randWhite():
    return _randColorGenerator((_MED_VALUE,_MAX_VALUE),(_MED_VALUE,_MAX_VALUE),(_MED_VALUE,_MAX_VALUE))

def _randDull():
    return _randColorGenerator((0,_MED_VALUE),(0,_MED_VALUE),(0,_MED_VALUE))

class Demo():

    def __init__(self, GPIO, size):
        self.pin = Pin(GPIO, Pin.OUT)
        self.np = NeoPixel(self.pin,size)
        self.size = size

    def update(self):
        i = random.randrange(0,self.size)
        self.np[i] = _randColor()
        self.np.write()
        print(self.np[i])

class Clock():

    location = 0

    def __init__(self, GPIO, size, handSize=1, handcolor=_randGreen(), facecolor=_randBlue()):
        self.pin = Pin(GPIO, Pin.OUT)
        self.np = NeoPixel(self.pin,size)
        self.size = size
        self.HandSize = handSize
        self.HandColor = handcolor
        self.FaceColor = facecolor
        self.update()

    def update(self):
        self.np.fill(self.FaceColor)
        for _ in range(0,self.HandSize):
            self.location = (self.location+1)%self.size
            self.np[self.location] = self.HandColor