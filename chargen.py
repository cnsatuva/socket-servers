import socket
import threading
import SocketServer
import sys

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    ascii = ''.join([chr(i) for i in xrange(0x21, 0x7f)])*2

    def handle(self):
        try:
            while True:
                for i in xrange(len(self.ascii)/2):
                    self.request.sendall(self.ascii[i:i+72]+'\n')
        except:
            pass

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0
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
