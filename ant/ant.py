class Ant:
    """
    A little ant which can do exactly one job
    set the deps option for this ant to depend on others
    """

    def _dependencies(self):
        if hasattr(self, 'deps') and self.deps is not None:
            return self.deps
        else:
            return []

    def march(self, queen):
        """Do the thing this ant can do"""
        pass
