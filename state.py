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

class Command(State):
    def __init__(self):
        self.args = None
        self.kwargs = {}
        self.deps = []

    def with_dependency(self, state):
        self.deps.append(state)
        return self

    def with_args(self, *args):
        self.args = list(args)
        return self

    def with_timout(self, timout):
        self.kwargs['timout'] = timout
        return self

    def with_input_str(self, input_str):
        self.kwargs['input_str'] = input_str
        return self

    def with_passthrough(self):
        self.kwargs['passthrough'] = True
        return self

    def with_cwd(self, cwd):
        self.kwargs['cwd'] = cwd
        return self

    def with_sudo(self):
        self.kwargs['sudo'] = True
        return self

    def apply(self):
        import command
        if not self.args:
            raise Error('No in applyargs supplied')
        command.run(self.args, ignore_error=False, **self.kwargs)
