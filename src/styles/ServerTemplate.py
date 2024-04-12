import os
import signal
import sys

import mutagen
import Ice
import vlc

Ice.loadSlice('../SOUP/MusiqueReceiver.ice')
import SOUP


class MusiqueReceiverI(SOUP.MusiqueReceiver):
    # Path to your media file
    media_file_path = "../styles/"

    media = None


    def __init__(self, serverTemplate):
        self.media_file_path += serverTemplate.styleName
        self.communicator = serverTemplate.communicator
        self.template = None

        # Creating a VLC instance
        self.instance = vlc.Instance("--no-video")

        # Creating a media player
        self.player = self.instance.media_player_new()

    def addClient(self, adress, port, current):
        self.template = ClientTemplate(adress, port, self.communicator)

    def getSongs(self, current):
        retList = self.get_song_list()
        retString = ""
        for song in retList:
            retString += song + "\n"
        self.template.musiqueSender.responseGetSongs(retString)

    def getSongsByName(self, song_name: str, current):
        list = os.listdir('./')
        retList = ""
        for object in list:
            if not object.__contains__(".py") and not object.__contains__("__"):
                for song in os.listdir('./' + object + "/"):
                    if song.__contains__(".mp3") and song.__contains__(song_name):
                        retList += object + "/" + song + "\n"
        self.template.musiqueSender.responseGetSongs(retList)
    def getSongsByAuthor(self, author_name: str, current):
        list_dir = os.listdir('./')
        ret_list = ""

        for object in list_dir:
            if not object.endswith(".py") and not "__" in object:
                for song_file in os.listdir('./' + object + "/"):
                    if song_file.endswith(".mp3"):
                        song_path = './' + object + "/" + song_file
                        try:
                            audio = mutagen.File(song_path, easy=True)
                            print("artist name : ",audio['artist'][0])
                            if 'artist' in audio and audio['artist'][0] == author_name:
                                ret_list += object + "/" + song_file + "\n"
                        except Exception as e:
                            print(f"Error reading metadata for {song_file}: {e}")

        self.template.musiqueSender.responseGetSongs(ret_list)

    upload_completion: [bool]
    upload_data: [bytes]
    upload_song_name: str
    upload_style: str

    def prepareUpload(self, style: str, song_name: str, nb_blocs: int, current):
        print("preparing download")
        self.upload_style = style
        self.upload_song_name = song_name
        self.upload_completion = []
        self.upload_data = []
        for index in range(0,nb_blocs):
            self.upload_completion.append(False)
        print("download prepared " + str(nb_blocs) + " blocs")

    def upload(self, bloc_id: int, data: bytes, current):
        self.upload_data.append(data)
        self.upload_completion[bloc_id] = True
        self.template.musiqueSender.responseGetCompletion(self.upload_completion.count(True))

        if all(self.upload_completion):
            # Concaténez toutes les données pour reconstruire le fichier complet
            full_data = b"".join(self.upload_data)

            # Déterminez le chemin où enregistrer le fichier
            # Par exemple, enregistrez-le dans un dossier spécifique avec le nom spécifié
            save_path = "./" + self.upload_style + "/" + self.upload_song_name

            print("saving on : " + save_path)

            # Vérifiez si le dossier existe, sinon créez-le
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))

            # Enregistrez les données dans un nouveau fichier
            with open(save_path, "wb") as file:
                file.write(full_data)

            self.resetUpload()

    def resetUpload(self):
        # Réinitialisez toutes les variables d'upload pour une nouvelle transaction
        self.upload_data = [None] * len(self.upload_completion)
        self.upload_completion = [False] * len(self.upload_completion)
        self.upload_song_name = ""
        self.upload_style = ""

    def select(self, songName, current):

        retList = self.get_song_list()

        for song in retList:
            if song.__contains__(songName):
                songName = song
                break
        # Creating a media object
        # vlm = self.instance.vlm_add_broadcast("MyBroadcast", self.media_file_path + songName,
        #                                   ":sout=#rtp{sdp=rtsp://" + current.con.getInfo().localAddress + ":8554/} :no-sout-all :sout-keep", 0, [],
        #                                   True, False)
        mediaPath = self.media_file_path + songName
        self.media = self.instance.media_new(mediaPath)

        option = ':sout=rtp/ts://' + getIP.get_ip() + ':32470/'

        print("broadcasting : " + option)

        self.media.add_option(option)
        #
        # # Setting up the media player with the media object

        self.player.set_media(self.media)
        self.player.audio_set_volume(0)
        print("media changed to :",mediaPath)

    def play(self, current):
        if self.media != None:
            # Starting the broadcasting
            # Specify your desired IP and port for broadcasting
            print("song playing")
            self.player.play()

    def pause(self, current):
        if self.media != None:
            # Stopping the media player
            self.player.pause()
            print("song paused")

    def stop(self, current):
        if self.media != None:
            # Stopping the media player
            self.player.stop()
            self.media = None
            print("song stopped")

    def get_song_list(self):
        list = os.listdir('./')
        retList = []
        for object in list:
            if not object.__contains__(".py") and not object.__contains__("__"):
                for song in os.listdir('./' + object + "/"):
                    if song.__contains__(".mp3"):
                        retList.append(object + "/" + song)
        return retList

        # # Create a new vlm object
        #
        # # Wait for the broadcast to finish
        # input("Press any key to stop the broadcast...\n")
        #
        # # Stopping the broadcast
        # instance.vlm_del_media("MyBroadcast")

class ClientTemplate:
    port = "5000"
    adress = "localhost"

    def __init__(self, adress, port, communicator):
        proxy = communicator.stringToProxy("musiqueSender:default -h " + adress + " -p " + port)
        self.musiqueSender = SOUP.MusiqueSenderPrx.checkedCast(proxy)
        print("connected")

class RegistryTemplate:
    port = "5000"
    address = "localhost"

    def __init__(self, adress, port, communicator):
        proxy = communicator.stringToProxy("registry:default -h " + adress + " -p " + port)
        self.registry = SOUP.RegistryPrx.checkedCast(proxy)
        print("connected")


class ServerTemplate:

    port = "10000"
    adress = "localhost"

    def __init__(self, adress = "localhost", port = "10000", registryAddress = "localhost", registryPort = "4000", styleName = ""):
        self.communicator = Ice.initialize(sys.argv)
        self.adress = adress
        self.port = port
        self.styleName = styleName
        #<self.registry = RegistryTemplate(registryAddress, registryPort, self.communicator)
        #self.registry.registry.addServer(adress, port)

    def start(self):
        #
        # Install a signal handler to shutdown the communicator on Ctrl-C
        #
        adapter = self.communicator.createObjectAdapterWithEndpoints("MusiqueReceiver", "default -h " + self.adress + " -p " + self.port)
        adapter.add(MusiqueReceiverI(self), Ice.stringToIdentity("musiqueReceiver"))
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
    import getIP
    print("local IP :",getIP.get_ip())
    clientTest = ServerTemplate(getIP.get_ip(),"5000")
    clientTest.listen()
