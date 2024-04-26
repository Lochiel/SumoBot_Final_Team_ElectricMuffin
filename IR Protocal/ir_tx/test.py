from slam import SLAM
from machine import Pin
from time import sleep
from nec import NEC

test_SLAM = True

# indicator_led = Pin("LED", Pin.OUT)

FREQ_36 = 36_000
FREQ_38 = 38_000 # Default
FREQ_40 = 40_000
FREQ_56 = 56_000

led = Pin("LED", Pin.OUT)
pin = Pin(19, Pin.OUT)
pin_Tx_test = Pin(6,Pin.IN,Pin.PULL_UP)

def Tx_test_pin():
    return pin_Tx_test.value()

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

if test_SLAM:
    Tx_test = SLAM(pin)
    print(f"Dot: {Tx_test._DOT}")
    print(f"Dash: {Tx_test._DASH}")
else:
    Tx_test = NEC(pin)

Tx_test.tx(0x5,0xF,None)
printSummery(Tx_test)

while True:
    if Tx_test_pin():
        sleep(0.1)
    for addr in range(0,0xF,):
        if Tx_test_pin():
            break
        for data in range(0,0xF):
            print(f"Tx addr: {addr} data: {data}")
            Tx_test.transmit(addr,data)
            led.toggle()
            sleep(0.1)
            if Tx_test_pin():
                print("Stopping due to input")
                break