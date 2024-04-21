from slam import SLAM
from nec import NEC
from machine import Pin
from time import sleep

# indicator_led = Pin("LED", Pin.OUT)

FREQ_36 = 36_000
FREQ_38 = 38_000 # Default
FREQ_40 = 40_000
FREQ_56 = 56_000

pin = Pin("LED", Pin.OUT)
pin_Tx_test = Pin(6,Pin.IN,Pin.PULL_UP)

def Tx_test_pin():
    return not( pin_Tx_test.value())

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


while True:
    if not Tx_test_pin():
        sleep(0.1)
    for addr in range(0,0xF,):
        if not Tx_test_pin():
            break
        for data in range(0,0xF):
            print(f"Tx addr: {addr} data: {data}")
            slam_test.transmit(addr,data)
            sleep(0.1)
            if not Tx_test_pin():
                print("Stopping due to input")
                break