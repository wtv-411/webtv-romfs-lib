import os
import sys
import struct
import math
import tempfile
import shutil
import zlib
from lib.lzpf import *
from lib.lzss import *
from lib.lzj import *
from lib.romfs_type import *

class romfs_explode():
    def read_node(f, romfs_info, address):
        position = romfs_sniff.position(romfs_info, address)

        f.seek(position)

        file_info = [0, 0, 0, 0, 0, 0, ""]

        if romfs_info["type"] == ROMFS_TYPE.DREAMCAST:
            file_info = struct.unpack_from("<IIIIIII28s", bytes(f.read(56)))
        else:
            file_info = struct.unpack_from(">IIIIIII28s", bytes(f.read(56)))

        file_type = OBJECT_TYPE.UNKNOWN
        if file_info[3] == 0 and file_info[4] == 0 and file_info[6] == 0:
            file_type = OBJECT_TYPE.DIRECTORY
        else: 
            file_type = OBJECT_TYPE.FILE

        name = str(file_info[7][0:file_info[7].index(b'\x00')], "ascii", "ignore")

        data = b''

        file_position = 0
        data_size = file_info[4]
        compression_type = FILE_COMPRESSION.UNKNOWN
        compressed_size = -1

        if file_type == OBJECT_TYPE.FILE and file_info[3] > 0 and file_info[4] > 0:
            file_position = romfs_sniff.position(romfs_info, file_info[3])

            f.seek(file_position)

            if romfs_info["type"] == ROMFS_TYPE.BOX and (data_size & 0xF0000000) != 0:
                size_param = data_size
                compressed_size = data_size - (data_size & 0xFF000000)

                data = bytes(f.read(compressed_size))

                data_size = int.from_bytes(bytes(data[0:4]), "big")

                compressed_size -= 4

                if (size_param & 0x90000000) == 0x90000000:
                    compression_type = FILE_COMPRESSION.LZSS

                    data = lzss.ExpandLzss(data[4:], data_size)

                    data_size = len(data)
                elif (size_param & 0x80000000) == 0x80000000:
                    compression_type = FILE_COMPRESSION.LZFP

                    c = lzpf()
                    data = c.Lzpf_Expand(data[4:])

                    data_size = len(data)
            else:
                data_size -= (data_size & 0xFF000000)

                compression_type = FILE_COMPRESSION.NONE
                compressed_size = -1
                data = bytes(f.read(data_size))

        return {
            "address": address,
            "position": position,
            "type": file_type,
            "next_link": file_info[0],
            "parent": file_info[1],
            "child_list": file_info[2],
            "data_address": file_info[3],
            "reserve": file_info[5],
            "data_checksum": file_info[6],
            "compression_type": compression_type,
            "compressed_size": compressed_size,
            "data_offset": file_position,
            "data_size": data_size,
            "data": data,
            "name": name,
            "children": []
        }

    def walk_romfs(f, romfs_info, address):
        items = []

        is_base = False
        if address == romfs_info["romfs_address"]:
            is_base = True
            address -= 56 + 8

        while address != 0:
            file_info = romfs_explode.read_node(f, romfs_info, address)

            if file_info["child_list"] != 0:
                file_info["children"] = romfs_explode.walk_romfs(f, romfs_info, file_info["child_list"])

            items.append(file_info)

            if is_base:
                address = 0
            else:
                address = file_info["next_link"]

        return items

    def unscramble_vwr_file(romfs_info):
        td, tmp_path = tempfile.mkstemp()

        print("\tUnscrambling vwr file...")

        with os.fdopen(td, "wb") as t:
            with open(romfs_info["path"], "rb") as f:
                f.seek(0, os.SEEK_END)
                file_size = f.tell()

                current_position = 0
                while (file_size - current_position) > 8:
                    f.seek(current_position)

                    t.write(romfs_sniff.unscramble(f.read(8)))

                    current_position += 8

                    print("\r\t\t" + str(int((current_position / file_size) * 100)) + "%", end='', flush=True)

                f.seek(current_position)
                t.write(f.read(8))

                f.close()
            t.close()

        new_romfs_info = romfs_sniff.detect(tmp_path)

        new_romfs_info["original_path"] = romfs_info["path"]

        print("\r\tDone unscrambling vwr file!", flush=True)
        
        return new_romfs_info

    def expand_minibrowser(romfs_info):
        LZSS_START = b'\x10\x00\x00'

        td, tmp_path = tempfile.mkstemp()

        print("\tExpanding minibrowser...")

        if romfs_info["minibrowser_offset"] > 0:
            with os.fdopen(td, "wb") as t:
                with open(romfs_info["path"], "rb") as f:
                    f.seek(0, os.SEEK_END)
                    file_size = f.tell()

                    f.seek(romfs_info["minibrowser_offset"])
                    data = f.read(file_size - romfs_info["minibrowser_offset"])

                    if data[1:4] == LZSS_START:
                        t.write(lzss.ExpandLzss(data, 0x1c0000))
                    else:
                        t.write(lzj.ExpandLzj(data))

                    f.close()
                t.close()

            new_romfs_info = romfs_sniff.detect(tmp_path)

            new_romfs_info["original_path"] = romfs_info["path"]

            print("\tDone expanding minibrowser!")

            return new_romfs_info
        else:
            print("No minibrowser found")

            return romfs_info

    def expand_build(romfs_info):
        td, tmp_path = tempfile.mkstemp()

        print("\tExpanding build...")

        with os.fdopen(td, "wb") as t:
            with open(romfs_info["path"], "rb") as f:
                f.seek(0, os.SEEK_END)
                file_size = f.tell()

                f.seek(0x28)
                lzj_version = int.from_bytes(bytes(f.read(4)), "big")

                f.seek(0x200)
                data = f.read(file_size)

                t.write(lzj.ExpandLzj(data, LZJ_VERSION(lzj_version)))

                f.close()
            t.close()

            new_romfs_info = romfs_sniff.detect(tmp_path)

            new_romfs_info["original_path"] = romfs_info["path"]

            print("\n\tDone expanding build!")

            return new_romfs_info


    def process_romfs(romfs_info, secondary_copy_path = "", use_minibrowser = False):
        romfs_nodes = []

        using_secondary_image = False

        allowable_types = [
            ROMFS_TYPE.VIEWER,
            ROMFS_TYPE.BOX,
            ROMFS_TYPE.DREAMCAST
        ]

        if romfs_info["type"] == ROMFS_TYPE.BUILD_BUGGED:
            print("Bugged approm file.")

            return None

        if romfs_info["type"] == ROMFS_TYPE.COMPRESSED_BOX:
            romfs_info = romfs_explode.expand_build(romfs_info)
            romfs_sniff.print_romfs_info(romfs_info, "\tNew Type: ")

        if romfs_info["type"] == ROMFS_TYPE.VIEWER_SCRAMBLED:
            using_secondary_image = True
            romfs_info = romfs_explode.unscramble_vwr_file(romfs_info)
            romfs_sniff.print_romfs_info(romfs_info, "\tNew Type: ")

        if use_minibrowser and romfs_info["minibrowser_offset"] > 0:
            using_secondary_image = True
            romfs_info = romfs_explode.expand_minibrowser(romfs_info)
            romfs_sniff.print_romfs_info(romfs_info, "\tNew Type: ")

        if romfs_info["type"] in allowable_types:
            romfs_nodes = romfs_explode.get_nodes(romfs_info)
        else:
            print("\tCan't dump this ROMFS type!")

        if using_secondary_image:
            if secondary_copy_path != "":
                shutil.copyfile(romfs_info["path"], secondary_copy_path)

            os.remove(romfs_info["path"])

        return romfs_nodes


    def get_nodes(romfs_info):
        romfs_nodes = []

        with open(romfs_info["path"], "rb") as f:
            romfs_nodes = romfs_explode.walk_romfs(f, romfs_info, romfs_info["romfs_address"])
            f.close()

        return romfs_nodes

    def walk_nodes(romfs_nodes, callback, path = "", depth = 0):
        if callback != None:
            for _romfs_nodes in romfs_nodes:
                node_path = path + "/" + _romfs_nodes["name"]

                romfs_node = {
                    "type": _romfs_nodes["type"],
                    "name": _romfs_nodes["name"],
                    "offset": _romfs_nodes["data_offset"],
                    "size": _romfs_nodes["data_size"],
                    "data": _romfs_nodes["data"],
                    "compression_type": _romfs_nodes["compression_type"],
                    "path": node_path,
                    "depth": depth
                }

                callback(romfs_node)

                if len(_romfs_nodes["children"]) > 0:
                    romfs_explode.walk_nodes(_romfs_nodes["children"], callback, node_path, depth + 1)
    
    def simplify_size(bytes):
        prefixes = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        size_e = int(math.floor(math.log(bytes, 1024)))
        simplified_size = round(bytes / math.pow(1024, size_e), 2)

        return str(simplified_size) + prefixes[size_e]

    def list(origin, simplify_sizes = False, secondary_copy_path = "", use_minibrowser = False):
        romfs_info = romfs_sniff.detect(origin)
        romfs_sniff.print_romfs_info(romfs_info)

        romfs_nodes = romfs_explode.process_romfs(romfs_info, secondary_copy_path, use_minibrowser)

        if romfs_nodes == None:
            return

        last_offset = 0

        def _list(romfs_node):
            nonlocal last_offset
            if romfs_node["type"] == OBJECT_TYPE.DIRECTORY:
                print(("\t" * romfs_node["depth"]) + romfs_node["name"] + "/")
            else:
                size = "0B"
                if simplify_sizes:
                    size = romfs_explode.simplify_size(romfs_node["size"])
                else:
                    size = str(romfs_node["size"]) + "B"

                print(("\t" * romfs_node["depth"]) + romfs_node["name"] + "\t(" + size + ")")
                last_offset = romfs_node["offset"]

        romfs_explode.walk_nodes(romfs_nodes, _list)
        
    def unpack(origin, destination = "./out", secondary_copy_path = "", use_minibrowser = False):
        romfs_info = romfs_sniff.detect(origin)
        romfs_sniff.print_romfs_info(romfs_info)

        if not os.path.isdir(destination):
            os.mkdir(destination)

            if not os.path.isdir(destination):
                raise Exception("Destination doesn't exist")

        romfs_nodes = romfs_explode.process_romfs(romfs_info, secondary_copy_path, use_minibrowser)
        
        if romfs_nodes == None:
            return

        def _unpack(romfs_node):
            path = destination + "/" + romfs_node["path"]

            compression = "UNKNOWN"
            if romfs_node["compression_type"] == FILE_COMPRESSION.LZFP:
                compression = "LZFP"
            elif romfs_node["compression_type"] == FILE_COMPRESSION.LZSS:
                compression = "LZSS"
            else:
                compression = "NONE"

            print("\tUnpack[" + compression + "]: " + romfs_node["path"])

            if romfs_node["type"] == OBJECT_TYPE.DIRECTORY:
                if not os.path.isdir(path):
                    os.mkdir(path)
            else:
                with open(path, "wb") as f:
                    f.write(romfs_node["data"])
                    f.close()

        romfs_explode.walk_nodes(romfs_nodes, _unpack)
