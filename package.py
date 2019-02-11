import cyberstate as cs

class Package(cs.State):
    """A package that is to be installed"""
    def __init__(self, name):
        self.name = name

    def apply(self):
        raise cs.Error("Package can not be applied directly")
