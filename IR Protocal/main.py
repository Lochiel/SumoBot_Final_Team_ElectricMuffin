import ir_tx
from ir_tx.slam import SLAM as tx_SLAM
from ir_rx.slam import SLAM as rx_SLAM
from ir_tx.nec import NEC as tx_NEC
from ir_rx.nec import NEC_ABC as rx_NEC

from machine import Pin
from time import sleep_us, ticks_diff

AUTOMATIC = False
SLAM = True

pin_Tx_test = Pin(6,Pin.IN,Pin.PULL_UP)
txPin = Pin(19, Pin.OUT)
rxPin = Pin(18, Pin.IN)


###RX Functions
def callback(cmd, addr, _):
    print(f"Address: {hex(addr)} Cmd: {hex(cmd)} ")

def calculate_pulsewidths(RxBlock):
    timeBlock = []
    for i in range(0,len(RxBlock)-1):
        timeBlock.append(ticks_diff(RxBlock[i+1],RxBlock[i]))
    return timeBlock

def runTest(data):
    for _ in data:
        if _ > 0:
            RX._cb_pin(0)
            sleep_us(_)
    RX._cb_pin(0)
    print(f"RX: {calculate_pulsewidths(RX._times)}")
    RX.decode(0)

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
    tx_array = tx._arr
    if SLAM:
        print(f"Dot: {tx._DOT}")
        print(f"Dash: {tx._DASH}")
    print(f"Number of on/offs: {len(tx_array)} Time in us: {TxTimeCalculation(tx_array)}")
    print(f"(TX: {tx_array}")

def printSummery_RX(rx):
    print("---RX Summery---")
    if SLAM:
        print(f"Dot: {rx._DOT}")
        print(f"Dash: {rx._DASH}")
        print(f"Threshold: {rx._DASH_Threshold}")
        print(f"RX block Length {rx._txBlock}")


# def trimTrailingZeros(tx_array):
#     for i in range(len(tx_array)-1,0,-1):
#         if tx_array[i] == 0:
#             tx_array.pop(i)
#         else:
#             return tx_array
#     return tx_array




if AUTOMATIC:
    import ir_tx.test
else:
    if SLAM:
        TX = tx_SLAM(txPin)
        RX = rx_SLAM(rxPin, callback)
    else:
        TX = tx_NEC(txPin)
        RX = rx_NEC(rxPin, 0,0, callback)
    print("Running Test")
    print("SLAM test") if SLAM else print("NEC Test")
    TX.tx(0x5,0xF,None)
    printSummery_TX(TX)

    txBlock = TX._arr
    # txBlock = trimTrailingZeros(txBlock)
    printSummery_RX(RX)

    print("-Good Data Test. Expect Address: 0x5, Cmd 0xF")
    runTest(txBlock)