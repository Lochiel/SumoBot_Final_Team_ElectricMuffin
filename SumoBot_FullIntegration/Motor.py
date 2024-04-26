## Motor Setup ##
from machine import PWM, Pin
from time import sleep_ms


class Motor:

    _DrivePin: PWM
    _GearPin: Pin
    _gear: None | bool


    PWM_MAX = 65535
    PWM_MIN = 0
    pwm_custom = int(PWM_MAX / 2)

    _DelayToStop = 0; #When commanded to stop, how many miliseconds will we wait for the motor to spin down? 

    def __init__(self, DrivePin: int | str, GearPin: int| str, CWisFwd=True) -> None:
        self.FWD = CWisFwd
        self.REV = not CWisFwd
        self._DrivePin = PWM(Pin(DrivePin), freq=2000)
        self._GearPin = Pin(GearPin, Pin.OUT, value=self.FWD)
        self._gear = self.FWD

    def fwd(self, speed):
         GearRtrn = self.gear(self.FWD)
         self.StartPulse()
         SpeedRtrn = self.speed(speed)
         return {GearRtrn, SpeedRtrn}
        
    def rev(self, speed):
         GearRtrn = self.gear(self.REV)
         SpeedRtrn = self.speed(speed)
         return {GearRtrn, SpeedRtrn} ## changed SpeedRtrn to rtrnValue to be in scope

    def gear(self, gear=None):
            if (type(gear) is bool) & (gear != self._gear):
                self.stop()
                self._GearPin.value(gear)
                self._gear = gear
            return self._gear
    
    def speed(self, speed=None) -> int:
        if type(speed) == int:
            speed_value = int( (speed/100) * self.PWM_MAX ) ## speed is a percentage; get the absolute value in terms of PWM duty cycle
            self._DrivePin.duty_u16(speed_value)
        return self._DrivePin.duty_u16()

    def stop(self):
        self._DrivePin.duty_u16(self.PWM_MIN)
        sleep_ms(self._DelayToStop)
    
    def StartPulse(self):
        if self._DrivePin.duty_u16() == 0:
            self.speed(100)
            sleep_ms(1)
        
    def status(self):
        return {self._gear,self._DrivePin.duty_u16()}
    
    def __str__(self) -> str:
        if (self._gear == self.FWD):
            gear = "Forward"
        elif (self._gear == self.REV):
            gear = "Reverse"
        else:
            gear = "ERROR"
        throttle = round(100 * self._DrivePin.duty_u16() / self.PWM_MAX)
        return str(gear) + " at " + str(throttle) + "%"