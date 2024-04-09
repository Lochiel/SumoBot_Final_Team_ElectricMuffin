from collections.abc import Callable

PIN_LED1 = "LED"
PIN_LED2 = 3
PIN_LED3 = 4
PIN_LED4 = 5

PIN_RX = 18

PIN_MOTOR_A_GEAR = 12 #Labelled AIN1 on PCB
PIN_MOTOR_A_THROTTLE = 13 #Labelled AIN2 on PCB

PIN_MOTOR_B_GEAR = 14 #Labelled BIN1 on PCB
PIN_MOTOR_B_THROTTLE = 15 #Labelled BIN2 on PCB

PIN_NEOPIXEL1 = 6
PIN_NEOPIXEL2 = 7

PIN_SENSOR_TRIGGER = 21
PIN_SENSOR_RETURN = 20

ADDRESS = 0x5

class Commands():
    code: int
    description: str
    callback: Callable
    args: None|int

    def __init__(self, code: int, description: str) -> None:
        self.code = code
        self.description = description

    def __str__(self) -> str:
        return hex(self.code)+": "+self.description
    
    def __eq__(self, __value: object) -> bool:
        return __value == self.code
    
    def setCallback(self, callback, value: None|int):
        self.callback = callback
        self.args=value

command_codes = {
    "FWD_SLOW": Commands(0x0, "Forward, Slow"),
    "FWD_FAST": Commands(0x1, "Forward, Fast"),
    "FWD_TURBO": Commands(0x2, "Forward, Turbo"),
    "REV": Commands(0x3, "Reverse"),
    "CW_SLOW": Commands(0x4, "Rotate Clockwise, Slow"),
    "CW_FAST": Commands(0x5, "Rotate Clockwise, Fast"),
    "CCW_SLOW": Commands(0x6, "Rotate CounterClockwise, Slow"),
    "CCW_FAST": Commands(0x7, "Rotate CounterClockwise, Fast"),
    "NP_1": Commands(0x8, "NeoPixel Mode 1"),
    "NP_2": Commands(0x9, "NeoPixel Mode 2"),
    "NP_3": Commands(0xA, "NeoPixel Mode 3"),
    "SEN_BACK": Commands(0xB, "Back Sensor Toggle"),

    "STOP": Commands(0xF, "Stop Motors")
}