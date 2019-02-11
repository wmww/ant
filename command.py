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
        return '`' + ' '.join(arg_list) + '` timed out after ' + self.time + ' seconds'

def run(arg_list, timout=1, interactive=False, cwd=None, stdin_text=None, raise_if_fail=False):
    """
    Run a command, returning a result
    arg_list: a list of strings, the command to run followed by the arguments
    timout: seconds
    interactive: if true, stdout/stderr will not be captured, and instead will get passed on directly to the user
    cwd: current working directory to run the command in
    stdin_text: input for the command
    raise_if_fail: if to raise a command.Error if the command fails
    """
    #log('Running `' + ' '.join(arg_list) + '`')
    out_popen_arg = None if interactive else subprocess.PIPE
    try:
        preexec_fn_popen_arg = os.setsid
        kill_subprocess_tree_on_timout = True
    except:
        # if os.setsid is not available (Windows), we wont be able to kill the child process if it has children
        # test_timout_actually_works_with_sh is the test that should fail
        preexec_fn_popen_arg = None
        kill_subprocess_tree_on_timout = False
    p = subprocess.Popen(arg_list,
                         cwd=cwd,
                         stdout=out_popen_arg,
                         stderr=out_popen_arg,
                         preexec_fn=preexec_fn_popen_arg)
    try:
        stdout, stderr = p.communicate(stdin_text, timout)
        did_timout = False
    except subprocess.TimeoutExpired:
        if kill_subprocess_tree_on_timout:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        else:
            p.kill() # will usually work, but will block if the process has running children
        stdout, stderr = p.communicate()
        did_timout = True
    if not interactive:
        stdout = stdout.decode('utf-8') if stdout != None else ''
        stderr = stderr.decode('utf-8') if stderr != None else ''
    else:
        stdout = None
        stderr = None
    exit_code = p.returncode
    result = Result(stdout, stderr, exit_code)
    if did_timout:
        raise TimoutError(arg_list, result, timout)
    if raise_if_fail and exit_code != 0:
        raise FailError(arg_list, result)
    return Result(stdout, stderr, exit_code)
