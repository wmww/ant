#!/usr/bin/python3

import cyberstate as cs
from package import Package

manager = cs.Manager()
manager.add(Package('syncthing'))
manager.apply()
