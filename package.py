import command
import cyberstate as cs

class PackageManagerUpdated(cs.State):
    def dependencies(self):
        return [cs.Command()
            .with_args('apt', 'update')
            .with_timout(3600)
            .with_passthrough()
            .with_sudo()]

class Package(cs.State):
    """A package that is to be installed"""
    def __init__(self, name):
        self.name = name

    def dependencies(self):
        return [cs.Command()
            .with_dependency(PackageManagerUpdated())
            .with_args('apt', 'install', self.name)
            .with_timout(3600)
            .with_passthrough()
            .with_sudo()]
