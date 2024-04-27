# Decoder for IR transmission of SumoBots
# Written by Cam Chalmers
# For ECEN 2440 - Applications of Embedded Systems, Spring '24
# Modified NEC code
# Based on code by Peter Hinch

#DONE Remove non-SLAM handling; Samsung, NEC-8 etc.
#DONE Reduce data and address size from 8 to 4 bits
#DONE Reduce burst length
#DONE Make burst time based on tx frequency, so that higher frequencies reduce tx time
#DONE Reduce Start block size 
# First and second burst are both one DASH in length. A properly coded transmission will not have any other sequential DASH'es
#TODO Evaluate possibility of a second, delayed transmission. This is to give a 2nd chance at capturing a corrupted transmission

from utime import ticks_us, ticks_diff
from ir_rx import IR_RX

class SLAM(IR_RX):
    
    _DASH_Ratio = 2 #Number of times we multiply _DOT to get the length of _DASH
    _CYCLES_PER_DOT = 10 #Number of IR cycles in a DOT. Determined by the IR Reciever, check the datasheet for information

    #NOTE In nec.py, StartBlock times are 9ms on then 4.5ms off
    # However, the default wait times in ir_rx/nec.py are 4ms and 3ms
    def __init__(self, pin, callback, freq=38_000, *args):
        self._edges = 36 #Number of expected edges
        self._setBurstLength(freq)
        self._setDASH_Threshold()
        self._setStartBlock()
        self._txBlock = self._calculate_txBlock() #Number of ms to wait for a full tx. 
        super().__init__(pin, self._edges, self._txBlock, callback, *args)
        self._addr = 0

    def _setBurstLength(self, freq):
        """Set's the length of the bursts based on the tx frequency"""
        cycles_per_us = freq/(1_000_000)
        period = 1/cycles_per_us
        burst_cycles = self._CYCLES_PER_DOT
        self._DOT = int(burst_cycles * period)
        self._DASH = int(self._DASH_Ratio * self._DOT)

    def _setStartBlock(self):
        self.StartBlock_leader = self._DASH_Threshold # Length of Start Block
        self.StartBlock_follower = self._DASH_Threshold

    def _calculate_txBlock(self):
        """Returns the expected txBlock size, based on the freq and data size"""
        #From the freq we get TBURST
        #The tx block has 2 edges for each bit, so we use _edges to find the data size of the block
        # Each bit is proceded by a TBURST, then a pause w/ length based on the value of the bit
        # 0b0 = 1 TBURST + 1 TBURST
        # 0b1 = 1 TBURST + n * TBURST, where n is the size ratio
        # Due to error correction, each tx block is half 1's and half 0's
        # thus, tx block length = bits/2 * (2 TBURST) + bits/2 * (1 TBURST = n * TBURST)
        bits = self._edges/2
        zero_length = (bits * self._DOT)
        ones_length = (bits/2 * (self._DOT + self._DASH_Ratio*self._DOT))
        data_length = zero_length + ones_length
        #Include header information.
        #TODO Update the header information when we have nailed that down
        txBlock_us = data_length + self.StartBlock_leader*2 + self.StartBlock_follower*2
        txBlock_ms = int(txBlock_us / 1000) # convert us to ms
        return txBlock_ms

    def _setDASH_Threshold(self):
        # This value will be the threshold that determines a bit in the datastream is a zero or one
        # A bit larger than the threshold is a 1
        # We don't want this to be explicitly TBURST or T_ONE, as physical realities of circuits and tranmissions may distort the times
        self._DASH_Threshold = int(self._DOT + (self._DASH - self._DOT)/2)

    def decode(self, _):
        try:
            if self.edge > self._edges:
                print(f"Too many edges: {self.edge}")
                raise RuntimeError(self.OVERRUN)
            width = ticks_diff(self._times[1], self._times[0])
            if width < self.StartBlock_leader:  # 2.5ms leading mark for all valid data
                print(f"Bad StartBlock Leader. Expected: {self.StartBlock_leader} Got: {width}")
                raise RuntimeError(self.BADSTART)
            width = ticks_diff(self._times[2], self._times[1])
            if width > self.StartBlock_follower:  # 4.5ms space for normal data
                if self.edge < self._edges:  # Haven't received the correct number of edges
                    raise RuntimeError(self.BADBLOCK)
                # Time spaces only (marks are always 562.5µs)
                # Space is 1.6875ms (1) or 562.5µs (0)
                # Skip last bit which is always 1
                val = 0
                for edge in range(3, self._edges - 2, 2):
                    val >>= 1
                    if ticks_diff(self._times[edge + 1], self._times[edge]) > self._DASH_Threshold:
                        val |= 0x8000  #make val the size of data transmission; each '0' is 4 bits
            else:
                print(f"Bad StartBlock Follower. Expected: {self.StartBlock_follower} Got: {width}")
                raise RuntimeError(self.BADSTART)
            
            addr = val & 0xf  # 4 bit addr
            if addr != ((val >> 4) ^ 0xf) & 0xf:  # 4 bit addr doesn't match check
                raise RuntimeError(self.BADADDR)
            self._addr = addr

            cmd = (val >> 8) & 0xf
            if cmd != (val >> 12) ^ 0xf:
                raise RuntimeError(self.BADDATA)

        except RuntimeError as e:
            cmd = e.args[0]
            addr =  0
        # Set up for new data burst and run user callback
        self.do_callback(cmd, addr, 0)