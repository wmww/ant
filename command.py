import subprocess
import os
import signal
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
        return '`' + ' '.join(self.args) + '` timed out after ' + str(self.time) + ' second' + ('s' if self.time != 1 else '')

def run(arguments, timout=1, capture_output=True, cwd=None, input_str=None, ignore_error=False):
    """
    Run a command, returning a result
    arguments: a list of strings, the command to run followed by the arguments
    timout: seconds
    capture_output: if to capture and return output, else passes stdout and stderr directly to the user
    cwd: current working directory to run the command in
    input_str: stdin input for the command
    ignore_error: if false, may raise a command.FailError or command.TimoutoutError. If true, will always return a result
    """
    #log('Running `' + ' '.join(arg_list) + '`')
    out_popen_arg = subprocess.PIPE if capture_output else None
    in_popen_arg =  subprocess.PIPE if input_str != None else None
    try:
        preexec_fn_popen_arg = os.setsid
        kill_subprocess_tree_on_timout = True
    except:
        # if os.setsid is not available (Windows), we wont be able to kill the child process if it has children
        # test_timout_actually_works_with_sh is the test that should fail (though it will also fail because sh)
        preexec_fn_popen_arg = None
        kill_subprocess_tree_on_timout = False
    p = subprocess.Popen(arguments,
                         cwd=cwd,
                         stdin=in_popen_arg,
                         stdout=out_popen_arg,
                         stderr=out_popen_arg,
                         preexec_fn=preexec_fn_popen_arg)
    try:
        input_bytes = bytes(input_str, 'utf-8') if input_str != None else None
        stdout, stderr = p.communicate(input_bytes, timout)
        did_timout = False
    except subprocess.TimeoutExpired:
        if kill_subprocess_tree_on_timout:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        else:
            p.kill() # will usually work, but will block if the process has running children
        stdout, stderr = p.communicate()
        did_timout = True
    if capture_output:
        stdout = stdout.decode('utf-8') if stdout != None else ''
        stderr = stderr.decode('utf-8') if stderr != None else ''
    else:
        stdout = None
        stderr = None
    exit_code = p.returncode
    result = Result(stdout, stderr, exit_code)
    if not ignore_error:
        if did_timout:
            raise TimoutError(arguments, result, timout)
        if exit_code != 0:
            raise FailError(arguments, result)
    return result
