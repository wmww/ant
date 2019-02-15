import ant

def install_timout():
    return 3600

def get_installed_check():
    return ant.Command('pacman', '--version').check_success()

class Install(ant.Ant):
    def __init__(self, package):
        self.package = package

    def march(self, queen):
        return [
            ant.Command()
                .with_args('pacman', '-S', self.package.get_name())
                .with_timout(install_timout())
                .with_passthrough()
                .with_sudo()
        ]

    def __str__(self):
        return 'Install ' + str(self.package.name) + ' with pacman'
