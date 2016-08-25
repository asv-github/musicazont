#!/usr/bin/env python3
"""
obtainer.py
Methods for obtaining a video from a query, be it by downloading with youtube-dl or just using the cache
"""
from subprocess import call, check_output
import os, os.path, glob

def filename_with_correct_extension(filename):
	"""
	youtube-dl gives us a filename it says it will download to. The actual filename may have a different extension.
	For instance, an ogg and an mp4 may get merged into an mkv.
	This method checks whether this happened and returns the actual filename. Returns None if file doesn't exist.
	"""
	os.chdir("/tmp")
	basename, ext = os.path.splitext(filename)
	if os.path.isfile(filename): return filename
	elif os.path.isfile(basename + ".mkv"): return basename + ".mkv" # To simplify, we tell youtube-dl that if it merges formats it should merge to an mkv
	else: return None

def obtain(query):
	os.chdir("/tmp")
	filename = check_output(["youtube-dl","--get-filename","--restrict-filenames","--",query],universal_newlines=True).strip()
	print("Filename would be \"{}\"".format(filename))
	# Sometimes the actual downloaded file will have a different extension -- e.g, ogg and mp4 get merged into an mkv.
	# We must be careful to handle this case.
	basename, ext = os.path.splitext(filename)

	# Is it in the cache?
	if os.path.isfile(filename) or os.path.isfile(basename + ".mkv"):
		print("Cache hit! \(^_^)/")
		return os.path.abspath(filename_with_correct_extension(basename + ".mkv"))
	else:
		print("Cache miss, downloading now")
		call(["youtube-dl","--restrict-filenames","--merge-output-format","mkv","--",query])
		return os.path.abspath(filename_with_correct_extension(filename))
	# There is a race condition here: the downloaded file could have a different filename if a video gets uploaded or taken down between the first and second invocations, changing the search results.
	# If this ever causes a problem in practice I'll give you a dollar.

if __name__ == "__main__":
	query = input("Youtube search query: ")
	print(obtain(query))
