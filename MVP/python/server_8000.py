#This is a wrapper of SimpleHTTPServer to add SVG image handling
#Author: Howard Webb
#Date: 7/5/2017
#NOTE: This needs to be started from the directory where your files to be served are located

#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import mimetypes

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

#Handler for SVG
Handler.extensions_map['.svg']='image/svg+xml'
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT

#Start the server running
httpd.serve_forever()
