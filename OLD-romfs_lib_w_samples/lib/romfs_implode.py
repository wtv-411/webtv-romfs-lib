import os
from os import listdir
from os.path import isfile, join
import sys
import struct
import math
import tempfile
import shutil
import zlib
import re
from lib.lzpf import *
from lib.lzss import *
from lib.lzj import *
from lib.romfs_type import *
import ctypes

class romfs_implode():
    def scrample_romfs_file(romfs_info, data):
        td, tmp_path = tempfile.mkstemp()

        print("\tScrambling romfs file...")

        file_size = len(data)
        with open(romfs_info["path"], "wb") as f:
            current_position = 0
            while (file_size - current_position) > 8:
                f.write(romfs_sniff.scramble(data[current_position:(current_position + 8)]))

                current_position += 8

                print("\r\t\t" + str(int((current_position / file_size) * 100)) + "%", end='', flush=True)

            f.write(data[current_position:(current_position + 8)])
            f.close()

        print("\r\tDone Scrambling romfs file!", flush=True)

    def write_romfs_file(romfs_info, data):
        with open(romfs_info["path"], 'wb') as f:
            f.write(data)

            f.close()


    def natural_sort(l): 
        convert = lambda text: int(text) if text.isdigit() else text.lower() 
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
        return sorted(l, key=alphanum_key)

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

    def get_file_data(path):
        data = b''

        with open(path, 'rb') as f:
            f.seek(0, os.SEEK_END)
            data_size = f.tell()

            f.seek(0)
            data = f.read(data_size)

            f.close()

        return bytearray(data)

    def build_romfs(directory_path, romfs_info):
        object_count = 0
        files_blob_size = 0
        romfs_blob = None
        files_blob_offset = 0
        object_table_offset = 0

        print("\tBuilding romfs")

        endian = ""
        if romfs_info["type"] == ROMFS_TYPE.DREAMCAST:
            endian = "<"
        else:
            endian = ">"

        def _build_romfs(romfs_nodes, parent_address = 0):
            nonlocal endian, romfs_blob, files_blob_offset, object_table_offset

            starting_table_offset = object_table_offset - 0x38
            previous_table_offset = -1

            if parent_address > 0:
                parent_address = romfs_sniff.address(romfs_info, parent_address)

            for romfs_node in romfs_nodes:
                object_table_offset -= 0x38
                current_table_offset = object_table_offset
                child_list_offset = 0
                data_offset = 0

                if romfs_node["type"] == OBJECT_TYPE.DIRECTORY:
                    child_list_offset = romfs_sniff.address(romfs_info, _build_romfs(romfs_node["children"], object_table_offset))
                    data_offset = 0
                else:
                    child_list_offset = 0
                    _data_offset = files_blob_offset - romfs_node["aligned_size"]

                    romfs_blob[_data_offset:files_blob_offset] = romfs_node["data"]
                    files_blob_offset -= romfs_node["aligned_size"]
                    
                    data_offset = romfs_sniff.address(romfs_info, _data_offset)

                if previous_table_offset >= 0:
                    struct.pack_into(
                        endian + "I",
                        romfs_blob,
                        previous_table_offset,
                        romfs_sniff.address(romfs_info, current_table_offset)
                    )

                struct.pack_into(
                    endian + "IIIIIII28s",
                    romfs_blob,
                    current_table_offset,
                    0,
                    parent_address,
                    child_list_offset,
                    data_offset,
                    romfs_node["data_size"],
                    0,
                    romfs_node["data_checksum"],
                    bytes(romfs_node["name"], "ascii", "ignore")
                )

                previous_table_offset = current_table_offset

                compression = "UNKNOWN"
                if romfs_node["compression_type"] == FILE_COMPRESSION.LZFP:
                    compression = "LZFP"
                elif romfs_node["compression_type"] == FILE_COMPRESSION.LZSS:
                    compression = "LZSS"
                else:
                    compression = "NONE"

                print("\tPack[" + compression + "]: " + romfs_node["path"])

            return starting_table_offset


        def _walk_directory(path, depth = 0):
            nonlocal object_count, files_blob_size

            objects = romfs_implode.natural_sort(listdir(path))

            _romfs_nodes = []
            
            for name in objects:
                object_path = join(path, name)

                file_type = OBJECT_TYPE.UNKNOWN
                children = []
                compression_type = FILE_COMPRESSION.UNKNOWN
                compressed_size = -1
                data = b''
                file_size = 0
                aligned_size = 0
                data_checksum = 0

                if isfile(object_path):
                    data = romfs_implode.get_file_data(object_path)

                    if len(data) == 0:
                        continue
                    
                    file_size = len(data)
                    for a in range(4 - (file_size % 4)):
                        data.append(0)
                    aligned_size = len(data)

                    file_type = OBJECT_TYPE.FILE
                    compression_type = FILE_COMPRESSION.NONE
                    compressed_size = -1
                    data_checksum = romfs_implode.checksum(data)
                else: 
                    file_type = OBJECT_TYPE.DIRECTORY

                    children = _walk_directory(object_path, (depth + 1))

                object_count += 1
                files_blob_size += aligned_size

                print("\r\t\tObject count: " + str(object_count), end='', flush=True)

                romfs_node = {
                    "address": 0,
                    "position": 0,
                    "type": file_type,
                    "next_link": 0,
                    "parent": 0,
                    "child_list": 0,
                    "data_address": 0,
                    "reserve": 0,
                    "data_checksum": data_checksum,
                    "compression_type": compression_type,
                    "compressed_size": compressed_size,
                    "data_offset": 0,
                    "data_size": file_size,
                    "aligned_size": aligned_size,
                    "data": data,
                    "name": name,
                    "path": object_path,
                    "depth": depth,
                    "children": children
                }

                _romfs_nodes.append(romfs_node)

            return _romfs_nodes
        
        print("\tWalking directory:", directory_path)

        romfs_nodes = _walk_directory(directory_path)

        print("\r\tDone walking Directory                ", flush=True)

        romfs_size = files_blob_size + (0x38 * object_count)

        files_blob_offset = files_blob_size
        object_table_offset = romfs_size

        romfs_info["romfs_offset"] = object_table_offset

        if romfs_info["type"] == ROMFS_TYPE.DREAMCAST:
            romfs_info["romfs_address"] = object_table_offset + 0x98

        romfs_blob = bytearray(romfs_size)
        _build_romfs(romfs_nodes)

        print("\tDone building romfs!")

        return romfs_blob

    def pack(origin, romfs_info):
        romfs_sniff.print_romfs_info(romfs_info)

        if romfs_info["type"] == ROMFS_TYPE.VIEWER_SCRAMBLED:
            romfs_implode.scrample_romfs_file(romfs_info, romfs_implode.build_romfs(origin, romfs_info))
        else:
            romfs_implode.write_romfs_file(romfs_info, romfs_implode.build_romfs(origin, romfs_info))
