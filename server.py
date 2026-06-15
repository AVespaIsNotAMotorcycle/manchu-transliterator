from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from ocr import NeuralNetwork

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    nn = NeuralNetwork()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(s):
        response_code = 200
        response = ""
        var_len = int(s.headers.get('Content-Length'))
        content = s.rfile.read(var_len);
        payload = json.loads(content);
        print(payload)

        s.send_header("Content-Type", "application/json")
        s.send_header("Access-Control-Allow-Origin", "*")
        s.end_headers()

        if payload.get('train'):
            try:
                nn.train(payload['trainArray'])
                nn.save()
            except Exception as inst:
                print(inst)
                response_code = 500
        elif payload.get('predict'):
            try:
                response = {
                    "type": "test",
                    "result": nn.predict(str(payload['image'])),
                }
            except Exception as inst:
                print(inst)
                response_code = 500
        else:
            response_code = 400
    
        s.send_response(response_code)
    
        if response:
            s.wfile.write(json.dumps(response))
        return

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

