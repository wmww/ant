from ant import Ant
from ant import install_apt as apt

class Install(Ant):
    """A package that is to be installed"""
    def __init__(self, name):
        self.name = name
        self.apt_check = apt.get_installed_check()
        self.deps = [self.apt_check]

    def march(self, queen):
        if self.apt_check.is_true():
            return apt.Install(self)
        else:
            raise ant.Error('No package manager found')

    def get_name(self):
        return self.name
