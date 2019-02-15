#!/usr/bin/python3

import ant

queen = ant.Queen()
queen.add(ant.Command('cowsay', '-h')
        .check_exists()
        .if_false(ant.Install('cowsay')))
queen.add(
    ant.Command('syncthing', '--version')
        .check_success()
        .if_false(ant.Install('syncthing')))
queen.add(
    ant.OpenVpn('/home/wmww/light/Config/mullvad'))
queen.march()
