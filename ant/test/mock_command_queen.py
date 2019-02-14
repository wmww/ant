import ant
import util.command

class MockCommandQueen(ant.Queen):
    def __init__(self):
        super().__init__()
        self.commands = []

    def run_command(self, args, **kwargs):
        self.commands.append((args, kwargs))
        return util.command.Result(None, None, 0)
