import signal
import sys

import Ice

Ice.loadSlice('../SOUP/MusiqueReceiver.ice')
import SOUP


# class MusiqueReceiverI(SOUP.MusiqueReceiver):
#
#     def __init__(self, registry):
#         self.registry = registry
#
#     def addClient(self, adress, port, current):
#
#
#     def getSongs(self, current):
#
#     def select(self, songName, current):
#
#     def play(self, current):
#
#     def pause(self, current):
#
#     def stop(self, current):
#
class ClientTemplate:
    port = "5000"
    adress = "localhost"

    def __init__(self, adress, port, communicator):
        proxy = communicator.stringToProxy("musiqueSender:default -h " + adress + " -p " + port)
        self.musiqueSender = SOUP.MusiqueSenderPrx.checkedCast(proxy)
        print("connected")

class ServerTemplate:
    port = "5000"
    address = "localhost"

    def __init__(self, adress, port, communicator):
        proxy = communicator.stringToProxy("musiqueReceiver:default -h " + adress + " -p " + port)
        self.musiqueReceiver = SOUP.MusiqueReceiverPrx.checkedCast(proxy)
        print("connected")


class registryImpl(SOUP.Registry):
    def __init__(self, communicator):
        self.allServers = []
        self.communicator = communicator

    def addServer(self, address, port, current):
        newServer = ServerTemplate(address, port, self.communicator)
        self.allServers.append((newServer.musiqueReceiver.getStyle(), newServer))
        print(self.allServers)

class registrySOUP:

    port = "4000"
    adress = "localhost"

    def __init__(self, adress = "localhost", port = "4000"):
        self.communicator = Ice.initialize(sys.argv)
        self.adress = adress
        self.port = port



    def start(self):
        #
        # Install a signal handler to shutdown the communicator on Ctrl-C
        #
        adapter = self.communicator.createObjectAdapterWithEndpoints("registry", "default -h " + self.adress + " -p " + self.port)
        adapter.add(registryImpl(self.communicator), Ice.stringToIdentity("registry"))
        adapter.activate()
        print("server UP")

    def listen(self, ):
        #
        # Ice.initialize returns an initialized Ice communicator,
        # the communicator is destroyed once it goes out of scope.
        #
            signal.signal(signal.SIGINT, lambda signum, frame: self.communicator.shutdown())
            if hasattr(signal, 'SIGBREAK'):
                signal.signal(signal.SIGBREAK, lambda signum, frame: self.communicator.shutdown())
            self.start()
            self.communicator.waitForShutdown()

if __name__ == '__main__':

    myRegistry = registrySOUP()
    myRegistry.listen()


