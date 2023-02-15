import os
import sys
import struct
import math
import tempfile
import shutil
import zlib
import json
from lib.lzpf import *
from lib.lzss import *
from lib.build_meta import *

class romfs_explode():
    def read_node(f, build_info, address, read_data = True):
        position = build_meta.position(build_info, address)

        f.seek(position)

        file_info = [0, 0, 0, 0, 0, 0, ""]

        if build_info["romfs_type"] == ROMFS_TYPE.DREAMCAST:
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

        file_position = build_meta.position(build_info, file_info[3])
        data_size = file_info[4]
        compression_type = FILE_COMPRESSION.UNKNOWN
        compressed_size = -1

        if read_data and file_type == OBJECT_TYPE.FILE and file_info[3] > 0 and file_info[4] > 0 and file_position > 0:
            f.seek(file_position)

            if build_info["romfs_type"] == ROMFS_TYPE.BOX and (data_size & 0xF0000000) != 0:
                size_param = data_size
                compressed_size = data_size - (data_size & 0xFF000000)

                data = bytes(f.read(compressed_size))

                data_size = int.from_bytes(bytes(data[0:4]), "big")

                compressed_size -= 4

                if (size_param & 0x90000000) == 0x90000000:
                    compression_type = FILE_COMPRESSION.LZSS

                    d = lzss()
                    data = d.Lzss_Expand(data[4:], data_size)

                    data_size = len(data)
                elif (size_param & 0x80000000) == 0x80000000:
                    compression_type = FILE_COMPRESSION.LZPF

                    d = lzpf()
                    data = d.Lzpf_Expand(data[4:])

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

    def walk_romfs(f, build_info, address, parent_address, is_base = False, read_data = True):
        items = []

        while address != 0:
            file_info = romfs_explode.read_node(f, build_info, address, read_data)

            if file_info["parent"] == parent_address:
                items.append(file_info)

                if file_info["child_list"] != 0:
                    file_info["children"] = romfs_explode.walk_romfs(f, build_info, file_info["child_list"], address, False, read_data)

            if is_base:
                address = 0
            else:
                address = file_info["next_link"]

        return items

    def process_romfs(build_info, read_data = True, secondary_copy_path = "", use_minibrowser = False):
        romfs_nodes = []

        allowable_types = [
            ROMFS_TYPE.VIEWER,
            ROMFS_TYPE.BOX,
            ROMFS_TYPE.DREAMCAST
        ]

        if build_info["romfs_type"] == ROMFS_TYPE.BUILD_BUGGED:
            print("!! Bugged approm file.  Please re-run parts through the new decompressTool!")

            return None

        if build_info["romfs_type"] == ROMFS_TYPE.COMPRESSED_BOX:
            build_info = build_matryoshka.expand_build(build_info)
            build_meta.print_build_info(build_info, "\tNew Type: ")

        if build_info["romfs_type"] == ROMFS_TYPE.VIEWER_SCRAMBLED:
            build_info = romfs_cipher.unscramble_vwr_file(build_info)
            build_meta.print_build_info(build_info, "\tNew Type: ")

        if use_minibrowser and build_info["minibrowser_offset"] > 0:
            build_info = build_matryoshka.expand_minibrowser(build_info)
            build_meta.print_build_info(build_info, "\tNew Type: ")

        if build_info["romfs_type"] in allowable_types:
            romfs_nodes = romfs_explode.get_nodes(build_info, read_data)
        else:
            print("\t!! Can't dump this ROMFS type!")

        if "is_secondary_image" in build_info.keys() and build_info["is_secondary_image"]:
            if secondary_copy_path != "":
                shutil.copyfile(build_info["path"], secondary_copy_path)

            os.remove(build_info["path"])

        return romfs_nodes


    def get_nodes(build_info, read_data = True):
        romfs_nodes = []

        with open(build_info["path"], "rb") as f:
            romfs_nodes = romfs_explode.walk_romfs(f, build_info, (build_info["romfs_address"] - (56 + 8)), 0x00000000, True, read_data)
            f.close()

        return romfs_nodes

    def walk_nodes(romfs_nodes, build_info, callback, path = "", depth = 0):
        if callback != None:
            for _romfs_nodes in romfs_nodes:
                node_path = path + "/" + _romfs_nodes["name"]

                romfs_node = {
                    "type": _romfs_nodes["type"],
                    "name": _romfs_nodes["name"],
                    "next_link": _romfs_nodes["next_link"],
                    "offset": _romfs_nodes["data_offset"],
                    "size": _romfs_nodes["data_size"],
                    "data": _romfs_nodes["data"],
                    "compression_type": _romfs_nodes["compression_type"],
                    "path": node_path,
                    "depth": depth
                }

                callback(romfs_node, build_info)

                if len(_romfs_nodes["children"]) > 0:
                    romfs_explode.walk_nodes(_romfs_nodes["children"], build_info, callback, node_path, depth + 1)
    
    def simplify_size(bytes):
        prefixes = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        size_e = int(math.floor(math.log(bytes, 1024)))
        simplified_size = round(bytes / math.pow(1024, size_e), 2)

        return str(simplified_size) + prefixes[size_e]

    def walk(origin, callback, read_data = True, secondary_copy_path = "", use_minibrowser = False):
        build_info = build_meta.detect(origin)
        build_meta.print_build_info(build_info)

        romfs_nodes = romfs_explode.process_romfs(build_info, read_data, secondary_copy_path, use_minibrowser)

        if romfs_nodes == None:
            return

        romfs_explode.walk_nodes(romfs_nodes, build_info, callback)

    def list(origin, simplify_sizes = False, read_data = False, secondary_copy_path = "", use_minibrowser = False):
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

        romfs_explode.walk(origin, _list, read_data, secondary_copy_path, use_minibrowser)

    def unpack(origin, destination = "./out", create_descriptor_file = True, secondary_copy_path = "", use_minibrowser = False):
        if not os.path.isdir(destination):
            os.mkdir(destination)

            if not os.path.isdir(destination):
                raise Exception("Destination doesn't exist")

        # compression_strategy:
        #   object-table-value: use compression_type value in object table, otherwise none (DEFAULT)
        #   best: try none, lzpf and lzss on all files and choose best.
        #   extension-list: use matched extension in compressed_extensions dictionary ({"txt": XXX, "gif": XXX}), otherwise none
        #   off: don't compress anything
        #
        # You can use  "dont_compress" array to block compression from a list of ROMFS file paths

        descriptor_table = {
            "build_info": {},
            "origin": origin,
            "destination": destination,
            "secondary_copy_path": secondary_copy_path,
            "use_minibrowser": use_minibrowser,
            "compression_strategy": "object-table-value",
            "object": {}
        }

        def _unpack(romfs_node, build_info):
            path = destination + "/" + romfs_node["path"]

            descriptor_table["build_info"] = build_info

            descriptor_table["object"][romfs_node["path"]] = {
                "type": romfs_node["type"],
                "name": romfs_node["name"],
                "offset": romfs_node["offset"],
                "next_link": romfs_node["next_link"],
                "size": romfs_node["size"],
                "compression_type": romfs_node["compression_type"],
                "depth": romfs_node["depth"]
            }

            compression = "UNKNOWN"
            if romfs_node["compression_type"] == FILE_COMPRESSION.LZPF:
                compression = "LZPF"
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

        romfs_explode.walk(origin, _unpack, True, secondary_copy_path, use_minibrowser)
        
        if create_descriptor_file:
            with open(destination + "/dt.json", "w") as f:
                f.write(json.dumps(descriptor_table, sort_keys=True, indent=4))
                f.close()
