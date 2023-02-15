from lib.build_meta import *
from lib.romfs_explode import *
from lib.romfs_implode import *
from lib.autodisk import *

def packd(directory_path, source_path, file_path):
    romfs_implode.pack(directory_path, source_path, file_path)

def pack(directory_path, ROMFS_TYPE = ROMFS_TYPE.VIEWER):
    romfs_implode.pack(directory_path, None, None, None)

def list(file_path):
    romfs_explode.list(file_path)

def unpack(file_path, destination = "out", use_minibrowser = True):
    romfs_explode.unpack(file_path, destination, True, "processed-out.bin", use_minibrowser)

def ad_list(file_path):
    autodisk.list(file_path)

def ad_unpack(file_path, destination = "out"):
    autodisk.unpack(file_path, destination)


######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################

# Step 1: Dump approm 'approm.o' ROMFS into './approm'
unpack("approm.o", "approm")

# Step 2: Edit or add files in dir './approm'.  Keep in mind the ROMFS size is limited.
#	You can change dt.json "compression_strategy" to "best" to test lzss and lzpf to auto-choose the best compression per file.  See comments in unpack() from lin/romfs_explode.py for more details.

# Step 3: Build approm 'approm-mod.o' based on the original approm 'approm.o' using files in ./approm
#packd("./approm", "approm.o", "approm-mod.o")

# Step 4: install onto box.

# This can be used for any build.
