import ant

def install_timout():
    return 3600

def get_installed_check():
    return ant.Command('apt', '-v').into_check()

class Update(ant.Ant):
    def __init__(self):
        self.deps = [
            ant.Command('apt', 'update')
                .with_timout(install_timout())
                .with_passthrough()
                .with_sudo()
        ]

class Install(ant.Ant):
    def __init__(self, package):
        self.package = package
        self.deps = [Update()]

    def march(self, queen):
        return [
            ant.Command()
                .with_args('apt', 'install', self.package.get_name())
                .with_timout(install_timout())
                .with_passthrough()
                .with_sudo()
        ]
