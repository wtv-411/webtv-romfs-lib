import ctypes
from enum import Enum
import traceback
import time
#from cool import *

class LZJ_VERSION(Enum):
    VERSION0 = 0x6C7A6A30 # lzj0
    VERSION1 = 0x6C7A6A31 # lzj1
    VERSION2 = 0x6C7A6A32 # lzj2

class lzj():
    def __init__(self, version: LZJ_VERSION = LZJ_VERSION.VERSION1):
        self.clear(version)

    def clear(self, version: LZJ_VERSION = LZJ_VERSION.VERSION1):
        self.BLOCK_SIZE = 0x100
        self.MAX_MATCH_LENGTH = 0x05
        self.MIN_MATCH_LENGTH = 0x02
        self.MATCH_START_OFFSET = 0x06
        self.MAX_LENGTH = 0x100 + 0x08

        self.version = version

        self.uncompressed_data = bytearray()
        self.uncompressed_length = 0x00
        self.uncompressed_index = 0x00

        self.compressed_data = bytearray()
        self.compressed_length = 0x00
        self.compressed_index = 0x00
        self.block_uncompressed_byte_length = 0x00

        self.pending_bytes = bytearray()

        self.flag = 0x00
        self.flag_bit_index = 0
        self.flagged_length = -1

        self.next_block_position = -1

        self.prev_block_compressed_index = 0x00
        self.prev_block_uncompressed_index = 0x00
        self.prev_block_flag_bit_index = 0
        self.prev_block_flag = 0x00
        self.prev_block_pending_bytes = bytearray()

        self.match_block_index_length = 0
        self.match_block_position = 0
        self.match_length = 0x00
        self.match_position = 0x00

        self.cool = 0

    def IsGoodMatch(self, position_difference, matched_length):
        if matched_length == 0x02 and position_difference <= 0x100:
            return True
        elif  matched_length == 0x03 and position_difference <= 0x1100:
            return True
        elif  matched_length == 0x04 and position_difference <= 0x111000:
            return True
        elif  matched_length > 0x04 and position_difference <= 0x911000:
            return True
        else:
            return False

    def MixingModel1(self, encode, end):
        Sdictionary = {}
        Edictionary = {}

        search_index = 0
        while search_index < self.uncompressed_length:
            self.match_position = -1
            self.match_length = 1
            matched_S = b''

            current_match_length = self.MAX_MATCH_LENGTH
            while current_match_length >= self.MIN_MATCH_LENGTH:
                uncompressed_end_index = search_index + current_match_length
                if uncompressed_end_index < self.uncompressed_length:
                    S = bytes(self.uncompressed_data[search_index:uncompressed_end_index])

                    if uncompressed_end_index >= self.MATCH_START_OFFSET and self.match_position == -1:
                        if S in Sdictionary:
                            position_difference = self.uncompressed_index - Sdictionary[S]
                            if Sdictionary[S] < self.uncompressed_index and self.IsGoodMatch(position_difference, current_match_length):
                                self.match_position = Sdictionary[S]
                                self.match_length = current_match_length
                                matched_S = S

                    Sdictionary[S] = search_index
                    if True and current_match_length == self.MAX_MATCH_LENGTH and self.MAX_MATCH_LENGTH < self.MAX_LENGTH:
                        if S in Edictionary:
                            Edictionary[S].append(search_index)
                        else:
                            Edictionary[S] = [search_index]

                current_match_length -= 1

            if search_index >= self.uncompressed_index:
                if self.match_length >= self.MAX_MATCH_LENGTH:
                    iii = self.match_length
                    while self.match_length < self.MAX_LENGTH and (search_index + iii) < self.uncompressed_length:
                        if self.uncompressed_data[search_index + iii] == self.uncompressed_data[self.match_position + iii]:
                            self.match_length += 1
                        else:
                            found_new_match = False
                            if True:
                                for _index in Edictionary[matched_S][0:-1]:
                                    if self.uncompressed_data[search_index:search_index + self.match_length + 1] == self.uncompressed_data[_index:_index + self.match_length + 1]:
                                        self.match_position = _index
                                        self.match_length += 1
                                        found_new_match = True
                                        break

                            if not found_new_match:
                                break
                        
                        iii += 1
                
                    if self.match_length == 0x09:
                        self.match_length = 0x08

                if search_index == 0x17003:
                    #print("self.match_length", hex(self.match_length), hex(search_index), Edictionary[matched_S])
                    #quit()
                    pass

                encode(search_index)

            search_index += 1

        end()

    def MixingModel2(self, encode, end):
        Sdictionary = {}
        Edictionary = {}
        cool_index = 0

        saved = 0
        maxdif = 0
        avgdif = 0
        difcnt = 0

        search_index = 0
        while search_index < self.uncompressed_length:
            self.match_position = -1
            self.match_length = 1
            matched_S = b''

            current_match_length = self.MAX_MATCH_LENGTH
            while current_match_length >= self.MIN_MATCH_LENGTH:
                uncompressed_end_index = search_index + current_match_length
                if uncompressed_end_index < self.uncompressed_length:
                    S = bytes(self.uncompressed_data[search_index:uncompressed_end_index])

                    if uncompressed_end_index >= self.MATCH_START_OFFSET and self.match_position == -1:
                        if S in Sdictionary:
                            position_difference = search_index - Sdictionary[S]
                            if Sdictionary[S] < search_index and self.IsGoodMatch(position_difference, current_match_length):
                                self.match_position = Sdictionary[S]
                                self.match_length = current_match_length
                                matched_S = S

                    Sdictionary[S] = search_index
                    if current_match_length == self.MAX_MATCH_LENGTH and self.MAX_MATCH_LENGTH < self.MAX_LENGTH:
                        if S in Edictionary:
                            Edictionary[S].append(search_index)
                        else:
                            Edictionary[S] = [search_index]


                current_match_length -= 1

            cool_position = cool[cool_index][0]

            if search_index == cool_position:
                if self.match_length >= self.MAX_MATCH_LENGTH:
                    iii = self.match_length
                    while self.match_length < self.MAX_LENGTH and (search_index + iii) < self.uncompressed_length:
                        if self.uncompressed_data[search_index + iii] == self.uncompressed_data[self.match_position + iii]:
                            self.match_length += 1
                        else:
                            found_new_match = False
                            for _index in Edictionary[matched_S][0:-1]:
                                if self.uncompressed_data[search_index:search_index + self.match_length + 1] == self.uncompressed_data[_index:_index + self.match_length + 1]:
                                    self.match_position = _index
                                    self.match_length += 1
                                    found_new_match = True
                                    break

                            if not found_new_match:
                                break
                        
                        iii += 1

                if self.match_length < cool[cool_index][2]:
                    dif = cool[cool_index][2] - self.match_length

                    print(hex(search_index), hex(self.match_length), hex(dif), hex(self.match_position), hex(search_index - cool[cool_index][1]), Edictionary[matched_S])
                    quit()

                    avgdif *= difcnt
                    avgdif += dif

                    difcnt += 1

                    avgdif /= difcnt
                    #print(hex(dif), self.uncompressed_data[cool[cool_index][1]:cool[cool_index][1]+cool[cool_index][2]])

                cool_index += 1
                if cool_index >= len(cool):
                    break

            search_index += 1

        print("avgdif", avgdif)


    def MixingModel4(self, encode, end):
        while self.uncompressed_index < self.uncompressed_length:
            self.match_position = -1
            self.match_length = 1

            if self.uncompressed_index >= 0x1652B4:
                #print("c", hex(cool[self.cool][0]), "cml", hex(cool[self.cool][2]), "ui", hex(self.uncompressed_index), "ci", hex(self.compressed_index))
                pass

            if self.uncompressed_index == cool[self.cool][0]:
                self.match_length = cool[self.cool][2]
                self.match_position = self.uncompressed_index - cool[self.cool][1]
                self.cool += 1

                if self.uncompressed_data[self.match_position + self.match_length] == self.uncompressed_data[self.uncompressed_index + self.match_length]:
                    print("IT CAN GO BIGGER!", hex(self.uncompressed_index), hex(self.match_position), hex(self.match_length))

                #if self.compressed_index > 0x8FF60 and self.match_position >= 0:
                #    print(hex(self.uncompressed_index), hex(self.compressed_index), hex(self.match_position), hex(self.match_length))

            if not encode(self.uncompressed_index) and self.match_position > 0:
                self.cool -= 1
        end()

    def AddPendingByte(self, byte):
        self.block_uncompressed_byte_length += 1
        self.pending_bytes.append(byte)

    def PushPendingBytes(self, length = -1):
        if length == -1:
            self.compressed_data.extend(self.pending_bytes)
            self.compressed_index += len(self.pending_bytes)
            self.pending_bytes.clear()
        elif length > 0:
            self.compressed_data.extend(self.pending_bytes[0:length])
            self.compressed_index += length
            self.pending_bytes = self.pending_bytes[length:]

    def PushFlag(self):
        self.compressed_data.append(self.flag & 0xFF)
        self.compressed_index += 1

        self.flag_bit_index = 0
        self.flag = 0x00

    def WriteReversedFlagBit(self, value, bits = 1, for_pending_bytes = False):
        reversed_value = 0

        i = 0
        while i < bits:
            reversed_value = (reversed_value << 1) + (value & 1)
            value >>= 1
            i += 1

        return self.WriteFlagBit(reversed_value, bits, for_pending_bytes)

    def WriteFlagBit(self, value, bits = 1, for_pending_bytes = False):
        prev_flag_bit_index = self.flag_bit_index

        self.flag |= (value << self.flag_bit_index)
        self.flag_bit_index += bits

        if self.flag_bit_index >= 8:
            new_flag = self.flag
            new_flag_bit_index = self.flag_bit_index

            self.PushFlag()

            if new_flag_bit_index > 8:
                new_flag >>= 8
                new_flag_bit_index -= 8

                if for_pending_bytes:
                    self.PushPendingBytes(min(8, 8 - prev_flag_bit_index))
                else:
                    self.PushPendingBytes()

                if self.flagged_length >= 0:
                    self.compressed_data.append(self.flagged_length & 0xFF)
                    self.compressed_index += 1
                    self.flagged_length = -1

                self.WriteFlagBit(new_flag, new_flag_bit_index, for_pending_bytes)
            else:
                self.PushPendingBytes()

                if self.flagged_length >= 0:
                    self.compressed_data.append(self.flagged_length & 0xFF)
                    self.compressed_index += 1
                    self.flagged_length = -1

    def RestoreState(self):
        self.flag_bit_index = self.prev_block_flag_bit_index
        self.flag = self.prev_block_flag & ((2 ** self.flag_bit_index) - 1)
        
        self.pending_bytes = self.prev_block_pending_bytes
        self.compressed_data = self.compressed_data[0:self.prev_block_compressed_index]
        self.compressed_index = self.prev_block_compressed_index

        self.uncompressed_index = self.prev_block_uncompressed_index

    def SaveState(self):
        self.prev_block_uncompressed_index = self.uncompressed_index
        self.prev_block_compressed_index = self.compressed_index
        self.prev_block_flag_bit_index = self.flag_bit_index
        self.prev_block_flag = self.flag

        self.prev_block_pending_bytes = bytearray(self.pending_bytes)

    def CheckBlockMark(self):
        can_continue = True

        if self.uncompressed_index >= self.next_block_position:
            flag_bit = 0
            advanced_uncompressed_index = 0
            if self.block_uncompressed_byte_length >= self.BLOCK_SIZE:
                self.RestoreState()
                
                advanced_uncompressed_index = self.BLOCK_SIZE
                self.pending_bytes.extend(self.uncompressed_data[self.uncompressed_index:(self.uncompressed_index + advanced_uncompressed_index)])
                flag_bit = 1
                can_continue = False
            else:
                advanced_uncompressed_index = 0
                flag_bit = 0
                can_continue = True
            
            self.SaveState()
            self.next_block_position = self.uncompressed_index + self.BLOCK_SIZE
            self.block_uncompressed_byte_length = 0
            self.WriteFlagBit(flag_bit)

            self.uncompressed_index += advanced_uncompressed_index

        return can_continue

    def Encode(self, search_index):
        match_block_adder = self.BLOCK_SIZE

        if self.CheckBlockMark():
            if self.match_position != -1 and self.match_length > 1:
                self.WriteFlagBit(0)

                self.match_position = self.uncompressed_index - self.match_position

                if self.match_length > 0x04:
                    self.WriteFlagBit(1)

                    if self.match_length == 0x08:
                        self.WriteFlagBit(0)
                        self.WriteFlagBit(1)
                        self.WriteFlagBit(1)
                    elif self.match_length == 0x07:
                        self.WriteFlagBit(0)
                        self.WriteFlagBit(1)
                        self.WriteFlagBit(0)
                    elif self.match_length == 0x06:
                        self.WriteFlagBit(0)
                        self.WriteFlagBit(0)
                        self.WriteFlagBit(1)
                    elif self.match_length == 0x05:
                        self.WriteFlagBit(0)
                        self.WriteFlagBit(0)
                        self.WriteFlagBit(0)
                    else:
                        self.flagged_length = (self.match_length - 0x09)
                        self.WriteFlagBit(1)

                    if self.match_position > (match_block_adder + 0x111000):
                        self.WriteFlagBit(1)
                        self.WriteFlagBit(1)
                        self.WriteFlagBit(1)
                        self.match_position -= (match_block_adder + 0x111000 + 0x01)
                        self.WriteReversedFlagBit(self.match_position, 0x17)
                    elif self.match_position > (match_block_adder + 0x11000):
                        self.WriteFlagBit(1)
                        self.WriteFlagBit(0)
                        self.match_position -= (match_block_adder + 0x11000 + 0x01)
                        self.WriteReversedFlagBit(self.match_position, 0x14)
                    elif self.match_position > (match_block_adder + 0x1000):
                        self.WriteFlagBit(0)
                        self.WriteFlagBit(1)
                        self.match_position -= (match_block_adder + 0x1000 + 0x01)
                        self.WriteReversedFlagBit(self.match_position, 0x10)
                    elif self.match_position > match_block_adder:
                        self.WriteFlagBit(1)
                        self.WriteFlagBit(1)
                        self.WriteFlagBit(0)
                        self.match_position -= (match_block_adder + 0x01)
                        self.WriteReversedFlagBit(self.match_position, 0x0C)
                    else:
                        self.WriteFlagBit(0)
                        self.WriteFlagBit(0)
                        self.match_position -= 0x01
                        self.WriteReversedFlagBit(self.match_position, 0x08)
                else:
                    self.WriteFlagBit(0)

                    if self.match_length == 0x04:
                        self.WriteFlagBit(1)

                        if self.match_position > (match_block_adder + 0x11000):
                            self.WriteFlagBit(1)
                            self.WriteFlagBit(1)
                            self.match_position -= (match_block_adder + 0x11000 + 0x01)
                            self.WriteReversedFlagBit(self.match_position, 0x14)
                        elif self.match_position > (match_block_adder + 0x1000):
                            self.WriteFlagBit(1)
                            self.WriteFlagBit(0)
                            self.match_position -= (match_block_adder + 0x1000 + 0x01)
                            self.WriteReversedFlagBit(self.match_position, 0x10)
                        elif self.match_position > match_block_adder:
                            self.WriteFlagBit(0)
                            self.WriteFlagBit(1)
                            self.match_position -= (match_block_adder + 0x01)
                            self.WriteReversedFlagBit(self.match_position, 0x0C)
                        else:
                            self.WriteFlagBit(0)
                            self.WriteFlagBit(0)
                            self.match_position -= 0x01
                            self.WriteReversedFlagBit(self.match_position, 0x08)
                    else:
                        self.WriteFlagBit(0)

                        if self.match_length == 0x03:
                            self.WriteFlagBit(1)

                            if self.match_position > match_block_adder:
                                self.WriteFlagBit(1)
                                self.match_position -= (match_block_adder + 0x01)
                                self.WriteReversedFlagBit(self.match_position, 0x0C)
                            else:
                                self.WriteFlagBit(0)
                                self.match_position -= 0x01
                                self.WriteReversedFlagBit(self.match_position, 0x08)
                        elif self.match_length == 0x02:
                            self.WriteFlagBit(0)

                            self.match_position -= 0x01
                            self.WriteReversedFlagBit(self.match_position, 0x08)
            else:
                self.AddPendingByte(self.uncompressed_data[search_index])
                self.WriteFlagBit(1, 1, True)

            self.uncompressed_index += self.match_length

            return True
        else:
            return False

    def End(self):
        if self.flag_bit_index > 0:
            self.WriteFlagBit(0x00, (0x08 - self.flag_bit_index))

    def Lzj_Compress(self, uncompressed_data):
        self.uncompressed_data = uncompressed_data
        self.uncompressed_length = len(uncompressed_data)

        if False:
            cool1 = {}
            coolN = {}
            while self.uncompressed_index < self.uncompressed_length:
                for i in range(2, 8):
                    S = self.uncompressed_data[self.uncompressed_index:self.uncompressed_index+i]
                    if S in coolN:
                        coolN[S] += 1
                    elif S in cool1:
                        coolN[S] = 2
                    else:
                        cool1[S] = 1

                self.uncompressed_index += 1

            for ii in coolN.keys():
                if coolN[ii] > 1:
                    print("'" + ii.hex() + "'," + str(coolN[ii]))

        self.uncompressed_data = uncompressed_data
        self.uncompressed_length = len(uncompressed_data)

        self.compressed_data.extend(self.uncompressed_length.to_bytes(4, "little"))
        self.compressed_index += 4

        self.MixingModel1(self.Encode, self.End)

        return self.compressed_data

    def read_flag_bit(self):
        prev_bit = ((self.flag & 1) == 1)

        self.flag >>= 1
        self.flag_bit_index -= 1

        if self.flag_bit_index <= 0:
            self.flag_bit_index = 8
            self.flag = self.compressed_data[self.compressed_index] if self.compressed_index < self.compressed_length else 0x00
            self.compressed_index += 1

        return prev_bit

    def _add_byte(self, byte):
        self.uncompressed_data[self.uncompressed_index] = byte
        self.uncompressed_index += 1

    def _copy_bytes(self, size):
        for p in range(size):
            self._add_byte(self.compressed_data[self.compressed_index])
            self.compressed_index += 1

    def DecodeLiteral(self):
        block_index = 0

        # If the index value is above 256 then stop early
        stop_early = (self.version == LZJ_VERSION.VERSION2 and self.match_block_index_length == 0x0c)
        while self.match_block_index_length > 0:
            self.read_flag_bit()
            block_index = (block_index * 2) + (self.flag & 1)
            self.match_block_index_length -= 1

            if self.match_block_index_length <= 0x08 and stop_early:
                if block_index != 0:
                    stop_early = False
                else:
                    break

        if not stop_early:
            self.match_position = (self.match_block_position + block_index)

        match_index = self.uncompressed_index - self.match_position

        if self.uncompressed_length < (match_index + self.match_length):
            self.match_length = self.uncompressed_length - match_index
        elif match_index > self.uncompressed_index:
            print("\tBORKED [" + hex(match_index) + " > " + hex(self.uncompressed_index) + "]! Returning, stopped at offset " + hex(self.compressed_index))

            return False
        elif match_index < 0x00:
            print("\tBORKED [" + hex(match_index) + " < 0x00]! Returning, stopped at offset " + hex(self.compressed_index))

            return False

        while self.match_length != 0:
            self._add_byte(self.uncompressed_data[match_index])
            match_index += 1

            self.match_length -= 1

        return True

    def Lzj_Expand(self, compressed_data):
        self.compressed_data = compressed_data
        self.compressed_length = len(compressed_data)

        self.uncompressed_length = int.from_bytes(compressed_data[0:4], "little")
        self.uncompressed_data = bytearray(self.uncompressed_length)
        self.compressed_index += 4

        match_block_adder = self.BLOCK_SIZE

        if self.version == LZJ_VERSION.VERSION2:
            match_block_adder = 0
        else:
            match_block_adder = self.BLOCK_SIZE

        while self.uncompressed_length > self.uncompressed_index:
            self.match_length = 0x00
            self.read_flag_bit() # read bit 1

            if self.uncompressed_index >= self.next_block_position:
                self.next_block_position = self.uncompressed_index + self.BLOCK_SIZE
                if (self.flag & 1) == 1: # check bit 1
                    self._copy_bytes(self.BLOCK_SIZE)
            elif (self.flag & 1) == 1: # check bit 1
                self._copy_bytes(1)
            else:
                self.read_flag_bit() # read bit 2
                
                if self.read_flag_bit(): # read bit 3, check bit 2
                    self.match_length = 0x05

                    if (self.flag & 1) == 1: # check bit 3
                        self.match_length = compressed_data[self.compressed_index] + 0x09
                        self.compressed_index += 1
                    else:
                        self.read_flag_bit() # read bit 4

                        if (self.flag & 1) == 1: # check bit 4
                            self.match_length = 0x07

                        self.read_flag_bit() # read bit 5

                        if (self.flag & 1) == 1: # check bit 5
                            self.match_length += 0x01

                    self.read_flag_bit() # read bit 6

                    if self.read_flag_bit(): # read bit 7, check bit 6
                        if (self.flag & 1) == 1: # check bit 7
                            if self.version != LZJ_VERSION.VERSION2 or self.uncompressed_index > (0x111000 + 0x01):
                                self.read_flag_bit() # read bit 8

                                if (self.flag & 1) == 1: # check bit 8
                                    self.match_block_position = match_block_adder + 0x111000 + 0x01
                                    self.match_block_index_length = 0x17
                                else:
                                    self.match_block_position = match_block_adder + 0x01
                                    self.match_block_index_length = 0x0C
                            else:
                                self.match_block_position = match_block_adder + 0x01
                                self.match_block_index_length = 0x0C
                        else:
                            self.match_block_position = match_block_adder + 0x11000 + 0x01
                            self.match_block_index_length = 0x14
                    else:
                        if (self.flag & 1) == 1: # check bit 7
                            self.match_block_position = match_block_adder + 0x1000 + 0x01
                            self.match_block_index_length = 0x10
                        else:
                            self.match_block_position = 0x01
                            self.match_block_index_length = 0x08
                else:
                    if self.read_flag_bit(): # read bit 4, check bit 3
                        ####
                        self.match_length = 0x04

                        if self.read_flag_bit(): # read bit 5, check bit 4
                            if (self.flag & 1) == 1: # check bit 5
                                self.match_block_position = match_block_adder + 0x11000 + 0x01
                                self.match_block_index_length = 0x14
                            else:
                                self.match_block_position = match_block_adder + 0x1000 + 0x01
                                self.match_block_index_length = 0x10
                        else:
                            if (self.flag & 1) == 1: # check bit 5
                                self.match_block_position = match_block_adder + 0x01
                                self.match_block_index_length = 0x0C
                            else:
                                self.match_block_position = 0x01
                                self.match_block_index_length = 0x08
                    else:
                        if (self.flag & 1) == 1: # check bit 4
                            ####
                            self.match_length = 0x03

                            self.read_flag_bit() # read bit 5

                            if self.version == LZJ_VERSION.VERSION0:
                                if (self.flag & 1) == 1: # check bit 5
                                    self.match_block_position = match_block_adder + 0x1000 + 0x01
                                    self.match_block_index_length = 0x10
                                else:
                                    self.read_flag_bit() # read bit 6

                                    if (self.flag & 1) == 1: # check bit 6
                                        self.match_block_position = match_block_adder + 0x01
                                        self.match_block_index_length = 0x0c
                                    else:
                                        self.match_block_position = 0x01
                                        self.match_block_index_length = 0x08
                            else:
                                if (self.flag & 1) == 1: # check bit 5
                                    self.match_block_position = match_block_adder + 0x01
                                    self.match_block_index_length = 0x0C
                                else:
                                    self.match_block_position = 0x01
                                    self.match_block_index_length = 0x08
                        else:
                            ####
                            self.match_length = 0x02

                            self.match_block_position = 0x01
                            self.match_block_index_length = 0x08

                if not self.DecodeLiteral():
                    break

        return self.uncompressed_data
