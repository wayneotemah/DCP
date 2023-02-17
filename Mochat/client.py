import os
import socket
from random import randint
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
import json

import webbrowser

template = './templates/index.html'


class Client(DatagramProtocol):
    def __init__(self, host, port) -> None:
        # if host == "localhost":
        #     host = "127.0.0.1"
        self.id = socket.gethostbyname((socket.gethostname())), port
        self.address = None
        self.server = "192.168.1.207", 9999
        print(f'working on ip {self.id}')

    def startProtocol(self):
        ''''
        run after the initalization, will connect to server 
        '''
        # webbrowser.open_new(template)
        self.transport.write('ready'.encode('utf-8'), self.server)

    def datagramReceived(self, datagram: bytes, addr):
        '''
        called when  data is received
        '''

        datagram = datagram.decode('utf-8')
        print('\n', datagram, "###########################\n")
        datagram = json.loads(datagram)

        if addr == self.server:
            print(f'Users: {datagram}')
            num = input('choose clients:')

            while not num.isnumeric() and not -1 <= int(num) >= len(datagram):
                num = input('choose clients:')

            num = int(num)
            client = datagram[num-1]["items"]

            self.address = client[1], client[2]
            reactor.callInThread(self.send_message)

    def send_message(self):
        while True:
            data = input(":::")
            self.transport.write(data.encode("utf-8"), self.address)


if __name__ == "__main__":
    port = randint(1000, 4999)
    reactor.listenUDP(port, Client('localhost', port))
    reactor.run()
