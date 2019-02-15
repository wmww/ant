from ant import Ant
from ant import install_apt as apt
from ant import install_pacman as pacman

class Install(Ant):
    """A package that is to be installed"""
    def __init__(self, name):
        self.name = name
        self.apt_check = apt.get_installed_check()
        self.pacman_check = pacman.get_installed_check()
        self.deps = [self.apt_check, self.pacman_check]

    def march(self, queen):
        if self.apt_check.is_true():
            return apt.Install(self)
        elif self.pacman_check.is_true():
            return pacman.Install(self)
        else:
            raise ant.Error('No package manager found')

    def get_name(self):
        return self.name

    def __str__(self):
        return 'Install ' + str(self.name)
