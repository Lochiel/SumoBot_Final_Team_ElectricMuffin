## Psuedo Code

## Goals
## Have basic control code setup 

## TODO seperate Main.py, Motors.py, and RX.py, etc into seperate modules
## TODO Break out repeating code into functions
## TODO Set up interrupts/callback sequences

#TODO Write Back Sensor Handling

# Constants for PWM
PWM_MAX = 65535
PWM_MIN = 0
pwm_custom = int(PWM_MAX / 2)

# Motor Class Definition
class Motor:
    def __init__(self, drive_pin, gear_pin, frequency=2000):
        self.drive_pin = PWM(Pin(drive_pin), freq=frequency)
        self.gear_pin = Pin(gear_pin, Pin.OUT)
        self.drive_pin.duty_u16(PWM_MIN)  # Ensure motor is off initially

    def control_motor(self, action, pwm_value=PWM_MIN):
        self.gear_pin.value(action)  # action: 0 for forward, 1 for reverse
        sleep(0.1)
        self.drive_pin.duty_u16(pwm_value)


## Interrupt based main.py

import constants
from constants import command_codes
import uasyncio as asyncio
from RX import IR_RX

#TODO Replace placeholders with functions in respective modules
def MotorFWD(speed:int): #Placeholder, actual function should be in Motors.py
    print("MotorFWD called with value: ",speed)
    pass

def MotorREV(): #Placeholder, actual function should be in Motors.py
    print("MotorREV called")
    pass

def MotorCW(speed:int): #Placeholder, actual function should be in Motors.py
    print("MotorCW called with value: ", speed)
    pass

def MotorCCW(speed:int): #Placeholder, actual function should be in Motors.py
    print("MotorCCW called with value: ", speed)
    pass

def MotorSTOP():
    print("MotorSTOP called")
    pass

def NeoPixelMode(mode:int): #Placeholder, actual function should be in SumoNeoPixels.py
    print("NeoPixelMode called with value: ", mode)
    pass

def BackSensor_Toggle(): #Placeholder, actual function should be in DistanceSenor.py
    print("DistanceSensor_Toggle called")
    pass

#TODO Replace callbacks with functions in modules
#TODO Replace placeholder numbers with constants
# Names like MotorFWD, MotorREV, MotorCW, MotorCCW are placeholders. 
# They should be replaced with the names of function that is supposed to be called when the coressponding command code is recieved
# arguments that need to be passed to that function should follow
command_codes["FWD_SLOW"].setCallback(MotorFWD, 25)
command_codes["FWD_FAST"].setCallback(MotorFWD, 50)
command_codes["FWD_TURBO"].setCallback(MotorFWD, 100)

command_codes["REV"].setCallback(MotorREV, None)

command_codes["CW_SLOW"].setCallback(MotorCW, 25)
command_codes["CW_FAST"].setCallback(MotorCW, 50)

command_codes["CCW_SLOW"].setCallback(MotorCCW, 25)
command_codes["CCW_FAST"].setCallback(MotorCCW, 50)

command_codes["STOP"].setCallback(MotorSTOP, None)

command_codes["NP_1"].setCallback(NeoPixelMode, 1)
command_codes["NP_2"].setCallback(NeoPixelMode, 2)
command_codes["NP_3"].setCallback(NeoPixelMode, 2)

command_codes["SEN_BACK"].setCallback(BackSensor_Toggle, None)

#TODO write RX processing fuction. This will be called by the RX module when it recieves a valid data package

## This will compare the recieved data to the codes in command_codes
## If a match is found, it will call the stored function with the stored value
def callback_RX(data: int):
    for _ in command_codes: 
        if command_codes[_] == data:
            FuncToCall = command_codes[_].callback
            ArgToPass = command_codes[_].args
            if ArgToPass is None:
                FuncToCall()
            else:
                FuncToCall(ArgToPass)
            return
    print("Error: "+ hex(data) + "recieved. Unable to match")

IR_Reciever = IR_RX(constants.PIN_RX, constants.ADDRESS, callback_RX)

#TODO setup Initalizations
#     Init BackSensor(Pin, Distance, CheckDelay, MotorSpin_callbackFunction)
#     Init Motors(MotorA pin1, MotorA pin2, MotorB pin1, MotorB pin2, MotorA_SpinDirection, MotorB_SpinDirection)
#     Init NeoPixels(Pin1, Pin2)

TESTING = True

async def _testCallBack():
    for _ in command_codes:
        print("Testing Code: ", command_codes[_])
        callback_RX(command_codes[_].code)
        await asyncio.sleep(2)

# Setup Motor Instances
motor_a = Motor(drive_pin=15, gear_pin=14)
motor_b = Motor(drive_pin=20, gear_pin=19)

# IR Receiver Callback Function
async def motor_callback(data, addr, _):
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
    
    # Motor A Control
    if data == 0xa0:
        motor_a.control_motor(action=0)  # StopMotor A
    elif data == 0xa1:
        motor_a.control_motor(action=0, pwm_value=pwm_custom)  # MotorA forward
    elif data == 0xa2:
        motor_a.control_motor(action=1, pwm_value=pwm_custom)  # MotorA reverse
    
    # Motor B Control
    if data == 0xb0:
        motor_b.control_motor(action=0)  # StopMotor B
    elif data == 0xb1:
        motor_b.control_motor(action=0, pwm_value=pwm_custom)  # MotorB forward
    elif data == 0xb2:
        motor_b.control_motor(action=1, pwm_value=pwm_custom)  # MotorB reverse

async def main():
    if TESTING:
        await _testCallBack()
    else:
        while True:
            await asyncio.sleep_ms(50)
            pass

_ = main()