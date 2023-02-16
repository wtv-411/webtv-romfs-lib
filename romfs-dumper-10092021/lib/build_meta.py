import os
import sys
import tempfile
import ctypes
from enum import Enum
from lib.lzss import *
from lib.lzj import *
from lib.tea import *

class OBJECT_TYPE(int, Enum):
    UNKNOWN   = 0
    FILE      = 1
    DIRECTORY = 2

class ROMFS_TYPE(int, Enum):
    UNKNOWN             = 0
    VIEWER              = 1
    VIEWER_SCRAMBLED    = 2
    BOX                 = 3
    COMPRESSED_BOX      = 4
    BUILD_BUGGED        = 5
    DREAMCAST           = 6

class FILE_COMPRESSION(int, Enum):
    UNKNOWN = 0
    NONE    = 1
    LZPF    = 2
    LZSS    = 3

class build_meta():
    def print_build_info(build_info, prefix = "Type: "):
        print(prefix + str(build_info["romfs_type"]) + ", Build: " + hex(build_info["build_address"]) + ", Minibrowser: " + hex(build_info["minibrowser_address"]) + ", ROMFS: " + hex(build_info["romfs_address"]) + " [size " + hex(build_info["romfs_size"]) + "]")

    def checksum(data):
        checksum = 0

        if (len(data) % 4) != 0:
            for a in range(4 - (len(data) % 4)):
                data.append(0)

        for i in range(0, len(data), 4):
            checksum += ctypes.c_uint32(
                (data[i] << 0x18) +
                (data[i + 1] << 0x10) +
                (data[i + 2] << 0x08) +
                (data[i + 3])
            ).value

        return checksum & 0xFFFFFFFF

    def address(build_info, position):
        address = position - (build_info["romfs_offset"] - (build_info["romfs_address"] - 0x08))

        if build_info["romfs_type"] == ROMFS_TYPE.BOX:
            address += 0x08
        
        return address

    def position(build_info, address):
        position = build_info["romfs_offset"] - ((build_info["romfs_address"] - address) - 0x08)

        if build_info["romfs_type"] == ROMFS_TYPE.BOX:
            position -= 0x08

        return position

    def romfs_base(f, build_info, file_size = 0xFFFFFFFF):
        if build_info["romfs_type"] == ROMFS_TYPE.BOX:
            f.seek(build_info["romfs_offset"] - 56)
            build_info["romfs_address"] = (build_meta.read32bit(f) + 120)
        elif build_info["romfs_type"] == ROMFS_TYPE.VIEWER or build_info["romfs_type"] == ROMFS_TYPE.DREAMCAST:
            f.seek(build_info["romfs_offset"] - 48)
            start_offset = build_meta.read32bit(f) + 0x78

            f.seek(build_info["romfs_offset"] - 48)
            test_start_offset = build_meta.read32bit(f, "little") + 0x78

            if test_start_offset == (file_size + 0x98):
                start_offset = test_start_offset
                build_info["romfs_type"] = ROMFS_TYPE.DREAMCAST

            build_info["romfs_address"] = start_offset
        else:
            build_info["romfs_address"] = 0
        
        return build_info

    def test_romfs(f, base, file_size = 0xFFFFFFFF, start_offset = 0):
        base += start_offset

        SIGNATURE_TESTS = [
            {
                "romfs_type": ROMFS_TYPE.VIEWER, 
                "offset": -0x20,
                "signature": b'\x00\x00\x00\x00\x7A\x46\x4C\x41\x53\x48'
            },
            {
                "romfs_type": ROMFS_TYPE.VIEWER,
                "offset": -0x20,
                "signature": b'\x00\x00\x00\x00\x52\x4F\x4D\x00'
            },
            {
                "romfs_type": ROMFS_TYPE.COMPRESSED_BOX,
                "offset": 0,
                "signature": b'\x10\x00\x00\x00\x00\x00\x00\x00'
            },
            {
                "romfs_type": ROMFS_TYPE.BUILD_BUGGED,
                "offset": 0x04,
                "signature": b'\x00\x20\x20\x20'
            },
            {
                "romfs_type": ROMFS_TYPE.BOX,
                "offset": -0x24,
                "signature": b'\x52\x4F\x4D\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            },
            {
                "romfs_type": ROMFS_TYPE.BOX,
                "offset": 0,
                "signature": b'\x10\x00\x00\x12\x00\x00\x00\x00'
            },
            {
                "romfs_type": ROMFS_TYPE.BOX,
                "offset": 0,
                "signature": b'\x10\x00\x00\x11\x00\x00\x00\x00'
            },
            {
                "romfs_type": ROMFS_TYPE.VIEWER_SCRAMBLED,
                "offset": -0x20,
                "signature": b'\x00\x00\x00\x00\x52\x4F\x4D\x00'
            },
            {
                "romfs_type": ROMFS_TYPE.VIEWER_SCRAMBLED,
                "offset": -0x1C,
                "signature": b'\x52\x4F\x4D\x00\x00\x00\x00\x00'
            },
        ]

        for sig_test in SIGNATURE_TESTS:
            if sig_test["offset"] < 0 and abs(base + sig_test["offset"]) < file_size:
                f.seek(base + sig_test["offset"], os.SEEK_END)
            elif sig_test["offset"] < file_size and sig_test["offset"] >= 0:
                f.seek(sig_test["offset"] + start_offset)

            romfs_sig = bytes(f.read(len(sig_test["signature"])))

            if sig_test["romfs_type"] == ROMFS_TYPE.VIEWER_SCRAMBLED:
                if romfs_cipher.unscramble(romfs_sig) == sig_test["signature"]:
                    return sig_test["romfs_type"]
            else:
                if romfs_sig == sig_test["signature"]:
                    return sig_test["romfs_type"]

        return None
        
    def read32bit(f, endian = "big", position = -1, start_offset = 0):
        if position != -1:
            f.seek(start_offset + position)

        intval = int.from_bytes(bytes(f.read(4)), endian)

        return intval
    
    def detect(path):
        BUILD_START = b'\x10\x00\x00'
        COMPRESSED_BUILD_START = b'\x10\x00\x00\x00'
        AUTODISK_FILEM_MAGIC = 0x39592841
        AUTODISK_FILED_MAGIC = 0x11993456
        NOROMFS_MAGIC = 0x4E6F4653 # NoFS
        MIN_FILE_SIZE = 0x1000

        build_info = {
            "path": path,

            "build_address": 0,
            "start_offset": 0,
            "end_offset": 0,

            "build_size": -1,
            "code_checksum": -1,
            "code_size": -1,

            "minibrowser_offset": -1,
            "minibrowser_address": -1,

            "romfs_type": ROMFS_TYPE.UNKNOWN,
            "romfs_address": -1,
            "romfs_offset": -1,
            "romfs_end_address": -1,
            "romfs_end_offset": -1,
            "romfs_size": -1,

            "autodisk_offset": -1,
            "autodisk_address": -1,
       }

        file_size = 0

        def check_offsets(f, start_offset = 0):
            nonlocal build_info
            
            f.seek(start_offset)
            if bytes(f.read(len(COMPRESSED_BUILD_START))) == COMPRESSED_BUILD_START:
                build_info["end_offset"] = 0

                return True
            else:
                f.seek(start_offset)
                if bytes(f.read(len(BUILD_START))) == BUILD_START:
                    build_info["start_offset"] = start_offset

                    build_info["code_checksum"] = build_meta.read32bit(f, "big", 0x08, build_info["start_offset"])
                    build_info["build_size"] = build_meta.read32bit(f, "big", 0x0C, build_info["start_offset"]) << 2
                    build_info["code_size"] = build_meta.read32bit(f, "big", 0x10, build_info["start_offset"]) << 2

                    build_info["build_address"] = build_meta.read32bit(f, "big", 0x30, build_info["start_offset"])

                    _romfs_address = build_meta.read32bit(f, "big", 0x24, build_info["start_offset"])
                    _compressed_minibrowser_address = build_meta.read32bit(f, "big", 0x3C, build_info["start_offset"])

                    _romfs_offset = (_romfs_address - build_info["build_address"])

                    if _romfs_address != NOROMFS_MAGIC and file_size >= _romfs_offset:
                        build_info["romfs_address"] = _romfs_address
                        build_info["romfs_offset"] = _romfs_offset

                        _end_offset = build_info["romfs_offset"]

                        if file_size >= _romfs_offset + 4:
                            build_info["footer_length"] = file_size - _romfs_offset
                            build_info["footer_offset"] = _romfs_offset
                            build_info["footer_address"] = _romfs_address

                            autodisk_metadata_magic = build_meta.read32bit(f, "big", _romfs_offset, build_info["start_offset"])
                            if autodisk_metadata_magic == AUTODISK_FILEM_MAGIC:
                                autodisk_metadata_size = build_meta.read32bit(f, "big", _romfs_offset + 0x10, build_info["start_offset"])
                                autodisk_file_count = build_meta.read32bit(f, "big", _romfs_offset + 0x14, build_info["start_offset"])

                                if autodisk_metadata_size > 0 and autodisk_metadata_size < 0x10001 and autodisk_file_count > 0 and autodisk_file_count < 0x401:
                                    autodisk_filedata_offset = _romfs_offset + autodisk_metadata_size

                                    autodisk_filedata_magic = build_meta.read32bit(f, "big", autodisk_filedata_offset - 4, build_info["start_offset"])

                                    if autodisk_filedata_magic == AUTODISK_FILED_MAGIC:
                                        build_info["autodisk_offset"] = _romfs_offset
                                        build_info["autodisk_address"] = _romfs_address

                                        _end_offset = file_size

                        build_info["end_offset"] = -1 * (file_size - _end_offset)

                    if _compressed_minibrowser_address > 0 and _compressed_minibrowser_address > build_info["build_address"]:
                        _minibrowser_offset = (_compressed_minibrowser_address - build_info["build_address"]) + 0x10

                        if _minibrowser_offset <= file_size:
                            build_info["minibrowser_address"] = _compressed_minibrowser_address
                            build_info["minibrowser_offset"] = _minibrowser_offset
                    
                    return True


        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()

            build_info["start_offset"] = 0

            if file_size > MIN_FILE_SIZE:
                if not check_offsets(f, 0) and check_offsets(f, 0x20):
                    build_info["start_offset"] = 0x20

                detected_romfs_type = build_meta.test_romfs(f, build_info["end_offset"], file_size, build_info["start_offset"])
                if detected_romfs_type is None:
                    build_info["start_offset"] = 0
                    build_info["end_offset"] = 0
                    detected_romfs_type = build_meta.test_romfs(f, build_info["end_offset"], file_size, build_info["start_offset"])

                if detected_romfs_type is not None:
                    build_info["romfs_type"] = detected_romfs_type

                    if detected_romfs_type == ROMFS_TYPE.BOX:
                        build_info["romfs_size"] = build_meta.read32bit(f, "big", build_info["romfs_offset"] - 0x08, build_info["start_offset"])
                    else:
                        build_info["romfs_offset"] = file_size
                        build_info["romfs_size"] = build_info["romfs_offset"]

                    build_info["romfs_end_address"] = build_info["romfs_address"] - 8 - (build_info["romfs_size"] * 4)
                    build_info["romfs_end_offset"] = build_info["romfs_offset"] - 8 - (build_info["romfs_size"] * 4)

                    build_info["romfs_offset"] += build_info["start_offset"]
                    build_info["romfs_end_offset"] += build_info["start_offset"]

                    if build_info["minibrowser_offset"] >= 0:
                        build_info["minibrowser_offset"] += build_info["start_offset"]

                    if build_info["autodisk_offset"] >= 0:
                        build_info["autodisk_offset"] += build_info["start_offset"]

                    if build_info["romfs_address"] == -1:
                        build_info = build_meta.romfs_base(f, build_info, file_size)

            f.close()

        return build_info

class build_matryoshka():
    def expand_minibrowser(build_info):
        LZSS_START = b'\x10\x00\x00'

        td, tmp_path = tempfile.mkstemp()

        print("\tExpanding minibrowser...")

        if build_info["minibrowser_offset"] > 0:
            with os.fdopen(td, "wb") as t:
                with open(build_info["path"], "rb") as f:
                    f.seek(0, os.SEEK_END)
                    file_size = f.tell()

                    f.seek(build_info["minibrowser_offset"])
                    data = f.read(file_size - build_info["minibrowser_offset"])

                    if data[1:4] == LZSS_START:
                        d = lzss()

                        t.write(d.Lzss_Expand(data, 0x1c0000))
                    else:
                        d = lzj(LZJ_VERSION.VERSION1)
                        t.write(d.Lzj_Expand(data))

                    f.close()
                t.close()

            new_build_info = build_meta.detect(tmp_path)

            new_build_info["is_secondary_image"] = True
            new_build_info["original_path"] = build_info["path"]

            print("\tDone expanding minibrowser!")

            return new_build_info
        else:
            print("No minibrowser found")

            return build_info

    def expand_build(build_info):
        td, tmp_path = tempfile.mkstemp()

        print("\tExpanding build...")

        with os.fdopen(td, "wb") as t:
            with open(build_info["path"], "rb") as f:
                f.seek(0, os.SEEK_END)
                file_size = f.tell()

                f.seek(0x28)
                lzj_version = int.from_bytes(bytes(f.read(4)), "big")

                f.seek(0x200)
                data = f.read(file_size)

                d = lzj(LZJ_VERSION(lzj_version))
                t.write(d.Lzj_Expand(data))

                f.close()
            t.close()

            new_build_info = build_meta.detect(tmp_path)

            new_build_info["is_secondary_image"] = True
            new_build_info["original_path"] = build_info["path"]

            print("\n\tDone expanding build!")

            return new_build_info

class romfs_cipher():
    SCRAMBLE_KEY =b'\xFE\x0F\x8A\x50\x40\x38\x8A\x7C\x14\x22\x84\x7C\xBF\x52\xA4\x50'

    def unscramble(data):
        return tea.decrypt(data, romfs_cipher.SCRAMBLE_KEY)

    def scramble(data):
        return tea.encrypt(data, romfs_cipher.SCRAMBLE_KEY)

    def scramble_vwr_file(build_info, data):
        td, tmp_path = tempfile.mkstemp()

        print("\tScrambling romfs file...")

        file_size = len(data)
        with open(build_info["path"], "wb") as f:
            current_position = 0
            while (file_size - current_position) > 8:
                f.write(romfs_cipher.scramble(data[current_position:(current_position + 8)]))

                current_position += 8

                print("\r\t\t" + str(int((current_position / file_size) * 100)) + "%", end='', flush=True)

            f.write(data[current_position:(current_position + 8)])
            f.close()

        print("\r\tDone Scrambling romfs file!", flush=True)

    def unscramble_vwr_file(build_info):
        td, tmp_path = tempfile.mkstemp()

        print("\tUnscrambling vwr file...")

        with os.fdopen(td, "wb") as t:
            with open(build_info["path"], "rb") as f:
                f.seek(0, os.SEEK_END)
                file_size = f.tell()

                current_position = 0
                while (file_size - current_position) > 8:
                    f.seek(current_position)

                    t.write(romfs_cipher.unscramble(f.read(8)))

                    current_position += 8

                    print("\r\t\t" + str(int((current_position / file_size) * 100)) + "%", end='', flush=True)

                f.seek(current_position)
                t.write(f.read(8))

                f.close()
            t.close()

        new_build_info = build_meta.detect(tmp_path)

        new_build_info["original_path"] = build_info["path"]

        print("\r\tDone unscrambling vwr file!", flush=True)
        
        return new_build_info
