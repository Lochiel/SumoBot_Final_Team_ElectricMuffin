# SumoBot Control Main
# Cam Chalmers, Anusha Venka, Melissa Clark
# ECEN 2440 - Applications of Embedded System. Spring '24
#

#TODO Write Neo-Pixel Handling
#TODO Write Back Sensor Handling

## Interrupt based main.py

import constants
from constants import command_codes
import uasyncio as asyncio
from RX import IR_RX
from machine import Pin
from Motor import Motor
from time import sleep
import constants
import distance_sensor

led = Pin(constants.PIN_LED1, Pin.OUT)
led2 = Pin(constants.PIN_LED2, Pin.OUT)
led3 = Pin(constants.PIN_LED3, Pin.OUT)
led4 = Pin(constants.PIN_LED4, Pin.OUT)

led.value(1) #Turn on board led, it'll be turned off whene everything is loaded... ie very quickly
led2.value(0)
led3.value(0)
led4.value(0)

# Setup Motor Instances
motor_a = Motor(constants.PIN_MOTOR_A_THROTTLE, constants.PIN_MOTOR_A_GEAR)
motor_b = Motor(constants.PIN_MOTOR_B_THROTTLE, constants.PIN_MOTOR_B_GEAR)

motor_a.stop()
motor_b.stop()

#TODO Replace placeholders with functions in respective modules
def MotorFWD(speed:int): #Placeholder, actual function should be in Motors.py
    # print("MotorFWD called with value: ",speed)
    motor_a.fwd(speed)
    motor_b.fwd(speed)
    print(f"Motor_A: {motor_a} Motor_B: {motor_b}")


def MotorREV(speed:int): #Placeholder, actual function should be in Motors.py
    # print("MotorREV called", speed)
    motor_a.rev(speed)
    motor_b.rev(speed)
    print(f"Motor_A: {motor_a} Motor_B: {motor_b}")

def MotorCW(speed:int): #Placeholder, actual function should be in Motors.py
    print("MotorCW called with value: ", speed)
    motor_a.fwd(speed)
    motor_b.rev(speed)
    print(f"Motor_A: {motor_a} Motor_B: {motor_b}")
    pass

def MotorCCW(speed:int): #Placeholder, actual function should be in Motors.py
    print("MotorCCW called with value: ", speed)
    motor_a.rev(speed)
    motor_b.fwd(speed)
    print(f"Motor_A: {motor_a} Motor_B: {motor_b}")
    pass

def MotorSTOP():
    # print("MotorSTOP called")
    motor_a.stop()
    motor_b.stop()
    print(f"Motor_A: {motor_a} Motor_B: {motor_b}")

def NeoPixelMode(mode:int): #Placeholder, actual function should be in SumoNeoPixels.py
    if mode == 1:
        led2.toggle()
    elif mode == 2:
        led3.toggle()
    elif mode == 3:
        led4.toggle()

    print("NeoPixelMode called with value: ", mode)
    pass

def BackSensor_Toggle(): #Placeholder, actual function should be in DistanceSenor.py
    print("DistanceSensor_Toggle called")
    pass

async def TurnMotors(turn): # If check_distance (in distancesensor.py) returns true, turn Bot CW
    if(turn): 
        MotorCW(50)
        await asyncio.sleep(3)
        MotorSTOP()
    pass

## Set the callback functions for each command code
command_codes["FWD_SLOW"].setCallback(MotorFWD, 25)
command_codes["FWD_FAST"].setCallback(MotorFWD, 50)
command_codes["FWD_TURBO"].setCallback(MotorFWD, 100)

command_codes["REV"].setCallback(MotorREV, 50)

command_codes["CW_SLOW"].setCallback(MotorCW, 25)
command_codes["CW_FAST"].setCallback(MotorCW, 50)

command_codes["CCW_SLOW"].setCallback(MotorCCW, 25)
command_codes["CCW_FAST"].setCallback(MotorCCW, 50)

command_codes["STOP"].setCallback(MotorSTOP, None)

command_codes["NP_1"].setCallback(NeoPixelMode, 1)
command_codes["NP_2"].setCallback(NeoPixelMode, 2)
command_codes["NP_3"].setCallback(NeoPixelMode, 3)

command_codes["SEN_BACK"].setCallback(BackSensor_Toggle, None)

## This will compare the recieved data to the codes in command_codes
## If a match is found, it will call the stored function with the stored value
def callback_RX(data: int):
    for _ in command_codes: 
        if command_codes[_] == data:
            led.toggle()
            FuncToCall = command_codes[_].callback
            ArgToPass = command_codes[_].args
            if ArgToPass is None:
                FuncToCall()
            else:
                FuncToCall(ArgToPass)
            return
    print("Error: "+ hex(data) + "recieved. Unable to match")

IR_Reciever = IR_RX(constants.PIN_RX, constants.ADDRESS, callback_RX)

##### Testing Modes
# Manual = allows for functions to be called from the REPL
# Test = cycles through the command codes with a short delay

MANUAL = False
TESTING = False

async def _testCallBack():
    for _ in command_codes:
        print("Testing Code: ", command_codes[_])
        callback_RX(command_codes[_].code)
        await asyncio.sleep(2)

async def main():
    print("Loading Main...")
    led.value(0) # Turn off led now that everything is loaded
    if MANUAL:
        led3.value(1)   
        print("Starting Manual Control")
        return
    elif TESTING:
        led4.value(1)
        print("Starting Testing")
        await _testCallBack()
    else:
        led2.value(1)
        print("Starting...")
        while True:
            led3.toggle()
            await asyncio.sleep_ms(50)
            turn = distance_sensor.check_distance()
            await TurnMotors(turn)
            pass
asyncio.run(main())