import unittest
import ant
import mock

class TestCommandAnt(unittest.TestCase):
    def test_command_output(self):
        q = ant.Queen()
        a = ant.Command('echo', 'abc')
        q.add(a)
        q.march()
        self.assertEqual(a.result.stdout, 'abc\n')

class TestMockCommand(unittest.TestCase):
    def test_mock_command(self):
        q = mock.Queen()
        a = ant.Command('ls')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {})])

    def test_mock_command_multiple_args(self):
        q = mock.Queen()
        a = ant.Command('echo', 'abc')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['echo', 'abc'], {})])

    def test_mock_command_result(self):
        q = mock.Queen()
        a = ant.Command('echo', 'abc')
        q.add(a)
        q.march()
        self.assertIsNotNone(a.result)
        self.assertEqual(a.result.stdout, None)
        self.assertEqual(a.result.stderr, None)
        self.assertEqual(a.result.exit_code, 0)

    def test_with_args(self):
        q = mock.Queen()
        a = ant.Command().with_arg('echo').with_arg('a').with_args('b', 'c')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['echo', 'a', 'b', 'c'], {})])

    def test_with_timout(self):
        q = mock.Queen()
        a = ant.Command('ls').with_timout(4)
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'timout': 4})])

    def test_with_input_str(self):
        q = mock.Queen()
        a = ant.Command('ls').with_input_str('foo')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'input_str': 'foo'})])

    def test_with_passthrough(self):
        q = mock.Queen()
        a = ant.Command('ls').with_passthrough()
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'passthrough': True})])

    def test_with_cwd(self):
        q = mock.Queen()
        a = ant.Command('ls').with_cwd('/usr')
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'cwd': '/usr'})])

    def test_with_sudo(self):
        q = mock.Queen()
        a = ant.Command('ls').with_sudo()
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['sudo', '-S', 'ls'], {})])

    def test_with_ignore_error(self):
        q = mock.Queen()
        a = ant.Command('ls').with_ignore_error()
        q.add(a)
        q.march()
        self.assertEqual(q.commands, [(['ls'], {'ignore_error': True})])

class TestCommandCheck(unittest.TestCase):
    def test_command_check_true(self):
        q = ant.Queen()
        a = ant.Command('true').into_check()
        q.add(a)
        q.march()
        self.assertTrue(a.is_true())

    def test_command_check_false(self):
        q = ant.Queen()
        a = ant.Command('false').into_check()
        q.add(a)
        q.march()
        self.assertFalse(a.is_true())

class TestCommandCheckMockCommand(unittest.TestCase):
    def test_command_check_mock_true(self):
        q = mock.Queen()
        q.installed = {'echo': True}
        a = ant.Command('echo').into_check()
        q.add(a)
        q.march()
        self.assertTrue(a.is_true())

    def test_command_check_mock_false(self):
        q = mock.Queen()
        q.installed = {'echo': False}
        a = ant.Command('echo').into_check()
        q.add(a)
        q.march()
        self.assertFalse(a.is_true())

