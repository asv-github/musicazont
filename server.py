import http.server, cgi
import concurrent.futures
import time
from obtainer import obtain
from subprocess import call

def enqueue(query):
	# For now, there is no queue. Just play!
	filename = obtain(query)
	call(["mplayer","-fs","--",filename])

class MusicazontRequestHandler(http.server.BaseHTTPRequestHandler):
	def reply(self,string):
		self.wfile.write(string.encode('utf-8'))

	def do_GET(self):
		# Send a static page
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.end_headers()
		self.reply(get_page)

	def do_POST(self):
		# Send a static page, but in parallel enqueue the video
		executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
		form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
		query = form.getvalue('q')
		executor.submit(enqueue, query)
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.end_headers()
		self.reply(post_page)

if __name__ == "__main__":
	with open('get.html','r') as f:
		get_page = f.read()
	with open('post.html','r') as f:
		post_page = f.read()
	httpd = http.server.HTTPServer(('',8080), MusicazontRequestHandler)
	httpd.serve_forever()
