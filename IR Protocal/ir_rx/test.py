from slam import SLAM
from machine import Pin
from time import sleep_us
from print_error import print_error

###RX Functions
def callback(cmd, addr, _):
    print(f"Address: {hex(addr)} Cmd: {hex(cmd)} ")

def calculate_pulsewidths(RxBlock):
    timeBlock = []
    for i in range(0,len(RxBlock)-1):
        timeBlock.append(RxBlock[i+1]-RxBlock[i])
    return timeBlock

def runTest(data, RX):
    i = 1
    RX._times[0] = 0
    for _ in data:
        if _ is not 0:
            RX._times[i] = RX._times[i-1] + _
        i += 1
    # # print(f"RX._times: {RX._times}")
    # print(f"Pulse Widths: {calculate_pulsewidths(RX._times)}")
    RX.decode(0)

def printSummery(rx):
    print("\n---RX Summery---")
    print(f"Dot: {rx._DOT}us")
    print(f"Dash: {rx._DASH}us")
    print(f"Threshold: {rx._DASH_Threshold}us")
    print(f"RX block Length: {rx._txBlock}ms")

###

def main():
    print("Starting RX test...")
    while True:
        sleep_us(1000)

if __name__ == "__main__":
    RxPin = Pin(18, Pin.IN)
    RX = SLAM(RxPin, callback)
    RX.error_function(print_error)
    printSummery(RX)
    main()