import command
from state import State

class Command(State):
    def __init__(self):
        self.args = []
        self.kwargs = {}
        self.deps = []
        self.sudo = False

    def with_dependency(self, state):
        self.deps.append(state)
        return self

    def with_arg(self, arg):
        self.args.append(arg)
        return self

    def with_args(self, *args):
        self.args += list(args)
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
        self.sudo = True
        return self

    def apply(self):
        args = self.args
        if not args:
            raise Error('No command arguments supplied')
        if self.sudo:
            args = ['sudo', '-S'] + args
        command.run(args, ignore_error=False, **self.kwargs)
