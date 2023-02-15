import argparse
import os
from lib.romfs_explode import *

# (C) WebTV Wiki Crew 2021
# Simple wrapper for romfs_explode library

def main():
	arg_parser = argparse.ArgumentParser(prog="extract_romfs", description="Extracts files from ROMFS containers in WebTV/MSN TV ROM images.")
	arg_parser.add_argument('file', help='ROM image to extract ROMFS data from.')
	arg_parser.add_argument('-d', '--destination', help='Destination folder to extract ROMFS data to. Default name of this directory is "out".', default='out')
	args = arg_parser.parse_args()
	
	# Check if file exists before continuing
	if not os.path.isfile(args.file):
		print("File specified does not exist. Terminating.")
		return
	
	romfs_explode.unpack(args.file, args.destination, "processed-out.bin", True) # Not sure what "processed-out.bin" is used for yet. Keep an eye out on that.
	print('\nDone extracting ROMFS! Make sure to take note of the ROMFS type shown earlier if you want to rebuild the extracted files into the same type.')

if __name__ == '__main__':
	main()