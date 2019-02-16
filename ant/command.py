import ant

class Command(ant.Ant):
    def __init__(self, *args):
        self.args = list(args)
        self.kwargs = {}
        self.deps = []
        self.result = None

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
        self.kwargs['sudo'] = True
        return self

    def with_ignore_error(self):
        self.kwargs['ignore_error'] = True
        return self

    def check_success(self):
        """Return a Check object depending on this command (and make this command not raise on error)"""
        return SuccessCheck(self)

    def check_exists(self):
        """Return a Check object depending on this command (and make this command not raise on error)"""
        return ExistsCheck(self)

    def march(self, queen):
        args = self.args
        if not args:
            raise Error('No command arguments supplied')
        self.result = queen.command(args, **self.kwargs)

    def __str__(self):
        return 'run `' + ' '.join(self.args) + '`'

class SuccessCheck(ant.Check):
    def __init__(self, command):
        assert isinstance(command, Command)
        self.command = command
        self.deps = [
            command.with_ignore_error()
        ]

    def check(self, queen):
        assert self.command.result
        return self.command.result.success()

    def __str__(self):
        return 'check if `' + ' '.join(self.command.args) + '` succeeds'

class ExistsCheck(SuccessCheck):
    def check(self, queen):
        assert self.command.result
        return self.command.result.exit_code != 127

    def __str__(self):
        return 'check if `' + ' '.join(self.command.args) + '` exists'
