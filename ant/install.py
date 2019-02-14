from ant import Ant
from ant import install_apt as apt

class PackageManagerBuilder(Ant):
    def __init__(self):
        self.apt_test = apt.Tester()
        self.deps = [self.apt_test]

    def build(self, package):
        if self.apt_test.success():
            print(dir(apt))
            return apt.Install(package)
        else:
            raise ant.Error('No package manager found')

class Install(Ant):
    """A package that is to be installed"""
    def __init__(self, name):
        self.name = name
        self.builder = PackageManagerBuilder()
        self.deps = [self.builder]

    def march(self, queen):
        return self.builder.build(self)

    def get_name(self):
        return self.name
