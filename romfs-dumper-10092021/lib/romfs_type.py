import os
import sys
from enum import Enum
from lib.tea import *

class OBJECT_TYPE(Enum):
    UNKNOWN   = 0
    FILE      = 1
    DIRECTORY = 2

class ROMFS_TYPE(Enum):
    UNKNOWN             = 0
    VIEWER              = 1
    VIEWER_SCRAMBLED    = 2
    BOX                 = 3
    COMPRESSED_BOX      = 4
    BUILD_BUGGED        = 5
    DREAMCAST           = 6

class FILE_COMPRESSION(Enum):
    UNKNOWN = 0
    NONE    = 1
    LZFP    = 2
    LZSS    = 3

class romfs_sniff():
    SCRAMBLE_KEY =b'\xFE\x0F\x8A\x50\x40\x38\x8A\x7C\x14\x22\x84\x7C\xBF\x52\xA4\x50'

    def print_romfs_info(romfs_info, prefix = "Type: "):
        print(prefix + str(romfs_info["type"]) + ", Buld: " + hex(romfs_info["build_address"]) + ", Minibrowser: " + hex(romfs_info["minibrowser_address"]) + ", ROMFS: " + hex(romfs_info["romfs_address"]) + " [size " + hex(romfs_info["romfs_size"]) + "]")

    def address(romfs_info, position):
        address = position - (romfs_info["romfs_offset"] - (romfs_info["romfs_address"] - 0x08))

        if romfs_info["type"] == ROMFS_TYPE.BOX:
            address += 0x08
        
        return address

    def position(romfs_info, address):
        position = romfs_info["romfs_offset"] - ((romfs_info["romfs_address"] - address) - 0x08)

        if romfs_info["type"] == ROMFS_TYPE.BOX:
            position -= 0x08

        return position

    def romfs_base(f, romfs_info, file_size = 0xFFFFFFFF):
        if romfs_info["type"] == ROMFS_TYPE.BOX:
            f.seek(romfs_info["romfs_offset"] - 56)
            romfs_info["romfs_address"] = (romfs_sniff.read32bit(f) + 120)
        elif romfs_info["type"] == ROMFS_TYPE.VIEWER or romfs_info["type"] == ROMFS_TYPE.DREAMCAST:
            f.seek(romfs_info["romfs_offset"] - 48)
            start_offset = romfs_sniff.read32bit(f) + 0x78

            f.seek(romfs_info["romfs_offset"] - 48)
            test_start_offset = romfs_sniff.read32bit(f, "little") + 0x78

            if test_start_offset == (file_size + 0x98):
                start_offset = test_start_offset
                romfs_info["type"] = ROMFS_TYPE.DREAMCAST

            romfs_info["romfs_address"] = start_offset
        else:
            romfs_info["romfs_address"] = 0
        
        return romfs_info

    def unscramble(data):
        return tea.decrypt(data, romfs_sniff.SCRAMBLE_KEY)

    def scramble(data):
        return tea.encrypt(data, romfs_sniff.SCRAMBLE_KEY)

    def test(f, base, file_size = 0xFFFFFFFF, start_offset = 0):
        base += start_offset

        SIGNATURE_TESTS = [
            {
                "type": ROMFS_TYPE.VIEWER, 
                "offset": -0x20,
                "signature": b'\x00\x00\x00\x00\x7A\x46\x4C\x41\x53\x48'
            },
            {
                "type": ROMFS_TYPE.VIEWER,
                "offset": -0x20,
                "signature": b'\x00\x00\x00\x00\x52\x4F\x4D\x00'
            },
            {
                "type": ROMFS_TYPE.COMPRESSED_BOX,
                "offset": 0,
                "signature": b'\x10\x00\x00\x00\x00\x00\x00\x00'
            },
            {
                "type": ROMFS_TYPE.BUILD_BUGGED,
                "offset": 0x04,
                "signature": b'\x00\x20\x20\x20'
            },
            {
                "type": ROMFS_TYPE.BOX,
                "offset": -0x24,
                "signature": b'\x52\x4F\x4D\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            },
            {
                "type": ROMFS_TYPE.VIEWER_SCRAMBLED,
                "offset": -0x20,
                "signature": b'\x00\x00\x00\x00\x52\x4F\x4D\x00'
            },
        ]

        for sig_test in SIGNATURE_TESTS:
            if sig_test["offset"] < 0 and abs(base + sig_test["offset"]) < file_size:
                f.seek(base + sig_test["offset"], os.SEEK_END)
            elif sig_test["offset"] < file_size and sig_test["offset"] >= 0:
                f.seek(sig_test["offset"] + start_offset)

            romfs_sig = bytes(f.read(len(sig_test["signature"])))

            if sig_test["type"] == ROMFS_TYPE.VIEWER_SCRAMBLED:
                if romfs_sniff.unscramble(romfs_sig) == sig_test["signature"]:
                    return sig_test["type"]
            else:
                if romfs_sig == sig_test["signature"]:
                    return sig_test["type"]

        return None
        
    def define(path, type = ROMFS_TYPE.UNKNOWN, start_offset = 0, end_offset = 0, romfs_address = -1, romfs_offset = -1, romfs_end_address = -1, romfs_end_offset = -1, romfs_size = -1, build_address = 0, minibrowser_address = -1, minibrowser_offset = -1):
        return {
            "path": path,
            "type": type,

            "start_offset": start_offset,
            "end_offset": end_offset,

            "romfs_address": romfs_address,
            "romfs_offset": romfs_offset,

            "romfs_end_address": romfs_end_address,
            "romfs_end_offset": romfs_end_offset,

            "romfs_size": romfs_size,

            "build_address": build_address,

            "minibrowser_address": minibrowser_address,
            "minibrowser_offset": minibrowser_offset
        }

    def read32bit(f, endian = "big", position = -1, start_offset = 0):
        if position != -1:
            f.seek(start_offset + position)

        intval = int.from_bytes(bytes(f.read(4)), endian)

        return intval
    
    def detect(path):
        BUILD_START = b'\x10\x00\x00'
        COMPRESSED_BUILD_START = b'\x10\x00\x00\x00'
        MIN_FILE_SIZE = 0x1000

        romfs_info = romfs_sniff.define(path)

        end_offset = 0
        romfs_address = -1
        romfs_offset = -1
        romfs_end_address = -1
        romfs_end_offset = -1
        build_address = -1
        minibrowser_address = -1
        minibrowser_offset = -1

        def check_base(file_size, _build_address, _romfs_address, _compressed_minibrowser_address):
            nonlocal end_offset, romfs_address, build_address, minibrowser_address, minibrowser_offset

            romfs_offset = (_romfs_address - _build_address)

            if file_size >= romfs_offset:
                build_address = _build_address
                romfs_address = _romfs_address

                end_offset = -1 * (file_size - romfs_offset)

                if _compressed_minibrowser_address > 0 and _compressed_minibrowser_address > build_address:
                    minibrowser_offset = (_compressed_minibrowser_address - build_address) + 0x10

                    if minibrowser_offset > file_size:
                        minibrowser_offset = -1
                    else:
                        minibrowser_address = _compressed_minibrowser_address
                else:
                    minibrowser_offset = -1

                return True
            else:
                return False


        def check_offsets(start_offset = 0):
            nonlocal end_offset, build_address
            
            f.seek(start_offset)
            if bytes(f.read(4)) == COMPRESSED_BUILD_START:
                end_offset = 0

                return True
            else:
                f.seek(start_offset)
                if bytes(f.read(3)) == BUILD_START:
                    _build_address = romfs_sniff.read32bit(f, "big", 0x30, start_offset)
                    _romfs_address = romfs_sniff.read32bit(f, "big", 0x24, start_offset)
                    _compressed_minibrowser_address = romfs_sniff.read32bit(f, "big", 0x3C, start_offset)

                    if _romfs_address == 0x4E6F4653: # NoFS
                        build_address = _build_address
                    elif not check_base(file_size, _build_address, _romfs_address, _compressed_minibrowser_address):
                        build_address = _build_address
                    
                    return True


        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()

            start_offset = 0

            if file_size > MIN_FILE_SIZE:
                if not check_offsets(0) and check_offsets(0x20):
                    start_offset = 0x20

                detected_type = romfs_sniff.test(f, end_offset, file_size, start_offset)
                if detected_type is None:
                    end_offset = 0
                    start_offset = 0
                    detected_type = romfs_sniff.test(f, end_offset, file_size, start_offset)

                if detected_type is not None:
                    romfs_offset = (file_size + end_offset)

                    if detected_type == ROMFS_TYPE.BOX:
                        romfs_size = romfs_sniff.read32bit(f, "big", romfs_offset - 0x08, start_offset)
                    else:
                        romfs_size = romfs_offset

                    romfs_end_address = romfs_address - romfs_size
                    romfs_end_offset = romfs_offset - romfs_size

                    if minibrowser_offset >= 0:
                        minibrowser_offset += start_offset

                    romfs_info = romfs_sniff.define(
                        path,
                        
                        detected_type,

                        start_offset,
                        end_offset,
                        
                        romfs_address,
                        romfs_offset + start_offset,
                        
                        romfs_end_address,
                        romfs_end_offset + start_offset,

                        romfs_size,

                        build_address,

                        minibrowser_address,
                        minibrowser_offset
                    )

                    if romfs_info["romfs_address"] == -1:
                        romfs_info = romfs_sniff.romfs_base(f, romfs_info, file_size)
                else:
                    romfs_info["build_address"] = build_address

            f.close()

        return romfs_info
