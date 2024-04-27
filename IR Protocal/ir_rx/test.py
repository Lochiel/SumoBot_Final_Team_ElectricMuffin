from slam import SLAM
from nec import NEC_ABC as NEC
from machine import Pin
from array import array
from time import sleep_us
from utime import ticks_diff
from print_error import print_error

Test_SLAM = True

RxPin = Pin(18, Pin.IN)

def callback(cmd, addr, _):
    print(f"Address: {hex(addr)} Cmd: {hex(cmd)} ")

def runTest(data):
    for _ in data:
        RX._cb_pin(0)
        sleep_us(_)
    RX.decode(0)

if Test_SLAM:
    RX = SLAM(RxPin, callback)
else:
    RX = NEC(RxPin, 0,0, callback)

RX.error_function(print_error)

print("Starting RX test...")
while True:
    sleep_us(500)

# print("Good Data Test. Expect Address: 0x5, Cmd 0xF")
# runTest(DataStream)

# print("Bad Data: Missing end")
# BadDataStream=DataStream[:]
# BadDataStream.append(100)
# runTest(BadDataStream)

# print("Bad Data: Flipped Bit")
# BadDataStream=DataStream[:]
# BadDataStream[5] = 1687
# runTest(BadDataStream)


# # print(f"Array of edge times: {slam_test._times}")
# # print(f"Number of edges: {slam_test.edge}")
# # print(f"Size of start block: {ticks_diff(slam_test._times[2],slam_test._times[1])}")
