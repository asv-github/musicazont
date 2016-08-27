#!/usr/bin/env python3
"""
obtainer.py
Methods for obtaining a video from a query, be it by downloading with youtube-dl or just using the cache
"""
from subprocess import call, check_output
import os, os.path, glob

def obtain(query, cachedir="/tmp"):
	"""
	Given a query, obtains a youtube video and returns a path to it.
	To save time, keep previously downloaded videos in a cache directory and don't redownload a video if we already have it.
	This method takes some care to handle an edge case where youtube-dl reports one filename but the actual file has a different extension. (This happens if, for instance, downloaded ogg audio and mp4 video get merged into an mkv file.)
	"""
	os.chdir(cachedir)
	filename = check_output(["youtube-dl","--no-playlist","--get-filename","--restrict-filenames","--",query],universal_newlines=True).strip()
	basename, ext = os.path.splitext(filename)
	if os.path.isfile(filename) or os.path.isfile(basename + ".mkv"):
		# Cache hit! We already have this video. \(^_^)/
		return os.path.abspath(filename_with_correct_extension(filename))
	else:
		# Cache miss, have to download the video.
		call(["youtube-dl","--no-playlist","--restrict-filenames","--merge-output-format","mkv","--",query])
		return os.path.abspath(filename_with_correct_extension(filename))
	# There is a race condition here: the downloaded file could have a different filename if a video gets uploaded or taken down between the first and second invocations, changing the search results.
	# If this ever causes a problem in practice I'll give you a dollar.


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


if __name__ == "__main__":
	query = input("Youtube search query: ")
	print(obtain(query))
