import unittest
import ant

class TestCommandAnt(unittest.TestCase):
    def test_command_output(self):
        q = ant.Queen()
        a = ant.Command('echo', 'abc')
        q.add(a)
        q.march()
        self.assertEqual(a.result.stdout, 'abc\n')

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
