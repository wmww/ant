import subprocess
import os
import signal

NOT_FOUND_EXIT_CODE = 127

class Result:
    """The result of a command, returned by run()"""
    def __init__(self, stdout, stderr, exit_code):
        assert isinstance(stdout, str) or stdout == None
        assert isinstance(stderr, str) or stderr == None
        assert isinstance(exit_code, int)
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

    def success(self):
        """If the process ended successfully"""
        return self.exit_code == 0

    def found(self):
        """If the command was found"""
        return self.exit_code != NOT_FOUND_EXIT_CODE

    def timout(self):
        """If the process ended because it timed out"""
        return self.exit_code == -signal.SIGTERM or self.exit_code == -signal.SIGKILL

    def terminated(self):
        """If the processed ended because it was aksed to with SIGTERM"""
        return self.exit_code == -signal.SIGTERM

    def killed(self):
        """If the process ended because it was forced to with SIGKILL"""
        return self.exit_code == -signal.SIGKILL

    def __str__(self):
        ret = ''
        ret += 'exit code: ' + str(self.exit_code)
        if self.stdout != None:
            ret += ('\nstdout: ' +
                    '\n        | '.join(self.stdout.strip().splitlines()))
        if self.stderr != None:
            ret += ('\nstderr: ' +
                    '\n        | '.join(self.stderr.strip().splitlines()))
        return ret

class Error(Exception):
    pass

class NotFoundError(Error):
    """Raised when the command to be run is not found"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name + ' not found'

class FailError(Error):
    """Raised in run() when raise_on_fail is true"""
    def __init__(self, args, result):
        self.args = args
        self.result = result

    def __str__(self):
        return '`' + ' '.join(self.args) + '` failed with ' + str(self.result)

class TimoutError(Error):
    def __init__(self, args, result, time):
        self.args = args
        self.result = result
        self.time = time

    def __str__(self):
        return ('`' + ' '.join(self.args) + '`' +
                ' timed out after ' + str(self.time) + ' second' + ('s' if self.time != 1 else '') +
                ' with ' + str(self.result))

def run(arguments, timout=1, input_str=None, passthrough=False, cwd=None, ignore_error=False):
    """
    Run a command, returning a result
    arguments: a list of strings, the command to run followed by the arguments
    timout: seconds before terminating the child. After SIGTERM, the child gets 100ms (or timout, whichever's shorter) to exit before getting SIGKILL
    input_str: stdin input for the command
    passthrough: if to pass stdout and stderr directly to the user, or capture the output
    cwd: current working directory to run the command in
    ignore_error: if false, may raise a command.FailError or command.TimoutoutError. If true, will always return a result
    """
    #log('Running `' + ' '.join(arg_list) + '`')
    out_popen_arg = None if passthrough else subprocess.PIPE
    in_popen_arg = None if input_str == None else subprocess.PIPE
    try:
        p = subprocess.Popen(arguments,
                             cwd=cwd,
                             stdin=in_popen_arg,
                             stdout=out_popen_arg,
                             stderr=out_popen_arg,
                             start_new_session=True)
        try:
            input_bytes = bytes(input_str, 'utf-8') if input_str != None else None
            stdout, stderr = p.communicate(input_bytes, timout)
            did_timout = False
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                stdout, stderr = p.communicate(None, min(timout, 0.1))
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                stdout, stderr = p.communicate()
            did_timout = True
        if passthrough:
            stdout = None
            stderr = None
        else:
            stdout = stdout.decode('utf-8') if stdout != None else ''
            stderr = stderr.decode('utf-8') if stderr != None else ''
        exit_code = p.returncode
    except FileNotFoundError as e:
        if ignore_error:
            stdout = None
            stderr = None
            exit_code = NOT_FOUND_EXIT_CODE
        else:
            raise NotFoundError(e.filename)
    result = Result(stdout, stderr, exit_code)
    if not ignore_error:
        if did_timout:
            raise TimoutError(arguments, result, timout)
        if exit_code != 0:
            raise FailError(arguments, result)
    return result
