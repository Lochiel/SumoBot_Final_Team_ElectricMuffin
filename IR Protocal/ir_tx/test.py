from slam import SLAM
from nec import NEC
from machine import Pin

# indicator_led = Pin("LED", Pin.OUT)

FREQ_36 = 36_000
FREQ_38 = 38_000 # Default
FREQ_40 = 40_000
FREQ_56 = 56_000

pin = Pin("LED", Pin.OUT)

def TxTimeCalculation(input):
    packet_list = input
    tx_time = 0
    for _ in packet_list:
        tx_time += _
    return tx_time

def printSummery(tx_string):
    tx_string = tx_string._arr
    print(f"Number of on/offs: {len(tx_string)} Time in us: {TxTimeCalculation(tx_string)}")
    print(f"(TX: {tx_string}")

slam_test = SLAM(pin)
slam_test.tx(0x5,0xF,None)
printSummery(slam_test)

nec_test = NEC(pin)
nec_test.tx(0x05,0x0F,None)
printSummery(nec_test)