class State:
    """A state that can be applied to a system"""
    def dependencies(self):
        """Return a list of states required before this state can be applied"""
        return []

    def apply(self):
        """Apply this state, assumed to succeed unless an exception is raised"""
        pass

class Manager:
    def __init__(self):
        self.states = []

    def add(self, state):
        self.states.append(state)

    def _apply_states(states):
        for state in states:
            Manager._apply_states(state.dependencies())
            state.apply()

    def apply(self):
        Manager._apply_states(self.states)

class Error(Exception):
    """Generic Cyberstate error"""
    pass
