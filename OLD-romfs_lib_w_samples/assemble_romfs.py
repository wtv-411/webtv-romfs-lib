import argparse
import os
from lib.romfs_type import *
from lib.romfs_implode import *

# (C) WebTV Wiki Crew 2021
# Wrapper of eMac's "romfs_implode" functions in his ROMFS library
# Currently only supports building ROMFS data into Viewer (1.x/scrambled) and Dreamcast formats

def main():
	arg_parser = argparse.ArgumentParser(prog="assemble_romfs", description="Builds a ROMFS container image with files from a specified source directory.", formatter_class=argparse.RawTextHelpFormatter)
	arg_parser.add_argument('directory', help='Source directory with ROMFS files.')
	arg_parser.add_argument('type', help='''Type of ROMFS file to build.

Supported types:
  viewer - WebTV Viewer 1.x format
  viewer-scrambled - WebTV/MSN TV Viewer 2.x format (scrambled)
  dreamcast - Dreamcast format (little-endian)
  ''')
	arg_parser.add_argument('target_romfs_file', help='Destination file to write ROMFS data to.')
	args = arg_parser.parse_args()
	
	# Check if directory exists and isn't empty
	if not os.path.isdir(args.directory) or os.listdir(args.directory) == 0:
		print("Source directory doesn't exist or has no content. Terminating.")
		return
	
	romfs_info = determine_romfs_type(args.type.lower(), args.target_romfs_file)
	if romfs_info is None:
		print('ROMFS type "{}" is invalid.'.format(args.type))
		return
	
	romfs_implode.pack(args.directory, romfs_info) # Do actual packing

def determine_romfs_type(type_string, rom_name):
	# Determine ROMFS type from string, return appropriate ROMFS info object (or none if type is unsupported/invalid)
	
	if type_string == 'viewer':
		return romfs_sniff.define(rom_name, ROMFS_TYPE.VIEWER, 0, 0, 0x80800000)
	elif type_string == 'viewer-scrambled':
		return romfs_sniff.define(rom_name, ROMFS_TYPE.VIEWER_SCRAMBLED, 0, 0, 0x80800000)
	elif type_string == 'dreamcast':
		return romfs_sniff.define(rom_name, ROMFS_TYPE.DREAMCAST)
	else:
		return None

if __name__ == '__main__':
	main()