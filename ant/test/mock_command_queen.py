import ant
import util.command

class MockCommandQueen(ant.Queen):
    def __init__(self):
        super().__init__()
        self.commands = []

    def run_command(self, args, **kwargs):
        self.commands.append((args, kwargs))
        exit_code = 0
        if hasattr(self, 'installed'):
            cmd = args[0]
            if cmd == 'sudo':
                cmd = args[1]
                if cmd == '-S':
                    cmd = args[2]
            assert cmd in self.installed
            if not self.installed[cmd]:
                exit_code = 1
        return util.command.Result(None, None, exit_code)
