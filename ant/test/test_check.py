import unittest
import ant
import mock

class TrueCheck(ant.Check):
    def check(self, queen):
        assert isinstance(queen, ant.Queen)
        return True

class FalseCheck(ant.Check):
    def check(self, queen):
        assert isinstance(queen, ant.Queen)
        return False

class TestCheck(unittest.TestCase):
    def march(self, a):
        q = mock.Queen()
        q.add(a)
        q.march()
        return q

    def test_true(self):
        a = TrueCheck()
        self.march(a)
        self.assertTrue(a.is_true())

    def test_false(self):
        a = FalseCheck()
        self.march(a)
        self.assertFalse(a.is_true())

    def test_ant_if_true_true(self):
        a = mock.Ant()
        b = TrueCheck().if_true(a)
        self.march(b)
        self.assertTrue(a.applied)

    def test_ant_if_true_false(self):
        a = mock.Ant()
        b = FalseCheck().if_true(a)
        self.march(b)
        self.assertFalse(a.applied)

    def test_ant_if_false_true(self):
        a = mock.Ant()
        b = TrueCheck().if_false(a)
        self.march(b)
        self.assertFalse(a.applied)

    def test_ant_if_false_false(self):
        a = mock.Ant()
        b = FalseCheck().if_false(a)
        self.march(b)
        self.assertTrue(a.applied)
