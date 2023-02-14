import os
from random import randint
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol

import webbrowser

template = './templates/index.html'

class Client(DatagramProtocol):
    def __init__(self,host, port) -> None:
        if host == "localhost":
            host = "127.0.0.1"
        self.id = host, port
        self.address = None
        self.server = host, 9999
        print(f'working on ip {self.id}')
        webbrowser.open('file://' + os.path.realpath(template))


    def startProtocol(self):
        ''''
        run after the initalization, will connect to server 
        '''
        self.transport.write('ready'.encode('utf-8'),self.server)


    def  datagramReceived(self, datagram: bytes, addr):
        '''
        called when  data is received
        '''
        datagram = datagram.decode('utf-8')
        
        if addr == self.server:
            print('Choose to chat with any clinet from these\n',datagram)
            self.address = input('write host: '), int(input('write port:'))
            reactor.callInThread(self.send_message)
        else:
            print(f'{addr} send {datagram}')


    def send_message(self):
        while True:
            data = input(":::")
            self.transport.write(data.encode("utf-8"),self.address)


if __name__ == "__main__":
    port = randint(1000,4999)
    reactor.listenUDP(port,Client('localhost',port))
    reactor.run()