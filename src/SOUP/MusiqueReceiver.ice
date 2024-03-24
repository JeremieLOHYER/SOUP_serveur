//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#pragma once

module SOUP
{

    interface MusiqueReceiver
    {
        void AddClient(string adress, string port);
        void getSongs();
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
