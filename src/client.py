#!/usr/bin/env python
#
# Copyright (c) ZeroC, Inc. All rights reserved.
#

import sys
import threading

import Ice

import server

Ice.loadSlice('Hello.ice')
import Demo

#
# Ice.initialize returns an initialized Ice communicator,
# the communicator is destroyed once it goes out of scope.
#
with Ice.initialize(sys.argv) as communicator:
    hello = Demo.HelloPrx.checkedCast(communicator.stringToProxy("hello:default -h localhost -p 11000"))
    server.listen()
    while True:
        message = input("say something : ")
        hello.say(message)
