from machine import Pin, PWM
from time import sleep
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging
# create PWM object from a pin and set the frequency = 20Hz of slice associated with pin 3
# and duty cycle = 50%, duty_u16 sets the duty cycle as a ratio duty_u16 /65535
#DOUBLE CHECK PINOUT, BENBLS SHOULD BE TO IN2EN ON DRV, BPHASE TO PH


def ir_callback(data, addr, _):
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

# Setup the IR receiver
ir_pin = Pin(18, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)

#Pin.value(x) evaluates x for truthiness. True sets Pin High. False sets Pin Low
FWD = True
REV = False

PWM_MAX = 65535
PWM_MIN = 0

LED = Pin("LED", Pin.OUT)

Aenbl = PWM(Pin(15), freq=2000, duty_u16=32768)
Aphase = Pin(14, Pin.OUT)

Benbl = PWM(Pin(20), freq=2000, duty_u16=32768)
Bphase = Pin(19, Pin.OUT)

def ChangeGear(motor, gear_pin, gear):
    motor.duty_u16(0)
    sleep(2)
    if type(gear) is bool:
        gear_pin.value(gear)
        LED.toggle()

def ChangeSpeed(motor, speed):
     speed_value = int( (speed/100) * PWM_MAX ) ## Convert speed to a percentage. Apply that to large
     motor.duty_u16(speed_value)

while True:
    ChangeGear(Aenbl, Aphase, FWD)
    ChangeSpeed(Aenbl, 50)
    print("Motor A : Forward")

    ChangeGear(Benbl, Bphase, FWD)
    ChangeSpeed(Benbl, 50)
    print("Motor B : Forward")

    ChangeGear(Aenbl, Aphase, REV)
    ChangeSpeed(Aenbl, 50)
    print("Motor A : Reverse")

    ChangeGear(Benbl, Bphase, REV)
    ChangeSpeed(Benbl, 50)
    print("Motor B : Reverse")