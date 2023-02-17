from random import randint
import socket
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
import json

import json

class MultiDimensionalArrayEncoder(json.JSONEncoder):
    def encode(self, obj):
        def hint_tuples(item):
            if isinstance(item, tuple):
                return {'items': item}
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            if isinstance(item, dict):
                return {key: hint_tuples(value) for key, value in item.items()}
            else:
                return item

        return super(MultiDimensionalArrayEncoder, self).encode(hint_tuples(obj))

def hinted_tuple_hook(obj):
    if '__tuple__' in obj:
        return tuple(obj['items'])
    else:
        return obj


class Server (DatagramProtocol):
    def __init__(self) -> None:

        self.clients = []
        print(socket.gethostbyname(socket.gethostname()))

        

    def datagramReceived(self, datagram: bytes, addr):
        '''
        received data from the client
        '''
        client = socket.gethostbyaddr(addr[0])
        print(f'{client[0]} has connected on {client[-1][0]} -p {addr[1]}')

        client_address = client[0],client[-1][0],addr[1]
        
        datagram = datagram.decode('utf-8')
        if datagram == "ready":
            print(self.clients)
            found = False
            for index,element in enumerate(self.clients):
                if client[0] == element[0]:
                    self.clients.remove(self.clients[index])
                    self.clients.append(client_address)
                    found = True
                    break
            if not found:
                self.clients.append(client_address)
            
            enc = MultiDimensionalArrayEncoder()
            address_list = enc.encode(self.clients)

            self.transport.write(address_list.encode('utf-8'),addr)


if __name__ == "__main__":
    port = 9999
    portSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Make the port non-blocking and start it listening.
    portSocket.setblocking(False)
    portSocket.bind(("0.0.0.0", port))

    # Now pass the port file descriptor to the reactor.
    port = reactor.adoptDatagramPort(portSocket.fileno(), socket.AF_INET, Server())

    # The portSocket should be cleaned up by the process that creates it.
    portSocket.close()

    reactor.run()