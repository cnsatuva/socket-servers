import socket
import threading
import SocketServer
import sys
import random

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        magic = random.randint(1, 10000)
        while True:
            self.request.sendall("Guess the number [1-10000]: ")
            try:
                data = int(self.request.recv(10))
            except:
                self.request.sendall("Nope\n")
                break
            if data == magic:
                self.request.sendall("You got it!!\n")
                break
            else:
                if data > magic:
                    self.request.sendall("Too high\n")
                else:
                    self.request.sendall("Too low\n")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "0.0.0.0", 0
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    print "Server running on port:", port

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    server.shutdown()
    server.server_close()
