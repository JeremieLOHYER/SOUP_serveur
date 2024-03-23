//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#pragma once

module SOUP
{

    interface MusiqueReceiver
    {
        string getSongs();
        void select(string song);
        void play();
        void pause();
        void stop();
    }
}
