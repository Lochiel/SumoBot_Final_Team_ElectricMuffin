from Motor import Motor
from machine import Pin
from time import sleep_ms

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

LED = Pin("LED", Pin.OUT)

MotorA = Motor(15,14)
MotorB = Motor(20,19)

while True:
    MotorA.gear(Motor.FWD)
    MotorA.speed(50)
    print("Motor A : Forward")
    LED.toggle()

    MotorB.gear(Motor.FWD)
    MotorB.speed(50)
    print("Motor B : Forward")
    LED.toggle()

    sleep_ms(3000)

    MotorA.gear(Motor.REV)
    MotorA.speed(50)
    print("Motor A : Reverse")
    LED.toggle()

    MotorB.gear(Motor.REV)
    MotorB.speed(50)
    print("Motor B : Reverse")
    LED.toggle()

    sleep_ms(3000)
