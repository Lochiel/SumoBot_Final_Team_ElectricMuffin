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
RED = (8,0,0)
GRN = (0,8,0)
BLU = (0,0,8)

## We create NeoPixel object by passing the constructor a Pin and the Number of LED's in the daisy chain
pin = Pin(1, Pin.OUT)
np = NeoPixel(pin, 12)

## NeoPixel.fill() will pass the same color to every LED
np.fill(BLU)

## NeoPizel.write() is what pushes the changes to the LEDs. Without this, the LEDs won't update
np.write()
led.toggle()
sleep(2)

##We can refrence each LED individually. NeoPixel[0] is the first LED
np[0] = GRN
np[3] = GRN
np[6] = GRN
np[9] = GRN

np.write()
led.toggle()
sleep(1)

## We can read the RGB values of each LED
for i in range(0,3):
    print(i)
    for j in range(0,len(np)):
        print(np[j])
        if np[j] == BLU:
            np[j] = GRN
        elif np[j] == GRN:
            np[j] = RED
        else:
            np[j] = BLU
        led.toggle()
        np.write()
        sleep(0.5)


## Finally, here is an idea for how to refrence sub sections of the led chain
## It feels ugly, so I'm looking for better ways to do it

left = [0,1,2,3,4,5]
right = [11,10,9,8,7,6]

np.fill(BLU)
led.toggle()
np.write()

while True:
    for j in range(0,6):
        print(left[j])
        if np[left[j]] == BLU:
            np[left[j]] = GRN
        elif np[left[j]] == GRN:
            np[left[j]] = RED
        else:
            np[left[j]] = BLU

        if np[right[j]] == BLU:
            np[right[j]] = GRN
        elif np[right[j]] == GRN:
            np[right[j]] = RED
        else:
            np[right[j]] = BLU
        np.write()
        led.toggle()
        sleep(0.25)
