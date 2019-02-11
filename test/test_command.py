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

    def test_sleep_timout(self):
        with self.assertRaises(command.TimoutError) as cm:
            command.run(['sleep', '1'], timout=0.25)
        e = cm.exception
        self.assertEqual(result.stdout, None)
        self.assertEqual(result.stderr, None)
        self.assertEqual(e.result.exit_code, 1)
