## Psuedo Code

## Goals
## Have basic control code setup 

## TODO seperate Main.py, Motors.py, and RX.py, etc into seperate modules
## TODO Break out repeating code into functions
## TODO Set up interrupts/callback sequences

#TODO Write Back Sensor Handling


## Interrupt based main.py

import constants
from constants import command_codes
from RX import IR_RX

#TODO Replace placeholders with functions in respective modules
def MotorFWD(speed:int): #Placeholder, actual function should be in Motors.py
    pass

def MotorREV(): #Placeholder, actual function should be in Motors.py
    pass

def MotorCW(speed:int): #Placeholder, actual function should be in Motors.py
    pass

def MotorCCW(speed:int): #Placeholder, actual function should be in Motors.py
    pass

def NeoPixelMode(mode:int): #Placeholder, actual function should be in SumoNeoPixels.py
    pass

def BackSensor_Toggle(): #Placeholder, actual function should be in DistanceSenor.py
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
            FuncToCall(ArgToPass)
            return
    print("Error: "+ hex(data) + "recieved. Unable to match")

#TODO setup Initalizations
IR_Reciever = IR_RX(constants.PIN_RX, constants.ADDRESS, callback_RX)

#     Init BackSensor(Pin, Distance, CheckDelay, MotorSpin_callbackFunction)

#     Init Motors(MotorA pin1, MotorA pin2, MotorB pin1, MotorB pin2, MotorA_SpinDirection, MotorB_SpinDirection)
#     Init NeoPixels(Pin1, Pin2)