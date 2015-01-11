import SocketServer
import os
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def serve_file(self, path, extension):
        file_content = open(path, "r")
        if extension == "css" or extension == "html":
            header = "HTTP/1.1 200 OK\r\n"
            header += "Content-Type: text/" + extension + "\r\n\r\n"
        else:
            header = "HTTP/1.1 200 OK\r\n\r\n"
        
        self.request.sendall(header + file_content.read())
        file_content.close()
        return

    def file_not_found(self):
        header = "HTTP/1.1 404 Not Found\r\n"
        header += "Content-Type: text/html\r\n\r\n"

        content = "<html><body>\n"
        content += "<h2>File not found</h2>\n"
        content += "This file does not exist :(\n"
        content += "</body></html>"

        self.request.sendall(header + content)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        request_data = self.data.split("\n")
        get_request = request_data[0].split(" ")
        file_request = get_request[1]

        if file_request[-1] == "/":
            file_request += "index.html"

        security_check = file_request.split("/")
        if ".." in security_check:
            self.file_not_found()
            return

        file_extension = file_request.split(".")[-1]
        file_path = os.getcwd() + "/www" + file_request
        if (os.path.isfile(file_path)):
            self.serve_file(file_path, file_extension)
            return
        else:
            self.file_not_found()
            return

        self.request.sendall(file_path)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
