from random import randint
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol

class Server (DatagramProtocol):
    def __init__(self) -> None:
        self.clients = set()

    def datagramReceived(self, datagram: bytes, addr):
        '''
        received data from the client
        '''
        datagram = datagram.decode('utf-8')
        if datagram == "ready":
            addressList = "\n".join([str(x) for x in self.clients])
            self.transport.write(addressList.encode('utf-8'),addr)
            self.clients.add(addr)


if __name__ == "__main__":
    port = 9999
    reactor.listenUDP(port,Server())
    reactor.run()