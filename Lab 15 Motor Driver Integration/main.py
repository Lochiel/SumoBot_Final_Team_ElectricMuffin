from machine import Pin, PWM
from time import sleep
from ir_rx.nec import NEC_8 
from ir_rx.print_error import print_error  
import IntegratedIRMotors, Motor

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

# Setup Motor Instances
motor_a = Motor(drive_pin=15, gear_pin=14)
motor_b = Motor(drive_pin=20, gear_pin=19)

# IR Receiver Callback Function
def ir_callback(data, addr, _):
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

# Setup the IR receiver
ir_pin = Pin(XXX, Pin.IN, Pin.PULL_UP) ## what pin did we choose?
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
ir_receiver.error_function(print_error)

# Main loop
try:
    while True:
        sleep(1) 
except KeyboardInterrupt:
    print("Stopped by User")
