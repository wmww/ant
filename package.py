import command
import cyberstate as cs

class PackageManagerUpdated(cs.State):
    def apply(self):
        result = command.run(['apt', 'update'], timout=3600, passthrough=True, sudo=True)

class Package(cs.State):
    """A package that is to be installed"""
    def __init__(self, name):
        self.name = name

    def dependencies(self):
        return [PackageManagerUpdated()]

    def apply(self):
        result = command.run(['apt', 'install', self.name], timout=3600, passthrough=True, sudo=True)
