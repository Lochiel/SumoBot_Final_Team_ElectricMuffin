import ir_tx
from ir_tx.slam import SLAM as tx_SLAM
from ir_rx.slam import SLAM as rx_SLAM
from ir_tx.nec import NEC as tx_NEC
from ir_rx.nec import NEC_ABC as rx_NEC

from machine import Pin
from time import sleep, sleep_us, ticks_diff

AUTOMATIC_TX = False
AUTOMATIC_RX = True
SLAM = True

pin_Tx_test = Pin(6,Pin.IN,Pin.PULL_UP)
txPin = Pin(19, Pin.OUT)
rxPin = Pin(18, Pin.IN)

def CheckArray(arr):
    total = 0
    for _ in arr:
        total += int(_)
    return total
    
###TX Functions
def Tx_test_pin():
    return pin_Tx_test.value()

def TxTimeCalculation(input):
    packet_list = input
    tx_time = 0
    for _ in packet_list:
        tx_time += _
    return tx_time

def printSummery_TX(tx):
    print("---TX Summery---")
    if SLAM:
        print(f"Dot: {tx._DOT}")
        print(f"Dash: {tx._DASH}")
    else:
        print(f"DOT/DASH length not available. NEC Defaults: 563, 1687")
    if CheckArray(tx._arr) > 0:
        tx_array = tx._arr
        print(f"Number of on/offs: {len(tx_array)} Time in us: {TxTimeCalculation(tx_array)}")
        print(f"(TX: {tx_array}")

###RX Functions
def callback(cmd, addr, _):
    print(f"Address: {hex(addr)} Cmd: {hex(cmd)} ")

def calculate_pulsewidths(RxBlock):
    timeBlock = []
    for i in range(0,len(RxBlock)-1):
        timeBlock.append(ticks_diff(RxBlock[i+1],RxBlock[i]))
    return timeBlock

def runTest(data):
    # for _ in data:
    #     if _ > 0:
    #         RX._cb_pin(0)
    #         sleep_us(_)
    i = 0
    for _ in data:
        if i==0:
            RX._times[0] = _
        else:
            RX._times[i] = RX._times[i-1] + _
        print(f"{_}", end = " ")
        i += 1
    RX._cb_pin(0)
    print(f"RX: {calculate_pulsewidths(RX._times)}")
    RX.decode(0)

def printSummery_RX(rx):
    print("---RX Summery---")
    if SLAM:
        print(f"Dot: {rx._DOT}")
        print(f"Dash: {rx._DASH}")
        print(f"Threshold: {rx._DASH_Threshold}")
        print(f"RX block Length {rx._txBlock}")

###

if AUTOMATIC_TX:
    import ir_tx.test
else:
    if SLAM:
        TX = tx_SLAM(txPin)
        RX = rx_SLAM(rxPin, callback)
    else:
        TX = tx_NEC(txPin)
        RX = rx_NEC(rxPin, 0,0, callback)
    print("SLAM test") if SLAM else print("NEC Test")

if AUTOMATIC_RX:
    printSummery_TX(TX)
    printSummery_RX(RX)
    print("--RX Test, waiting for signal--")
    while True:
        sleep(0.1)
else:
    print("Running Software Test")
    
    TX.tx(0x5,0xF,None)
    printSummery_TX(TX)
    printSummery_RX(RX)


    txBlock = TX._arr
    print("-Good Data Test. Expect Address: 0x5, Cmd 0xF")
    runTest(txBlock)