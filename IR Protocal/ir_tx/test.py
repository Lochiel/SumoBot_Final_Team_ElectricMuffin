from nec import NEC
from slam import SLAM
from machine import Pin

# indicator_led = Pin("LED", Pin.OUT)

FREQ_36 = 36_000
FREQ_38 = 38_000 # Default
FREQ_40 = 40_000
FREQ_56 = 56_000

pin = Pin("LED", Pin.OUT)

slam_test = SLAM(pin)
slam_test.tx(0x05,0xF,None)
print(slam_test._arr)

nec_test = NEC(pin)
nec_test.tx(0x05,0xF,None)
print(nec_test._arr)

def TxTimeCalculation(input):
    packet_list = input[1]
    tx_time = 0
    for _ in packet_list:
        tx_time =+ _
    return tx_time