class Error(Exception):
    """Generic Cyberstate error"""
    pass

class State:
    """A state that can be applied to a system"""
    def dependencies(self):
        """Return a list of states required before this state can be applied"""
        if hasattr(self, 'deps'):
            return self.deps
        else:
            return []

    def apply(self):
        """Apply this state, assumed to succeed unless an exception is raised"""
        pass
