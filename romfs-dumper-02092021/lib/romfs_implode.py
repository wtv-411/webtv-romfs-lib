import os
from os import listdir
from os.path import isfile
import struct
import math
import re
import json
from lib.lzpf import *
from lib.lzss import *
from lib.build_meta import *
import ctypes

class romfs_implode():
    def scrample_romfs_file(build_info, data):
        print("\tScrambling ROMFS file...")

        file_size = len(data)
        with open(build_info["out_path"], "wb") as f:
            current_position = 0
            while (file_size - current_position) > 8:
                f.write(build_meta.scramble(data[current_position:(current_position + 8)]))

                current_position += 8

                print("\r\t\t" + str(int((current_position / file_size) * 100)) + "%", end='', flush=True)

            f.write(data[current_position:(current_position + 8)])
            f.close()

        print("\r\tDone Scrambling ROMFS file!", flush=True)

        print("\tWrote ROMFS to '" + build_info["out_path"] + "'")

    def write_romfs_file(build_info, data):
        with open(build_info["out_path"], 'wb') as f:
            f.write(data)

            f.close()

        if build_info["romfs_type"] == ROMFS_TYPE.BOX or build_info["romfs_type"] == ROMFS_TYPE.COMPRESSED_BOX:
            print("\tWrote ROM to '" + build_info["out_path"] + "'")
        else:
            print("\tWrote ROMFS to '" + build_info["out_path"] + "'")


    def natural_sort(l): 
        convert = lambda text: int(text) if text.isdigit() else text.lower() 
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
        return sorted(l, key=alphanum_key)

    def checksum(data, chunk_size = 4):
        checksum = ctypes.c_uint32(0)

        if chunk_size > 1:
            if (len(data) % chunk_size) != 0:
                for a in range(chunk_size - (len(data) % chunk_size)):
                    data.append(0)

        for i in range(0, len(data), chunk_size):
            if chunk_size == 1:
                checksum.value += data[i]
            elif chunk_size == 2:
                checksum.value += (data[i + 2] << 0x08) + (data[i + 3])
            elif chunk_size == 3:
                checksum.value += (data[i + 1] << 0x10) + (data[i + 2] << 0x08) + (data[i + 3])
            elif chunk_size == 4:
                checksum.value += (data[i] << 0x18) + (data[i + 1] << 0x10) + (data[i + 2] << 0x08) + (data[i + 3])

        return checksum.value

    def get_file_data(path):
        data = b''

        with open(path, 'rb') as f:
            f.seek(0, os.SEEK_END)
            data_size = f.tell()

            f.seek(0)
            data = f.read(data_size)

            f.close()

        return bytearray(data)

    def build_romfs(directory_path, build_info, descriptor_table = None):
        object_count = 0
        files_blob_size = 0
        romfs_blob = None
        files_blob_offset = 0
        object_table_offset = 0

        print("\tBuilding romfs")

        endian = ""
        if build_info["romfs_type"] == ROMFS_TYPE.DREAMCAST:
            endian = "<"
        else:
            endian = ">"

        box_build = False
        if build_info["romfs_type"] == ROMFS_TYPE.BOX or build_info["romfs_type"] == ROMFS_TYPE.COMPRESSED_BOX:
            box_build = True
        else:
            box_build = False

        def _build_romfs(romfs_nodes, parent_address = 0):
            nonlocal endian, romfs_blob, files_blob_offset, object_table_offset

            if romfs_nodes == None or len(romfs_nodes) == 0:
                return 0

            starting_table_offset = object_table_offset - 0x38
            previous_table_offset = -1

            if parent_address > 0:
                parent_address = build_meta.address(build_info, parent_address)

            for romfs_node in romfs_nodes:
                object_table_offset -= 0x38
                current_table_offset = object_table_offset
                child_list_offset = 0
                data_offset = 0

                if romfs_node["type"] == OBJECT_TYPE.DIRECTORY:
                    data_offset = 0

                    _child_list_offset = _build_romfs(romfs_node["children"], object_table_offset)

                    if _child_list_offset != 0:
                        child_list_offset = build_meta.address(build_info, _child_list_offset)
                else:
                    child_list_offset = 0
                    _data_offset = files_blob_offset - romfs_node["aligned_size"]

                    romfs_blob[_data_offset:files_blob_offset] = romfs_node["data"]
                    files_blob_offset -= romfs_node["aligned_size"]
                    
                    data_offset = build_meta.address(build_info, _data_offset)

                if previous_table_offset >= 0:
                    struct.pack_into(
                        endian + "I",
                        romfs_blob,
                        previous_table_offset,
                        build_meta.address(build_info, current_table_offset)
                    )

                size_param = romfs_node["data_size"]
                compression = "UNKNOWN"
                if romfs_node["compression_type"] == FILE_COMPRESSION.LZPF:
                    size_param |= 0x80000000
                    compression = "LZPF"
                elif romfs_node["compression_type"] == FILE_COMPRESSION.LZSS:
                    size_param |= 0x90000000
                    compression = "LZSS"
                else:
                    compression = "NONE"

                struct.pack_into(
                    endian + "IIIIIII28s",
                    romfs_blob,
                    current_table_offset,
                    romfs_node["next_link"],
                    parent_address,
                    child_list_offset,
                    data_offset,
                    size_param,
                    0,
                    romfs_node["data_checksum"],
                    bytes(romfs_node["name"], "ascii", "ignore")
                )

                previous_table_offset = current_table_offset

                print("\tPack[" + compression + "]: " + romfs_node["path"])

            return starting_table_offset


        def _walk_directory(path = "", depth = 0):
            nonlocal descriptor_table, directory_path, object_count, files_blob_size, box_build

            search_dir = directory_path + "/" + path

            objects = romfs_implode.natural_sort(listdir(search_dir))

            _romfs_nodes = []
            
            for name in objects:
                if depth == 0 and name == "dt.json":
                    continue

                roms_path = path + "/" + name
                file_path = search_dir + "/" + name

                file_type = OBJECT_TYPE.UNKNOWN
                children = []
                compression_type = FILE_COMPRESSION.NONE
                compressed_size = -1
                data = b''
                file_size = 0
                data_size = 0
                aligned_size = 0
                data_checksum = 0
                next_link = 0

                if isfile(file_path):
                    data = romfs_implode.get_file_data(file_path)

                    if len(data) == 0:
                        continue

                    file_size = len(data)

                    if box_build and file_size > 10 and descriptor_table != None and "object" in descriptor_table:
                        compression_strategy = "object-table-value"
                        if "compression_strategy" in descriptor_table:
                            compression_strategy = descriptor_table["compression_strategy"]
                        else:
                            compression_strategy = "object-table-value"

                        if "dont_compress" in descriptor_table and roms_path in descriptor_table["dont_compress"]:
                            compression_type = FILE_COMPRESSION.NONE
                        elif compression_strategy == "best":
                            lzpf_len = file_size + 1
                            lzpf_data = b''
                            lzss_len = file_size + 1
                            lzss_data = b''

                            try:
                                c = lzpf()
                                lzpf_data = c.Lzpf_Compress(data, 0x00)
                                lzpf_len = len(lzpf_data)
                            except:
                                pass

                            try:
                                c = lzss()
                                lzss_data = c.Lzss_Compress(data)
                                lzss_len = len(lzss_data)
                            except:
                                pass

                            if lzss_len > file_size and lzpf_len > file_size:
                                compression_type = FILE_COMPRESSION.NONE
                            elif lzss_len >= lzpf_len:
                                compression_type = FILE_COMPRESSION.LZPF
                                data = lzpf_data
                            else:
                                compression_type = FILE_COMPRESSION.LZSS
                                data = lzss_data
                        else:
                            if compression_strategy == "extension-list" and "compressed_extensions" in descriptor_table:
                                extension = os.path.splitext(file_path)[1][1:].lower()
                                if extension in descriptor_table["compressed_extensions"]:
                                    compression_type = FILE_COMPRESSION(descriptor_table["compressed_extensions"][extension])
                            elif compression_strategy == "off":
                                compression_type = FILE_COMPRESSION.NONE
                            else: # object-table-value
                                if roms_path in descriptor_table["object"] and "compression_type" in descriptor_table["object"][roms_path]:
                                    compression_type = FILE_COMPRESSION(descriptor_table["object"][roms_path]["compression_type"])
                                    
                            if compression_type == FILE_COMPRESSION.LZPF:
                                c = lzpf()
                                data = c.Lzpf_Compress(data, 0x00)
                            elif compression_type == FILE_COMPRESSION.LZSS:
                                c = lzss()
                                data = c.Lzss_Compress(data)
                            else:
                                compression_type = FILE_COMPRESSION.NONE

                    if compression_type != FILE_COMPRESSION.NONE:
                        _file_size = bytearray(4)
                        struct.pack_into(
                            endian + "I",
                            _file_size,
                            0,
                            file_size
                        )

                        compressed_size = data_size
                        data = _file_size + data
                    else:
                        compressed_size = -1

                    data_size = len(data)
                    for a in range(4 - (data_size % 4)):
                        data.append(0)

                    aligned_size = len(data)

                    file_type = OBJECT_TYPE.FILE
                    data_checksum = romfs_implode.checksum(data, 1)
                else: 
                    file_type = OBJECT_TYPE.DIRECTORY

                    if descriptor_table != None and "object" in descriptor_table:
                        if depth == 0 and roms_path in descriptor_table["object"] and "next_link" in descriptor_table["object"][roms_path]:
                            next_link = descriptor_table["object"][roms_path]["next_link"]

                    children = _walk_directory(roms_path, (depth + 1))

                object_count += 1
                files_blob_size += aligned_size

                print("\r\t\tObject count: " + str(object_count), end='', flush=True)

                romfs_node = {
                    "address": 0,
                    "position": 0,
                    "type": file_type,
                    "next_link": next_link,
                    "parent": 0,
                    "child_list": 0,
                    "data_address": 0,
                    "reserve": 0,
                    "data_checksum": data_checksum,
                    "compression_type": compression_type,
                    "compressed_size": compressed_size,
                    "data_offset": 0,
                    "file_size": file_size,
                    "data_size": data_size,
                    "aligned_size": aligned_size,
                    "data": data,
                    "name": name,
                    "file_path": file_path,
                    "path": roms_path,
                    "depth": depth,
                    "children": children
                }

                _romfs_nodes.append(romfs_node)

            return _romfs_nodes
        
        print("\tWalking directory:", directory_path)

        romfs_nodes = _walk_directory()

        print("\r\tDone walking Directory                ", flush=True)

        code_section = b''
        footer_section = b''
        code_romfs_padding = b''
        next_romfs = b''
        
        romfs_size = files_blob_size + (0x38 * object_count)

        files_blob_offset = files_blob_size
        object_table_offset = romfs_size
        extra_alloc_bytes = 0

        build_info["romfs_offset"] = object_table_offset

        if build_info["romfs_type"] == ROMFS_TYPE.DREAMCAST:
            build_info["romfs_address"] = object_table_offset + 0x98
        elif box_build:
            extra_alloc_bytes = 8
            build_info["romfs_address"] -= 8

            if build_info["source_build_path"] != None:
                source_build_info = build_meta.detect(build_info["source_build_path"])

                if source_build_info != None:
                    unpadded_size = source_build_info["code_size"] + romfs_size
                    padding_size = build_info["romfs_address"] - (build_info["build_address"] + unpadded_size)

                    if padding_size < 0:
                        print("\t!! ROMFS ADDRESS EXTENDS BEYOND SOURCE.  I WILL EXTEND. THIS MAY NOT WORK!")

                        padding_size = 0
                        build_info["romfs_address"] = build_info["build_address"] + unpadded_size
                    else:
                        code_romfs_padding = b'eMac' * math.ceil(padding_size / 4)

                        code_romfs_padding = code_romfs_padding[0:padding_size]

                    print("\tRetrieving source build data.")

                    with open(build_info["source_build_path"], "rb") as s:
                        s.seek(0, os.SEEK_END)
                        file_size = s.tell()

                        s.seek(source_build_info["start_offset"])
                        code_section = bytearray(s.read(source_build_info["start_offset"] + source_build_info["code_size"]))

                        s.seek(source_build_info["romfs_offset"] - 0x40)
                        next_romfs = bytearray(s.read(4))

                        if source_build_info["footer_length"] > 0:
                            s.seek(source_build_info["start_offset"] + source_build_info["footer_offset"])
                            footer_section = s.read(file_size - source_build_info["footer_offset"])
                else:
                    print("\t!! CAN'T USE SOURCE BUILD! UNABLE TO DETECT FORMAT!")


            if len(code_section) == 0:
                print("\t!! NO CODE FOR BUILD, BUILDING RAW ROMFS!")
            else:
                print("\tChecking and fixing any build header values.")

                struct.pack_into(
                    endian + "II",
                    code_section,
                    0x08,
                    0x00000000,
                   int(((build_info["romfs_address"] + 8) - build_info["build_address"]) / 4)
                )

                code_checksum = romfs_implode.checksum(code_section)

                struct.pack_into(
                    endian + "I",
                    code_section,
                    0x08,
                    code_checksum
                )

                struct.pack_into(
                    endian + "I",
                    code_section,
                    0x24,
                    build_info["romfs_address"] + 8
                )


        romfs_blob = bytearray(romfs_size + extra_alloc_bytes)
        _build_romfs(romfs_nodes)

        if box_build:
            print("\tCalculating ROMFS size and checksum.")

            dword_romfs_size = ctypes.c_uint32(int(romfs_size / 4)).value
            romfs_checksum = romfs_implode.checksum(romfs_blob)

            struct.pack_into(
                endian + "II",
                romfs_blob,
                romfs_size,
                dword_romfs_size,
                romfs_checksum
            )

            if len(next_romfs) != 0:
                next_link_offset = (romfs_size - 0x38)

                romfs_blob[next_link_offset+0] = next_romfs[0]
                romfs_blob[next_link_offset+1] = next_romfs[1]
                romfs_blob[next_link_offset+2] = next_romfs[2]
                romfs_blob[next_link_offset+3] = next_romfs[3]

        print("\tDone building ROMFS.")

        if box_build:
            print("\tRebulding ROM file.")

            build_blob = code_section + code_romfs_padding + romfs_blob + footer_section

            if len(build_blob) > 0x800000:
                print("\t!! Build over 8MB.  May not work!")


            return build_blob
        else:
            return romfs_blob

    def pack(origin, source_build_path = None, out_path = None, romfs_type = None, build_info = None):
        descriptor_table_path = origin + "/dt.json"

        descriptor_table = None

        if build_info == None and source_build_path != None:
            build_info = build_meta.detect(source_build_path)

        if os.path.isfile(descriptor_table_path):
            descriptor_table = json.loads(romfs_implode.get_file_data(descriptor_table_path).decode())

            if build_info == None and "build_info" in descriptor_table:
                build_info = descriptor_table["build_info"]

        if build_info != None:
            if romfs_type != None:
                build_info["romfs_type"] = romfs_type
            elif build_info["romfs_type"] != None:
                build_info["romfs_type"] = ROMFS_TYPE(build_info["romfs_type"])

            if source_build_path != None:
                build_info["source_build_path"] = source_build_path
            elif build_info["path"] != None:
                build_info["source_build_path"] = build_info["path"]

            if out_path != None:
                build_info["out_path"] = out_path
            elif build_info["path"] != None:
                build_info["out_path"] = build_info["path"]
            elif build_info["source_build_path"] != None:
                build_info["out_path"] = build_info["source_build_path"]

            build_meta.print_build_info(build_info)

            if build_info["romfs_type"] == ROMFS_TYPE.VIEWER_SCRAMBLED:
                romfs_implode.scrample_romfs_file(build_info, romfs_implode.build_romfs(origin, build_info, descriptor_table))
            elif build_info["romfs_type"] == ROMFS_TYPE.BOX:
                romfs_implode.write_romfs_file(build_info, romfs_implode.build_romfs(origin, build_info, descriptor_table))
                pass
            else:
                romfs_implode.write_romfs_file(build_info, romfs_implode.build_romfs(origin, build_info, descriptor_table))
        else:
            print("Build info not found.  Need valid descriptor '" + origin + "/dt.json' file or valid approm '" + source_build_path + "' file.  I don't know how and what to build?")
