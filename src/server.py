#!/usr/bin/env python
#
# Copyright (c) ZeroC, Inc. All rights reserved.
#

import signal
import sys
import threading

import Ice

Ice.loadSlice('Hello.ice')
import Demo


class HelloI(Demo.Hello):
    def say(self, message, current):
        print("client said : "+message)

def start(communicator):
    #
    # Install a signal handler to shutdown the communicator on Ctrl-C
    #
    adapter = communicator.createObjectAdapterWithEndpoints("Hello", "default -h localhost -p 10000")
    adapter.add(HelloI(), Ice.stringToIdentity("hello"))
    adapter.activate()
    communicator.waitForShutdown()
def listen():
    #
    # Ice.initialize returns an initialized Ice communicator,
    # the communicator is destroyed once it goes out of scope.
    #
    with Ice.initialize(sys.argv) as communicator:
        signal.signal(signal.SIGINT, lambda signum, frame: communicator.shutdown())
        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, lambda signum, frame: communicator.shutdown())
        start(communicator)

if __name__ == '__main__':
    listen()