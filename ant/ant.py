class Error(Exception):
    """Generic Ant error"""
    pass

class Ant:
    """
    A little ant which can do exactly one job
    set the deps option for this ant to depend on others
    """
    def with_dependency(self, a):
        if not hasattr(self, 'deps'):
            self.deps = []
        self.deps.append(state)
        return self

    def _dependencies(self):
        if hasattr(self, 'deps'):
            return self.deps
        else:
            return []

    def march(self):
        """Do the thing this ant can do"""
        pass
