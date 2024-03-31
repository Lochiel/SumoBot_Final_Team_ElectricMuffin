from Motor import Motor
from machine import Pin
from time import sleep_ms

from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

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
    MotorA.fwd(50)
    MotorB.fwd(50)
    print("Motor A & B : Forward")
    LED.toggle()

    sleep_ms(3000)

    MotorA.rev(50)
    MotorB.rev(50)
    print("Motor A & B : Reverse")
    LED.toggle()

    sleep_ms(3000)
