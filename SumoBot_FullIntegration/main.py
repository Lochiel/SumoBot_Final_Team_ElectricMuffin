## Psuedo Code

## Goals
## Have basic control code setup 

## TODO
## 1) seperate Main.py, Motors.py, and RX.py, etc into seperate modules
## 2) Break out repeating code into functions
## 3) Set up interrupts/callback sequences


## Interrupt based main.py
#
__init__():
    Init BackSensor(Pin, Distance, CheckDelay, MotorSpin_callbackFunction)
    Init RX(Pin, FREQ, Address, RX_CallbackFunction)
    Init Motors(MotorA pin1, MotorA pin2, MotorB pin1, MotorB pin2, MotorA_SpinDirection, MotorB_SpinDirection)
    Init NeoPixels(Pin1, Pin2)

callback_RX(Data)
    Check Data
    Execute Command

callback_BackSensor(None)
    Check Distance
    Command Rotation
