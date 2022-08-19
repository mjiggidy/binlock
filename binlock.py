#!/usr/bin/env python3

"""
binlock.py
Create an Avid bin lock (.lck) file with a custom display name
By Michael Jordan <michael@glowingpixel.com>

Usage: binlock.py LockText path/to/output.lck
"""

import sys, pathlib

# Config
MAX_LENGTH = 255
FILE_EXTENSION = ".lck"
ALLOW_OVERWRITE = False

def format_lock_contents(name:str) -> bytes:
	"""Encode a given string into Avid lockfile contents"""
	
	if len(name) > MAX_LENGTH:
		raise ValueError(f"Lock name cannot exceed {MAX_LENGTH} characters")
	
	return name.ljust(MAX_LENGTH, '\0').encode("utf-16le")

def main(name:str, output:str) -> pathlib.Path:
	"""Create an Avid lockfile with a custom name"""

	# Create and validate the output path, ensuring we're using the correct file extension
	path_output = pathlib.Path(output).with_suffix(FILE_EXTENSION)
	
	if not path_output.parent.is_dir():
		raise FileNotFoundError("The given output path does not exist")
	elif path_output.exists() and not ALLOW_OVERWRITE:
		raise FileExistsError(f"A lock already exists at {path_output}")
	
	# Create the lockfile contents
	lock_bytes = format_lock_contents(name)
	
	# Write the lockfile contents to the output path
	with path_output.open('wb') as file_output:
		file_output.write(lock_bytes)
	
	return path_output

if __name__ == "__main__":

	if len(sys.argv) < 3:
		sys.exit(f"Usage: {__file__} LockText outputpath.lck")
	
	try:
		path_output = main(name=sys.argv[1], output=sys.argv[2])
	except Exception as e:
		sys.exit(f"Error creating lock file: {e}")
	else:
		print(f"Lock file written to {path_output}")
