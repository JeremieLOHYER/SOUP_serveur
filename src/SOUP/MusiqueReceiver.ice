//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#pragma once

module SOUP
{
    sequence<byte> dataArray;

    interface Registry
    {
        void addServer(string address, string port);
    };
    interface MusiqueReceiver
    {
        void addClient(string adress, string port);
        void getSongs();
        void getSongsByName(string songName);
        void getSongsByAuthor(string author);
        void prepareUpload(string style, string songName, int nbBlocs);
        void upload(int blocId, dataArray data);
        void select(string song);
        void play();
        void pause();
        void stop();
    };
    interface MusiqueSender
    {
        void responseGetSongs(string songs);
        void responseGetCompletion(int complete);
    }
}
