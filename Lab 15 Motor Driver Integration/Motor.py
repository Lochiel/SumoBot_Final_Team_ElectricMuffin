## Motor Setup ##
from machine import PWM, Pin
from time import sleep_ms


class Motor:

    __DrivePin: PWM
    __GearPin: Pin
    __gear: None | bool

    #Pin.value(x) evaluates x for truthiness. True sets Pin High. False sets Pin Low
    # Change this value based on the side the motor is on
    FWD = True
    REV = not FWD

    PWM_MAX = 65535
    PWM_MIN = 0

    _DelayToStop = 500; #When commanded to stop, how many miliseconds will we wait for the motor to spin down? 

    def __init__(self, DrivePin: int | str, GearPin: int| str) -> None:
        self.__DrivePin = PWM(Pin(DrivePin), freq=2000)
        self.__GearPin = Pin(GearPin, Pin.OUT, value=self.FWD)
        self.__gear = self.FWD
        pass

    def fwd(self, speed):
         GearRtrn = self.gear(self.FWD)
         SpeedRtrn = self.speed(speed)
         return {GearRtrn, SpeedRtrn}
        
    def rev(self, speed):
         GearRtrn = self.gear(self.REV)
         rtrnValue = self.speed(speed)
         return {GearRtrn, SpeedRtrn}

    def gear(self, gear=None):
            if (type(gear) is bool) & (gear != self.__gear):
                self.stop()
                self.__GearPin.value(gear)
                self.__gear = gear
            return self.__gear
    
    def speed(self, speed=None) -> int:
        if type(speed) == int:
            speed_value = int( (speed/100) * self.PWM_MAX ) ## speed is a percentage; get the absolute value in terms of PWM duty cycle
            self.__DrivePin.duty_u16(speed_value)
        return self.__DrivePin.duty_u16()

    def stop(self):
        self.__DrivePin.duty_u16(self.PWM_MIN)
        sleep_ms(self._DelayToStop)