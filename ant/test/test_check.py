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

    def test_true(self):
        q = ant.Queen()
        a = TrueCheck()
        q.add(a)
        q.march()
        self.assertTrue(a.is_true())

    def test_false(self):
        q = ant.Queen()
        a = FalseCheck()
        q.add(a)
        q.march()
        self.assertFalse(a.is_true())

    def test_ant_if_true_true(self):
        q = ant.Queen()
        a0 = mock.Ant()
        a1 = TrueCheck().if_true(a0)
        q.add(a1)
        q.march()
        self.assertTrue(a0.applied)

    def test_ant_if_true_false(self):
        q = ant.Queen()
        a0 = mock.Ant()
        a1 = FalseCheck().if_true(a0)
        q.add(a1)
        q.march()
        self.assertFalse(a0.applied)

    def test_ant_if_false_true(self):
        q = ant.Queen()
        a0 = mock.Ant()
        a1 = TrueCheck().if_false(a0)
        q.add(a1)
        q.march()
        self.assertFalse(a0.applied)

    def test_ant_if_false_false(self):
        q = ant.Queen()
        a0 = mock.Ant()
        a1 = FalseCheck().if_false(a0)
        q.add(a1)
        q.march()
        self.assertTrue(a0.applied)
