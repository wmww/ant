import unittest
import command

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
        result = command.run(['true'], capture_output=False)
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

    def test_output_from_timout_no_raise(self):
        result = command.run(['sh', '-c', 'echo abc; sleep 1; echo xyz'], timout=0.05, ignore_error=True)
        self.assertEqual(result.stdout, 'abc\n')
        self.assertEqual(result.stderr, '')
        self.assertEqual(result.exit_code, -9)

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
        import time
        start = time.perf_counter()
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['sh', '-c', 'sleep 5'], timout=0.05)
        end = time.perf_counter()
        elapsed = end - start
        self.assertGreater(elapsed, 0.04)
        self.assertLess(elapsed, 0.7)

    def test_input(self):
        result = command.run(['cat'], input_str='xyz\n')
        self.assertEqual(result.stdout, 'xyz\n')
