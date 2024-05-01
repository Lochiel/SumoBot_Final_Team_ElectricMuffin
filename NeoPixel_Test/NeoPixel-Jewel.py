from neopixel import NeoPixel
from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)
led.value(1)

##  3v - 5v input
## connect Data In (GRN) to GIO1, pin 2
## Data Out (BlU) isn't used 

## NeoPixel uses a RGB tuple to define colors. We can predfine these colors
## NepPixels are bright. Max values are 255, yet for this demonstration we are using a fraction of that
# COLOR = (RED, GREEN, BLUE)
RED = (10,0,0)
GREEN = (0,10,0)
BLUE = (0,0,10)
PURPLE = (5,1,20)
ORANGE = (25,5,0)
PINK = (20,1,10)
YELLOW = (20,20,0)
BLU = (200,200,200)

## We create NeoPixel object by passing the constructor a Pin and the Number of LED's in the daisy chain
pin = Pin(15, Pin.OUT)
np = NeoPixel(pin, 7)


# #We can refrence each LED individually. NeoPixel[0] is the first LED
# np[0] = PURPLE
# np[1] = ORANGE
# np[2] = YELLOW
# np[3] = GREEN
# np[4] = BLUE
# np[5] = PINK
# np[6] = RED
# led.toggle()
# sleep(2)
# np.write()

# color_list = [RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE,PINK]

# j = 0
# for i in range(len(np)):
#   if j > len(color_list)-1:
#      j=0
#   np[i] = color_list[j]
#   j += 1
# np.write()

# def NextColor(current_color, color_list):
#   print(current_color)
#   for i in range(len(color_list)):
#     if i == len(color_list)-1:
#         return color_list[0]
#     elif color_list[i] == current_color:
#         return color_list[i+1]
#   # return color_list[0]

# while True:
#   for i in range(0,7):
#     Target_color = NextColor(np[i], color_list)
#     print(f"{i}: {Target_color}")
#     np[i] = Target_color
#   np.write()
#   sleep(0.5)

# # ########################################################
# # ################ FIGHT MODE CODE BELOW #################
# # ########################################################

brightness = 25
delay = .25
redJewel = (brightness,0,0) 


while True:
    for i in range(1, len(np)):
        np[i] = redJewel
        np.write()
        sleep(.1)
        np[i] = (0,0,0)

 
    