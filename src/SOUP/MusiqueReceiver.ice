//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#pragma once

module SOUP
{
    interface Registry
    {
        void addServer(string address, string port);
    };
    interface MusiqueReceiver
    {
        void addClient(string adress, string port);
        void getSongs();
        string getStyle();
        void select(string song);
        void play();
        void pause();
        void stop();
    };
    interface MusiqueSender
    {
        void responseGetSongs(string songs);
    }
}
