import subprocess
import cyberstate as cs

class Result:
    """The result of a command, returned by run()"""
    def __init__(self, stdout, stderr, exit_code):
        assert isinstance(stdout, str) or stdout == None
        assert isinstance(stderr, str) or stderr == None
        assert isinstance(exit_code, int)
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

class Error(cs.Error):
    pass

class FailError(Error):
    """Raised in run() when raise_on_fail is true"""
    def __init__(self, args, result):
        self.args = args
        self.result = result

    def __str__(self):
        return '`' + ' '.join(self.args) + '` exited with code ' + str(self.result.exit_code)

class TimoutError(Error):
    def __init__(self, args, result, time):
        self.args = args
        self.result = result
        self.time = time

    def __str__(self):
        return '`' + ' '.join(arg_list) + '` timed out after ' + self.time + ' seconds'

def run(arg_list, timout=1, interactive=False, path=None, stdin_text=None, raise_if_fail=False):
    """
    Run a command, returning a result
    arg_list: a list of strings, the command to run followed by the arguments
    timout: seconds
    interactive: if true, stdout/stderr will not be captured, and instead will get passed on directly to the user
    path: working directory to run the command in
    stdin_text: input for the command
    raise_if_fail: if to raise a command.Error if the command fails
    """
    #log('Running `' + ' '.join(arg_list) + '`')
    if interactive:
        out_popen_arg = None
    else:
        out_popen_arg = subprocess.PIPE
    p = subprocess.Popen(arg_list, cwd=path, stdout=out_popen_arg, stderr=out_popen_arg)
    stdout, stderr = p.communicate(stdin_text)
    if not interactive:
        stdout = stdout.decode('utf-8') if stdout != None else ''
        stderr = stderr.decode('utf-8') if stderr != None else ''
    else:
        stdout = None
        stderr = None
    exit_code = p.returncode
    result = Result(stdout, stderr, exit_code)
    if raise_if_fail and exit_code != 0:
        raise FailError(arg_list, result)
    return Result(stdout, stderr, exit_code)
