import os
import random
import signal
import sys

import Ice
import vlc

Ice.loadSlice('../SOUP/MusiqueReceiver.ice')
import SOUP


class MusiqueReceiverI(SOUP.MusiqueReceiver):
    # Path to your media file
    media_file_path = "../styles/"

    media = None

    def __init__(self, styleName):
        self.media_file_path += styleName

        # Creating a VLC instance
        self.instance = vlc.Instance("--no-video")

        # Creating a media player
        self.player = self.instance.media_player_new()

    def getSongs(self, current):
        list = os.listdir('./')
        retList = []
        for object in list:
            if not object.__contains__(".py"):
                retList.append(object)
        return retList

    def select(self, songName, current):

        # Creating a media object
        self.media = self.instance.media_new(self.media_file_path + songName)

        # Setting up the media player with the media object
        self.player.set_media(self.media)
        self.player.audio_set_volume(100)

    def play(self, current):
        if self.media != None:
            # Starting the broadcasting
            # Specify your desired IP and port for broadcasting
            # Here, we are using UDP for broadcasting
            self.player.play()

    def pause(self, current):
        if self.media != None:
            # Stopping the media player
            self.player.stop()

    def stop(self, current):
        if self.media != None:
            # Stopping the media player
            self.player.stop()
            self.media = None



        # # Create a new vlm object
        # vlm = instance.vlm_add_broadcast("MyBroadcast", media_file_path,
        #                                  ":sout=#duplicate{dst=std{access=udp,mux=ts,dst=239.255.0.1:1234}}", 0, [],
        #                                  True, False)
        #
        # # Wait for the broadcast to finish
        # input("Press any key to stop the broadcast...\n")
        #
        # # Stopping the broadcast
        # instance.vlm_del_media("MyBroadcast")

class ServerTemplate:

    port = "10000"

    def __init__(self, port = "10000", styleName = ""):
        self.port = port
        self.styleName = styleName

    def start(self, communicator):
        #
        # Install a signal handler to shutdown the communicator on Ctrl-C
        #
        adapter = communicator.createObjectAdapterWithEndpoints("MusiqueReceiver", "default -h localhost -p " + self.port)
        adapter.add(MusiqueReceiverI(self.styleName), Ice.stringToIdentity("musiqueReceiver"))
        adapter.activate()
        communicator.waitForShutdown()

    def listen(self, ):
        #
        # Ice.initialize returns an initialized Ice communicator,
        # the communicator is destroyed once it goes out of scope.
        #
        with Ice.initialize(sys.argv) as communicator:
            signal.signal(signal.SIGINT, lambda signum, frame: communicator.shutdown())
            if hasattr(signal, 'SIGBREAK'):
                signal.signal(signal.SIGBREAK, lambda signum, frame: communicator.shutdown())
            self.start(communicator)




if __name__ == '__main__':
    clientTest = ServerTemplate("5000")
    clientTest.listen()
