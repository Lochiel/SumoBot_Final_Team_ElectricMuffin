# SumoBot Control Main
# Cam Chalmers, Anusha Venka, Melissa Clark
# ECEN 2440 - Applications of Embedded System. Spring '24


import constants
from constants import command_codes
from RX import IR_RX
from machine import Pin
from Motor import Motor
from time import sleep, sleep_ms
import time
import constants
import distance_sensor 
import leds

led = Pin(constants.PIN_LED1, Pin.OUT)
led2 = Pin(constants.PIN_LED2, Pin.OUT)
led3 = Pin(constants.PIN_LED3, Pin.OUT)
led4 = Pin(constants.PIN_LED4, Pin.OUT)

led.value(1) #Turn on board led, it'll be turned off whene everything is loaded... ie very quickly
led2.value(0)
led3.value(0)
led4.value(0)

last_tx_received_time = time.ticks_ms
AUTOSTOP_TIMEOUT = 250 #ms from last tx recieved to initiate autostop
SENSOR_ENABLE = True

# Setup Motor Instances
motor_a = Motor(constants.PIN_MOTOR_A_THROTTLE, constants.PIN_MOTOR_A_GEAR, CWisFwd=False)
motor_b = Motor(constants.PIN_MOTOR_B_THROTTLE, constants.PIN_MOTOR_B_GEAR, CWisFwd=True)

motor_a.stop()
motor_b.stop()

def MotorFWD(speed:int): 
    motor_a.fwd(speed)
    motor_b.fwd(speed)
    print(f"Motor_A: {motor_a} Motor_B: {motor_b}")

def MotorREV(speed:int): 
    motor_a.rev(speed)
    motor_b.rev(speed)
    print(f"Motor_A: {motor_a} Motor_B: {motor_b}")

def MotorCW(speed:int): 
    motor_a.fwd(speed)
    motor_b.rev(speed)
    print(f"Motor_A: {motor_a} Motor_B: {motor_b}")
    pass

def MotorCCW(speed:int): 
    motor_a.rev(speed)
    motor_b.fwd(speed)
    print(f"Motor_A: {motor_a} Motor_B: {motor_b}")
    pass

def MotorSTOP():
    motor_a.stop()
    motor_b.stop()
    # print(f"Motor_A: {motor_a} Motor_B: {motor_b}")

#TODO Call leds mode select function
def NeoPixelMode(mode:int):
    leds.mode(mode)
    print("NeoPixelMode called with value: ", mode)
    pass

def BackSensor_Toggle(): #Placeholder, actual function should be in DistanceSenor.py
    global SENSOR_ENABLE
    SENSOR_ENABLE = False
    print("DistanceSensor_Toggle called")
    pass

def Turn180(): 
    MotorCW(100)
    sleep_ms(200)
    MotorSTOP()
    pass

#TODO Write proper dodge function
def Dodge(direction):
    if (direction == "CW"):
        motor_b.rev(100)
        motor_a.fwd(20)
        pass
    elif (direction == "CCW"):
        motor_a.rev(100)
        motor_b.fwd(20)
        pass
    sleep_ms(750)
    MotorSTOP()

def AutoStopCheck():
    global last_tx_received_time
    if time.ticks_diff(time.ticks_ms(),last_tx_received_time)>AUTOSTOP_TIMEOUT:
        MotorSTOP()
        last_tx_received_time = time.ticks_ms()

def DistanceCheck():
    turn = distance_sensor.check_distance()
    if turn:
        Turn180()


## Set the callback functions for each command code
command_codes["FWD_SLOW"].setCallback(MotorFWD, constants.SLOW)
command_codes["FWD_FAST"].setCallback(MotorFWD, constants.FAST)
command_codes["FWD_TURBO"].setCallback(MotorFWD, constants.TURBO)

command_codes["REV"].setCallback(MotorREV, constants.FAST)

command_codes["CW_SLOW"].setCallback(MotorCW, constants.TURN_SLOW)
command_codes["CW_FAST"].setCallback(MotorCW, constants.TURN_FAST)
command_codes["CW_DODGE"].setCallback(Dodge, "CW")

command_codes["CCW_SLOW"].setCallback(MotorCCW, constants.TURN_SLOW)
command_codes["CCW_FAST"].setCallback(MotorCCW, constants.TURN_FAST)
command_codes["CCW_DODGE"].setCallback(Dodge, "CCW") 

command_codes["STOP"].setCallback(MotorSTOP, None)

command_codes["NP_1"].setCallback(NeoPixelMode, 1)
command_codes["NP_2"].setCallback(NeoPixelMode, 2)
command_codes["NP_3"].setCallback(NeoPixelMode, 3)

command_codes["SEN_BACK"].setCallback(BackSensor_Toggle, None)
command_codes["180"].setCallback(Turn180, None)

## This will compare the recieved data to the codes in command_codes
## If a match is found, it will call the stored function with the stored value
def callback_RX(data: int):
    global last_tx_received_time
    for _ in command_codes: 
        if command_codes[_] == data:
            last_tx_received_time = time.ticks_ms()
            Indicate_Heartbeat()
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

def _testCallBack():
    for _ in command_codes:
        print("Testing Code: ", command_codes[_])
        callback_RX(command_codes[_].code)
        sleep(2)

def main():
    print("Loading Main...")
    led.value(0) # Turn off led now that everything is loaded
    NeoPixelMode(1)
    if MANUAL:
        led3.value(1)   
        print("Starting Manual Control")
        return
    elif TESTING:
        led4.value(1)
        NeoPixelMode(2)
        # print("Starting Testing of commands")
        # _testCallBack()
        print("Starting testing of automatic functions")
        while True:
            time.sleep_ms(1000)
            # if distance_sensor.check_distance():
            #     print("Object in range, turn 180")
            leds.update()
            
    else:
        led2.value(1)
        print("Starting...")
        while True:
            led2.toggle()
            time.sleep_ms(100)
            AutoStopCheck()
            if SENSOR_ENABLE:
                DistanceCheck()
            leds.update()

def Indicate_Heartbeat():
    led.toggle()
    # leds.heartbeat()

main()