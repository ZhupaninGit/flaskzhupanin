from http.server import HTTPServer,CGIHTTPRequestHandler

serversocket = ('127.0.0.1',9999)

https = HTTPServer(serversocket,CGIHTTPRequestHandler)

https.serve_forever()
print("Сервер запущено.")

