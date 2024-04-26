# SumoBot Little Asynchronous Messaging - SLAM 
# Encoder for IR transmission of SumoBots
# Written by Cam Chalmers
# For ECEN 2440 - Applications of Embedded Systems, Spring '24
# Modified NEC code
# Based on code by Peter Hinch

#DONE Reduce data and address size from 8 to 4 bits
#TODO Reduce burst length - Need Real world testing
#TODO Reduce long/short space ratio - Code changes implemented, ready to deploy
#DONE Make burst time based on tx frequency, so that higher frequencies reduce tx time
#TODO Reduce Start block size 
#TODO Evaluate possibility of a second, delayed transmission. This is to give a 2nd chance at capturing a corrupted transmission

from ir_tx import IR, STOP

class SLAM(IR):
    valid = (0xf, 0xf, 0)  # Max addr, data, toggle

    _DOT = 563 #Default values, will be set late
    _DASH = 1687

    _DASH_Ratio = 2 #Number of times we multiply _TBURST to get the length of _T_ONE


    #DONE change asize argument passed to super().__init__() to new size
    # asize = on/off times (μs)
    # 2 on/off times per bit. 
    # NEC asize is 68 for 32 bits of data + start and end blocks
    # 8*4 + 2 = 34 bits

    # SLAM has 4 bit addr and data sizes. Additional 4 bits each of error detection, and Start and End bloc
    # 4*4 + 2 = 18 bits
    # SLAM asize = 36

    def __init__(self, pin, freq=38_000, verbose=False):  # 38kHz is the standard frequency
        self._setBurstLength(freq)
        super().__init__(pin, freq, 36, 33, verbose)  # Measured duty ratio 33% 

    def _bit(self, b):
        self.append(self._DOT, self._DASH if b else self._DOT) # If bit =1, long space, else short space

    def _setBurstLength(self, freq):
        """Set's the length of the bursts based on the tx frequency"""
        cycles_per_us = freq/(1_000_000)
        period = 1/cycles_per_us
        burst_cycles = 15 #Number of cycles in a burst
        self._DOT = int(burst_cycles * period)
        self._DASH = int(self._DASH_Ratio * self._DOT)

        self.StartBlock_leader = self._DASH
        self.StartBlock_follower = self._DASH
    
    #NOTE In nec.py, StartBlock times are 9ms on then 4.5ms off
    # However, the default wait times in ir_rx/nec.py are 4ms and 3ms

    def tx(self, addr, data, _):  # Ignore toggle
        self.append(self.StartBlock_leader, self.StartBlock_follower) #Start Block TODO
        addr |= ((addr ^ 0xf) << 4)
        for _ in range(8):
            self._bit(addr & 1)
            addr >>= 1
        data |= ((data ^ 0xf) << 4)
        for _ in range(8):
            self._bit(data & 1)
            data >>= 1
        self.append(self._DOT)
