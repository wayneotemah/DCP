from random import randint
import socket
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol

class Server (DatagramProtocol):
    def __init__(self) -> None:

        self.clients = set()
        print(socket.gethostbyname(socket.gethostname()))

        

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
    # reactor.listenUDP(port,Server())
    # reactor.run()

    portSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Make the port non-blocking and start it listening.
    portSocket.setblocking(False)
    portSocket.bind(("0.0.0.0", port))

    # Now pass the port file descriptor to the reactor.
    port = reactor.adoptDatagramPort(portSocket.fileno(), socket.AF_INET, Server())

    # The portSocket should be cleaned up by the process that creates it.
    portSocket.close()

    reactor.run()