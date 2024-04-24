from slam import SLAM
from machine import Pin
from array import array
from time import sleep_us
from utime import ticks_diff
from print_error import print_error

pin = Pin(18, Pin.IN)

#Address: 0x5, Command: 0xF
#Edges: 36
DataStream = array('i', [4500, 2500, 394, 1182, 394, 394, 394, 1182, 394, 394, 394, 394, 394, 1182, 394, 394, 394, 1182, 394, 1182, 394, 1182, 394, 1182, 394, 1182, 394, 394, 394, 394, 394, 394, 394, 394, 394, 0])

def callback(cmd, addr, _):
    print(f"Address: {hex(addr)} Cmd: {hex(cmd)} ")

def runTest(data):
    for _ in data:
        slam_test._cb_pin(0)
        sleep_us(_)
    slam_test.decode(0)

slam_test = SLAM(pin, callback)
slam_test.error_function(print_error)

# while True:
#     sleep_us(500)

print("Good Data Test. Expect Address: 0x5, Cmd 0xF")
runTest(DataStream)

print("Bad Data: Missing end")
BadDataStream=DataStream[:]
BadDataStream.append(100)
runTest(BadDataStream)

print("Bad Data: Flipped Bit")
BadDataStream=DataStream[:]
BadDataStream[5] = 1687
runTest(BadDataStream)


# # print(f"Array of edge times: {slam_test._times}")
# # print(f"Number of edges: {slam_test.edge}")
# # print(f"Size of start block: {ticks_diff(slam_test._times[2],slam_test._times[1])}")
