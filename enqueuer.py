from concurrent.futures import ProcessPoolExecutor
from subprocess import call
from obtainer import obtain

"""
This is a dead-simple enqueuer.`It works by using a ThreadPoolExecutor with a single worker thread.
Videos are queued by submitting them to the executor. Two videos won't play at the same time because there's only one worker thread.
There's no guarantee, but things will probably get played in the order they get enqueued. If not, oh well.
See https://docs.python.org/dev/library/concurrent.futures.html for more info on ThreadPoolExecutors.
"""

def play(query):
	filename = obtain(query)
	call(["mplayer","-fs","--",filename])

def enqueue(query):
	""" Enqueues a video and returns immediately. """
	executor.submit(play, query)

executor = ProcessPoolExecutor(max_workers=1)
