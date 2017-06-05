import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import face_recognizer as fd
import iot as txt
from urlparse import urlparse
import json
import os


dirname = '../data/images/'
clients = []
names = ["Greg", "Shlok"]

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		parsed_origin = urlparse(origin)

		# some restrictions on origin, ip included for testing
		return True
	
	def open(self):
		print("WebSocket opened")
		clients.append(self)

	def on_message(self, message):

		data = json.loads(message)

	def on_close(self):
		print("WebSocket closed")
		clients.remove(self)


class MainHandler(tornado.web.RequestHandler):
	def post(self):

		if self.request.headers["Content-Type"]=='image/bin':
			image = self.request.body
			print "Received image"

			with open(os.path.join(dirname, 'face.jpg'), 'wb') as f:
				f.write(image)
		
			path = dirname+'face.jpg'
			name = fd.run_recognizer(path, names)
			if name is None:
				print "no face found"
				self.write("access=false")

			else:
				print(name)
				contact = txt.getContacts(name)			
				print(contact)

				if contact is None:
					self.write("access=false")
				else:
					txt.contact(txt.getContacts(name), 'http://13.58.38.35/images/face.jpg')
					self.write("access=true")
		
			update_clients()

		else:
			print(self.request.headers)
			#print(self.request.body)
	get = post
	

def update_clients():
	for client in clients:
		client.write_message(".")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
		(r"/socket", WebSocketHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
