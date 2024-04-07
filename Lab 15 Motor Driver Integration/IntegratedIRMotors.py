from machine import Pin, PWM
from time import sleep
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging
# create PWM object from a pin and set the frequency = 20Hz of slice associated with pin 3
# and duty cycle = 50%, duty_u16 sets the duty cycle as a ratio duty_u16 /65535
#DOUBLE CHECK PINOUT, BENBLS SHOULD BE TO IN2EN ON DRV, BPHASE TO PH


def ir_callback(data, addr, _):
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

    # Each if-statement specifies a state that the motor will be at, based on which hex value is being transmitted


    # Turns A motor off
    if(data == 0xa0): 
        Athrottle.duty_u16(PWM_MIN)
        sleep(0.1)
        Agear.value(0)

    # Starts A motor forward 
    elif(data == 0xa1):
        Athrottle.duty_u16(PWM_MIN)
        sleep(0.1)
        Agear.value(0)
        Athrottle.duty_u16(pwm_custom)
        
    # Starts A motor backwards 
    elif(data == 0xa2):
        Athrottle.duty_u16(PWM_MIN)
        sleep(0.1)
        Agear.value(1)
        Athrottle.duty_u16(pwm_custom)
        
    # Turns B motor off
    elif(data == 0xb0):
        Bthrottle.duty_u16(PWM_MIN)
        sleep(0.1)
        Bgear.value(0)
    
    # Starts B motor forwards
    elif(data == 0xb1):
        Bthrottle.duty_u16(PWM_MIN)
        sleep(0.1)
        Bgear.value(0)
        Bthrottle.duty_u16(pwm_custom)
    
    # Starts B motor backwards
    elif(data == 0xb2):
        Bthrottle.duty_u16(PWM_MIN)
        sleep(0.1)
        Bgear.value(1)
        Bthrottle.duty_u16(pwm_custom)


# Setup the IR receiver
ir_pin = Pin(18, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)

PWM_MAX = 65535
PWM_MIN = 0
LED = Pin("LED", Pin.OUT)
pwm_custom = int(65535/2)

Bthrottle = PWM(Pin(20), freq=2000, duty_u16=32768)
Bgear = Pin(19, Pin.OUT)
Bthrottle.duty_u16(pwm_custom)

Athrottle = PWM(Pin(15), freq=2000, duty_u16=32768)
Agear = Pin(14, Pin.OUT)
Athrottle.duty_u16(pwm_custom)

while True:
    pass
# while True: 
#     if(addr == 0xa0):        
#     if(addr == 0xa1):
#     if(addr == 0xb0):
#     if(addr == 0xb1):

#     Bthrottle.duty_u16(0)
#     sleep(2)
#     print("Motor B : Forward")
#     Bgear.value(0)
#     LED.toggle()
#     Bthrottle.duty_u16(pwm_custom)
#     sleep(2)

#     Bthrottle.duty_u16(0)
#     sleep(.2)
#     print("Motor B : Backward") 
#     Bgear.toggle()
#     LED.toggle()
#     Bthrottle.duty_u16(pwm_custom)
#     sleep(2)

#     Athrottle.duty_u16(0)
#     sleep(2)
#     print("Motor A : Forward")
#     Agear.value(0)
#     LED.toggle()
#     Bthrottle.duty_u16(pwm_custom)
#     sleep(2)

#     Athrottle.duty_u16(0)
#     sleep(.2)
#     print("Motor A : Backward") 
#     Agear.toggle()
#     LED.toggle()
#     Athrottle.duty_u16(pwm_custom)
#     sleep(2)
