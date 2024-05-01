from neopixel import NeoPixel
from machine import Pin
from time import sleep
import uasyncio as asyncio


#TEST REMOVE LATER
RUN=True

led = Pin("LED", Pin.OUT)
led.value(1)

##  3v - 5v input
## connect Data In (GRN) to GIO1, pin 2
## Data Out (BlU) isn't used 

## NeoPixel uses a RGB tuple to define colors. We can predfine these colors
## NepPixels are bright. Max values are 255, yet for this demonstration we are using a fraction of that
# COLOR = (RED, GREEN, BLUE)
RED = (10,0,0)   #JEWEL
GREEN = (0,10,0)
BLUE = (0,0,10)
PURPLE = (5,1,20)
ORANGE = (25,5,0)
PINK = (20,1,10)
YELLOW = (20,20,0)
color_list = [RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE,PINK]

RED2 = (0,20,0)   #singles
ORANGE2 = (7,25,0)
YELLOW2 = (10,15,0)
GREEN2 = (10,0,0)
BLUE2 = (7,1,20) 
PURPLE2 = (0,15,50)
PINK2 = (0,25,30)
OFF = (0,0,0)
color_list2 = [RED2,ORANGE2,YELLOW2,GREEN2,BLUE2,PURPLE2,PINK2]

brightness = 25
delay = .25
redJewel = (brightness,0,0) 
red = (0,brightness,0) 
i = 0
mode = 0

#Singles Pinout
pin2 = Pin(18, Pin.OUT)
np2 = NeoPixel(pin2, 8)


#Jewel Pinout
pin = Pin(15, Pin.OUT)
np = NeoPixel(pin, 7)

def RedpatternJ(neopixel: NeoPixel):
        for i in range(1, len(np)):
            np[i] = redJewel
            np.write()
            sleep(.1)
            np[i] = (0,0,0)

def RedpatternS(neopixel):
    for i in range(0, len(np2)-1):
        np2[i] = red
        np2.write()
        sleep(.09)
        np2[i] = (0,0,0)
    for i in range(len(np2)-1,0,-1):
        np2[i] = red
        np2.write()
        sleep(.09)
        np2[i] = (0,0,0)

def SingleInit(neopixel: NeoPixel, colorlist):
    j = 0
    for i in range(len(neopixel)):
        if j > len(colorlist)-1:
            j=0
        neopixel[i] = colorlist[j]
        j += 1
    neopixel.write()

def NextColor2(current_color2, color_list2):
#   print(current_color2)
  for i in range(len(color_list2)):
    if i == len(color_list2)-1:
        return color_list2[0]
    elif color_list2[i] == current_color2:
        return color_list2[i+1]
  # return color_list[0]

def RunPattern(neopixel: NeoPixel, colorlist):
    # while RUN: 
        for i in range(len(neopixel)):
            Target_color2 = NextColor2(neopixel[i], colorlist)
            # print(f"{i}: {Target_color2}")
            neopixel[i] = Target_color2
        neopixel.write()
        # await asyncio.sleep(0.1)

def RainbowPattern(neopixel: NeoPixel, colorlist=color_list2):
    SingleInit(neopixel, colorlist)
    RunPattern(neopixel, colorlist)

# def SetMode(mode: int):
#     if mode ==1 :
#         RunPattern(np,color_list)
#         RunPattern(np2, color_list2)
#         sleep(.1)
#     elif mode == 2:
#         RedpatternJ(np2)
#         RedpatternS(np)
#         sleep(.2)
#     elif mode == 0:
#         np2.fill(OFF)
#         np.fill(OFF)
        
# button_a = 0
# button_b = 0

# def update():
#  while True:
#     if button_a == 1:
#         mode = 1
#     elif button_b == 1:
#        mode = 2

    

SingleInit(np,color_list)
SingleInit(np2,color_list2)

while True:
    RunPattern(np,color_list)
    RunPattern(np2, color_list2)
    # RedpatternJ(np2)
    # RedpatternS(np)
    sleep(0.1)
# asyncio.run(RainbowPattern(np, color_list))
# asyncio.run(RainbowPattern(np2, color_list2))



