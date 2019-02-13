from state import State

class Manager:
    def __init__(self):
        self.states = []

    def add(self, state):
        assert isinstance(state, State)
        self.states.append(state)

    def _apply_states(states):
        for state in states:
            Manager._apply_states(state.dependencies())
            state.apply()

    def apply(self):
        Manager._apply_states(self.states)
