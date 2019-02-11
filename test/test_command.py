import unittest
import command

class TestCommand(unittest.TestCase):
    def test_echo(self):
        result = command.run(['echo', 'abc'])
        self.assertEqual(result.stdout, 'abc\n')
        self.assertEqual(result.stderr, '')
        self.assertEqual(result.exit_code, 0)

    def test_true_noninteractive(self):
        result = command.run(['true'])
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, '')
        self.assertEqual(result.exit_code, 0)

    def test_true_interactive(self):
        result = command.run(['true'], interactive=True)
        self.assertEqual(result.stdout, None)
        self.assertEqual(result.stderr, None)
        self.assertEqual(result.exit_code, 0)

    def test_cwd(self):
        current = command.run(['ls'], cwd='.', raise_if_fail=True)
        dev = command.run(['ls'], cwd='/dev', raise_if_fail=True)
        self.assertNotEqual(current.stdout, dev.stdout)
        self.assertIn('null', {i: None for i in dev.stdout.split()})

    def test_false_result(self):
        result = command.run(['false'])
        self.assertEqual(result.exit_code, 1)

    def test_false_raise(self):
        with self.assertRaises(command.FailError) as cm:
            command.run(['false'], raise_if_fail=True)
        e = cm.exception
        self.assertEqual(e.args, ('false',)) # not sure why it turns the args into a tupel, but who cares
        self.assertEqual(e.result.stdout, '')
        self.assertEqual(e.result.stderr, '')
        self.assertEqual(e.result.exit_code, 1)

    def test_sleep_short(self):
        result = command.run(['sleep', '0.05'], timout=0.1)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, '')
        self.assertEqual(result.exit_code, 0)

    def test_sleep_timout(self):
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['sleep', '1'], timout=0.05)
        e = cm.exception
        self.assertEqual(e.result.stdout, '')
        self.assertEqual(e.result.stderr, '')
        self.assertEqual(e.result.exit_code, -9)

    def test_output_from_timout(self):
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['sh', '-c', 'echo abc; sleep 1; echo xyz'], timout=0.05)
        e = cm.exception
        self.assertEqual(e.result.stdout, 'abc\n')
        self.assertEqual(e.result.stderr, '')
        self.assertEqual(e.result.exit_code, -9)

    def test_timout_actually_works(self):
        import time
        start = time.perf_counter()
        with self.assertRaises(command.TimoutError):
            command.run(['sleep', '5'], timout=0.05)
        end = time.perf_counter()
        elapsed = end - start
        self.assertGreater(elapsed, 0.04)
        self.assertLess(elapsed, 0.7)

    def test_timout_actually_works_with_sh(self):
        """This currently should fail on Windows (see preexec_fn_popen_arg in command.py)"""
        import time
        start = time.perf_counter()
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['sh', '-c', 'sleep 5'], timout=0.05)
        end = time.perf_counter()
        elapsed = end - start
        self.assertGreater(elapsed, 0.04)
        self.assertLess(elapsed, 0.7)
