import unittest
import signal
import util.command as command

# if you have unexplained or intermittent test failures (especially on slower hardware) consider raising these
default_timout = 0.01 # default time to test timout
default_time_long = default_timout * 100 + 1 # default amount to sleep (which will get interrupted)
default_timout_tolerance = default_timout * 0.1 + 0.01 # how much longer than timout to accept
default_python_timout = default_timout * 2 + 0.1 # Python startup is too damn slow

class TestCommand(unittest.TestCase):
    def test_echo(self):
        result = command.run(['echo', 'abc'])
        self.assertEqual(result.stdout, 'abc\n')
        self.assertEqual(result.stderr, '')
        self.assertEqual(result.exit_code, 0)

    def test_true_capturing(self):
        result = command.run(['true'])
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, '')
        self.assertEqual(result.exit_code, 0)

    def test_true_noncapturing(self):
        result = command.run(['true'], passthrough=True)
        self.assertEqual(result.stdout, None)
        self.assertEqual(result.stderr, None)
        self.assertEqual(result.exit_code, 0)

    def test_cwd(self):
        current = command.run(['ls'], cwd='.')
        dev = command.run(['ls'], cwd='/dev')
        self.assertNotEqual(current.stdout, dev.stdout)
        self.assertIn('null', {i: None for i in dev.stdout.split()})

    def test_false_result(self):
        result = command.run(['false'], ignore_error=True)
        self.assertEqual(result.exit_code, 1)

    def test_false_raise(self):
        with self.assertRaises(command.FailError) as cm:
            command.run(['false'])
        e = cm.exception
        self.assertEqual(e.args, ('false',)) # not sure why it turns the args into a tupel, but who cares
        self.assertEqual(e.result.stdout, '')
        self.assertEqual(e.result.stderr, '')
        self.assertEqual(e.result.exit_code, 1)

    def test_sleep_short(self):
        result = command.run(['sleep', str(default_timout)],
                             timout=default_timout * 2)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, '')
        self.assertEqual(result.exit_code, 0)

    def test_sleep_timout(self):
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['sleep', str(default_time_long)],
                        timout=default_timout)
        e = cm.exception
        self.assertEqual(e.result.stdout, '')
        self.assertEqual(e.result.stderr, '')
        self.assertEqual(e.result.exit_code, -signal.SIGTERM)

    def test_output_from_timout(self):
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['sh', '-c', 'echo abc; sleep ' + str(default_time_long) + '; echo xyz'],
                        timout=default_timout)
        e = cm.exception
        self.assertEqual(e.result.stdout, 'abc\n')
        self.assertEqual(e.result.stderr, '')
        self.assertEqual(e.result.exit_code, -signal.SIGTERM)

    def test_output_from_timout_no_raise(self):
        result = command.run(['sh', '-c', 'echo abc; sleep ' + str(default_time_long) + '; echo xyz'],
                             timout=default_timout,
                             ignore_error=True)
        self.assertEqual(result.stdout, 'abc\n')
        self.assertEqual(result.stderr, '')
        self.assertEqual(result.exit_code, -signal.SIGTERM)

    def test_timout_actually_works(self):
        import time
        start = time.perf_counter()
        with self.assertRaises(command.TimoutError):
            command.run(['sleep', str(default_time_long)],
                        timout=default_timout)
        end = time.perf_counter()
        elapsed = end - start
        self.assertGreater(elapsed, default_timout)
        self.assertLess(elapsed, default_timout + default_timout_tolerance)

    def test_timout_actually_works_with_child(self):
        import time
        start = time.perf_counter()
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['sh', '-c', 'sleep ' + str(default_time_long)],
                        timout=default_timout)
        end = time.perf_counter()
        elapsed = end - start
        self.assertGreater(elapsed, default_timout)
        self.assertLess(elapsed, default_timout + default_timout_tolerance)

    def test_cooperative_child_gets_terminated(self):
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['python3', '-c', '''
import time
import sys
try:
    print('a')
    sys.stdout.flush()
    time.sleep(''' + str(default_time_long) + ''')
except:
    print('b')
    sys.stdout.flush()
                '''], timout=default_python_timout)
        e = cm.exception
        self.assertEqual(e.result.stdout, 'a\n')
        self.assertEqual(e.result.stderr, '')
        self.assertEqual(e.result.exit_code, -signal.SIGTERM)

    def test_uncooperative_child_gets_killed(self):
        with self.assertRaises(command.TimoutError) as cm:
            result = command.run(['python3', '-c', '''
import time
import signal
import sys
def signal_term_handler(signal, frame):
    print('c')
    sys.stdout.flush()
signal.signal(signal.SIGTERM, signal_term_handler)
try:
    print('a')
    sys.stdout.flush()
    time.sleep(''' + str(default_time_long) + ''')
except:
    print('b')
    sys.stdout.flush()
                '''], timout=default_python_timout)
        e = cm.exception
        self.assertEqual(e.result.stdout, 'a\nc\n')
        self.assertEqual(e.result.stderr, '')
        self.assertEqual(e.result.exit_code, -signal.SIGKILL) # Note the SIGKILL instead of SIGTERM, like in the rest

    def test_input(self):
        result = command.run(['cat'], input_str='xyz\n')
        self.assertEqual(result.stdout, 'xyz\n')

    def disabled_test_sudo(self):
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['echo', 'abc'], timout=default_timout, sudo=True)
        e = cm.exception
        self.assertEqual(e.result.stdout, '')
        self.assertRegex(e.result.stderr, '\\[sudo\\] password for .*:')
        self.assertEqual(e.result.exit_code, 1)
