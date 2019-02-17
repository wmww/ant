import unittest
from util import log

class MockLogger(log.Logger):
    def __init__(self):
        self.logs = []
        self.context = None

    def log(self, context, log_type, message):
        self.logs.append((context, log_type, message))

class TestLog(unittest.TestCase):
    def setUp(self):
        self.log = MockLogger()

    def test_boring(self):
        self.log.boring('test')
        self.assertEqual(self.log.logs, [(None, log.Type.BORING, 'test')])

    def test_yikes(self):
        self.log.yikes('test')
        self.assertEqual(self.log.logs, [(None, log.Type.YIKES, 'test')])

    def test_big_yikes(self):
        self.log.big_yikes('test')
        self.assertEqual(self.log.logs, [(None, log.Type.BIG_YIKES, 'test')])

    def test_boring_multi_args(self):
        self.log.boring('test', 3, True)
        self.assertEqual(self.log.logs, [(None, log.Type.BORING, 'test 3 True')])

    def test_yikes_multi_args(self):
        self.log.yikes('test', 3, True)
        self.assertEqual(self.log.logs, [(None, log.Type.YIKES, 'test 3 True')])

    def test_big_yikes_multi_args(self):
        self.log.big_yikes('test', 3, True)
        self.assertEqual(self.log.logs, [(None, log.Type.BIG_YIKES, 'test 3 True')])

