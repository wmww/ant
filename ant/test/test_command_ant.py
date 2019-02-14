import unittest
import ant
from mock_command_queen import MockCommandQueen

class TestCommandAnt(unittest.TestCase):
    def test_command_output(self):
        q = ant.Queen()
        a = ant.Command('echo', 'abc')
        q.add(a)
        q.march()
        self.assertEqual(a.result.stdout, 'abc\n')

class TestMockCommand(unittest.TestCase):
    def test_mock_command(self):
        q = MockCommandQueen()
        a = ant.Command('ls')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {})])

    def test_mock_command_multiple_args(self):
        q = MockCommandQueen()
        a = ant.Command('echo', 'abc')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['echo', 'abc'], {})])

    def test_mock_command_result(self):
        q = MockCommandQueen()
        a = ant.Command('echo', 'abc')
        q.add(a)
        q.march()
        self.assertIsNotNone(a.result)
        self.assertEqual(a.result.stdout, None)
        self.assertEqual(a.result.stderr, None)
        self.assertEqual(a.result.exit_code, 0)

    def test_with_args(self):
        q = MockCommandQueen()
        a = ant.Command().with_arg('echo').with_arg('a').with_args('b', 'c')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['echo', 'a', 'b', 'c'], {})])

    def test_with_timout(self):
        q = MockCommandQueen()
        a = ant.Command('ls').with_timout(4)
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'timout': 4})])

    def test_with_input_str(self):
        q = MockCommandQueen()
        a = ant.Command('ls').with_input_str('foo')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'input_str': 'foo'})])

    def test_with_passthrough(self):
        q = MockCommandQueen()
        a = ant.Command('ls').with_passthrough()
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'passthrough': True})])

    def test_with_cwd(self):
        q = MockCommandQueen()
        a = ant.Command('ls').with_cwd('/usr')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'cwd': '/usr'})])

    def test_with_sudo(self):
        q = MockCommandQueen()
        a = ant.Command('ls').with_sudo()
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['sudo', '-S', 'ls'], {})])

    def test_with_ignore_error(self):
        q = MockCommandQueen()
        a = ant.Command('ls').with_ignore_error()
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'ignore_error': True})])

class TestCommandTester(unittest.TestCase):
    def test_command_tester_true(self):
        q = ant.Queen()
        a = ant.command.Tester('true')
        q.add(a)
        q.march()
        self.assertTrue(a.success())

    def test_command_tester_false(self):
        q = ant.Queen()
        a = ant.command.Tester('false')
        q.add(a)
        q.march()
        self.assertFalse(a.success())

class TestCommandTesterMockCommand(unittest.TestCase):
    def test_command_tester_mock_true(self):
        q = MockCommandQueen()
        q.installed = {'echo': True}
        a = ant.command.Tester('echo')
        q.add(a)
        q.march()
        self.assertTrue(a.success())

    def test_command_tester_mock_false(self):
        q = MockCommandQueen()
        q.installed = {'echo': False}
        a = ant.command.Tester('echo')
        q.add(a)
        q.march()
        self.assertFalse(a.success())

