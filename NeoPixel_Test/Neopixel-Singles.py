from neopixel import NeoPixel
from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)
led.value(1)

# ##  3v - 5v input
# ## connect Data In (GRN) to GIO1, pin 2
# ## Data Out (BlU) isn't used 

# ## NeoPixel uses a RGB tuple to define colors. We can predfine these colors
# ## NepPixels are bright. Max values are 255, yet for this demonstration we are using a fraction of that
# # COLOR = (GREEN, RED, BLUE)
# RED2 = (0,20,0)
# ORANGE2 = (7,25,0)
# YELLOW2 = (10,15,0)
# GREEN2 = (10,0,0)
# BLUE2 = (7,1,20) 
# PURPLE2 = (0,15,50)
# PINK2 = (0,25,30)
# OFF = (0,0,0)

# ## We create NeoPixel object by passing the constructor a Pin and the Number of LED's in the daisy chain
pin2 = Pin(18, Pin.OUT)
np2 = NeoPixel(pin2, 8)

# color_list2 = [RED2,ORANGE2,YELLOW2,GREEN2,BLUE2,PURPLE2,PINK2]

# j = 0
# for i in range(len(np2)):
#   if j > len(color_list2)-1:
#      j=0
#   np2[i] = color_list2[j]
#   j += 1
# np2.write()

# def NextColor2(current_color2, color_list2):
#   print(current_color2)
#   for i in range(len(color_list2)):
#     if i == len(color_list2)-1:
#         return color_list2[0]
#     elif color_list2[i] == current_color2:
#         return color_list2[i+1]
#   # return color_list[0]

# while True:
#   for i in range(0,4): #The second number must be the exact number of neopixels to work
#     Target_color2 = NextColor2(np2[i], color_list2)
#     print(f"{i}: {Target_color2}")
#     np2[i] = Target_color2
#   np2.write()
#   sleep(0.1)


########################################################
################ FIGHT MODE CODE BELOW #################
########################################################

# we use the same brightness for each color
brightness = 25
delay = .25
# here we define variables for each color
#SINGLES: red = (0,brightness, 0) 
red = (0,brightness,0) 


while True:
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


