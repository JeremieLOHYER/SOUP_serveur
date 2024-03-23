import argparse
import ctypes
import os

import vlc



class StreamProviderDir(object):
    def __init__(self, rootpath, file_ext):
        self._media_files = []
        self._rootpath = rootpath
        self._file_ext = file_ext
        self._index = 0

    def open(self):
        """
        this function is responsible of opening the media.
        it could have been done in the __init__, but it is just an example

        in this case it scan the specified folder, but it could also scan a
        remote url or whatever you prefer.
        """

        print("read file list")
        for entry in os.listdir(self._rootpath):
            if os.path.splitext(entry)[1] == f".{self._file_ext}":
                self._media_files.append(os.path.join(self._rootpath, entry))
        self._media_files.sort()

        print("playlist:")
        for index, media_file in enumerate(self._media_files):
            print(f"[{index}] {media_file}")

    def release_resources(self):
        """
        In this example this function is just a placeholder,
        in a more complex example this may release resources after the usage,
        e.g. closing the socket from where we retrieved media data
        """
        print("releasing stream provider")

    def seek(self, offset):
        """
        Again, a placeholder, not useful for the example
        """
        print(f"requested seek with offset={offset}")

    def get_data(self):
        """
        It reads the current file in the list and returns the binary data
        In this example it reads from file, but it could have downloaded data from an url
        """
        print(f"reading file [{self._index}] ", end='')

        if self._index == len(self._media_files):
            print("file list is over")
            return b''

        print(f"{self._media_files[self._index]}")
        with open(self._media_files[self._index], 'rb') as stream:
            data = stream.read()

        self._index = self._index + 1

        return data


# HERE THERE ARE THE CALLBACKS USED BY THE MEDIA CREATED IN THE "MAIN"
# a callback in its simplest form is a python function decorated with the specific @vlc.CallbackDecorators.*

@vlc.CallbackDecorators.MediaOpenCb
def media_open_cb(opaque, data_pointer, size_pointer):
    print("OPEN", opaque, data_pointer, size_pointer)

    stream_provider = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value

    stream_provider.open()

    data_pointer.contents.value = opaque
    size_pointer.value = 1 ** 64 - 1

    return 0


@vlc.CallbackDecorators.MediaReadCb
def media_read_cb(opaque, buffer, length):
    print("READ", opaque, buffer, length)

    stream_provider = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value

    new_data = stream_provider.get_data()
    bytes_read = len(new_data)

    if bytes_read > 0:
        buffer_array = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char * bytes_read))
        for index, b in enumerate(new_data):
            buffer_array.contents[index] = ctypes.c_char(b)

    print(f"just read f{bytes_read}B")
    return bytes_read


@vlc.CallbackDecorators.MediaSeekCb
def media_seek_cb(opaque, offset):
    print("SEEK", opaque, offset)

    stream_provider = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value

    stream_provider.seek(offset)

    return 0


@vlc.CallbackDecorators.MediaCloseCb
def media_close_cb(opaque):
    print("CLOSE", opaque)

    stream_provider = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value

    stream_provider.release_resources()


# MAIN
if __name__ == '__main__':


    # Path to your media file
    media_file_path = "../styles/pop/chipichipi.mp3"

    # Creating a VLC instance
    instance = vlc.Instance("--no-video")

    # Creating a media player
    player = instance.media_player_new()

    # Creating a media object
    media = instance.media_new(media_file_path)

    # Setting up the media player with the media object
    player.set_media(media)
    player.audio_set_volume(100)

    # Starting the broadcasting
    # Specify your desired IP and port for broadcasting
    # Here, we are using UDP for broadcasting
    player.play()

    # Create a new vlm object
    vlm = instance.vlm_add_broadcast("MyBroadcast", media_file_path,
                                     ":sout=#duplicate{dst=std{access=udp,mux=ts,dst=239.255.0.1:1234}}",0,[],True,False)

    # Wait for the broadcast to finish
    input("Press any key to stop the broadcast...\n")

    # Stopping the broadcast
    instance.vlm_del_media("MyBroadcast")

    # Stopping the media player
    player.stop()