#!/usr/bin/python3

import ant

queen = ant.Queen()
#queen.add(ant.Install('syncthing'))
queen.add(ant.OpenVpn('/home/wmww/light/Config/mullvad'))
queen.march()
