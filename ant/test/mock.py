import ant
import mock
import util.command

"""Mock classes used for testing"""

class Ant(ant.Ant):
    def __init__(self, deps=None, next=None):
        self.applied = False
        self.next = next
        self.deps = deps

    def march(self, queen):
        for d in self._dependencies():
            if isinstance(d, Ant):
                assert d.applied
        assert not self.applied
        self.applied = True
        return self.next

class Queen(ant.Queen):
    """
    A Queen for testing that doesn't run commands, but instead logs them

    self.commands = [
        (['command', 'args'],
         {'timout': 60.0, 'passthrough': True, etc}),
        ...
    ]

    If self.installed is set, it is a dictionary of commands mapping to if they should appear to be installed
    All commands that are used must be in the dict, else an error will be raised
    The only purpose of this is that True commands will exit with code 0 and False ones will exit with code 1
    Sudo, although part of the args array, is not treated as a command, and doesn't need to be in the dict
    """
    def __init__(self):
        super().__init__(quiet=True)
        self.commands = []

    def command(self, args, **kwargs):
        self.commands.append((args, kwargs))
        exit_code = 0
        if hasattr(self, 'installed'):
            cmd = args[0]
            assert cmd in self.installed
            if not self.installed[cmd]:
                exit_code = 1
        return util.command.Result(None, None, exit_code)
