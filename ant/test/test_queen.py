import unittest
import ant
import mock

class TestAnt(unittest.TestCase):

    def march(self, a):
        q = mock.Queen()
        q.add(a)
        q.march()
        return q

    def test_single_ant(self):
        a = mock.Ant()
        self.assertFalse(a.applied)
        self.march(a)
        self.assertTrue(a.applied)

    def test_ant_with_dep(self):
        a = mock.Ant()
        b = mock.Ant([a])
        self.march(b)
        self.assertTrue(a.applied)
        self.assertTrue(b.applied)

    def test_ant_with_dep_on_dep(self):
        a = mock.Ant()
        b = mock.Ant([a])
        c = mock.Ant([b])
        self.march(c)
        self.assertTrue(a.applied)
        self.assertTrue(b.applied)
        self.assertTrue(c.applied)

    def test_ant_with_multi_dep(self):
        a = mock.Ant()
        b = mock.Ant()
        c = mock.Ant([a, b])
        self.march(c)
        self.assertTrue(a.applied)
        self.assertTrue(b.applied)
        self.assertTrue(c.applied)

    def test_dep_does_not_apply_depending(self):
        a = mock.Ant()
        b = mock.Ant([a])
        self.march(a)
        self.assertTrue(a.applied)
        self.assertFalse(b.applied)

    def test_ant_with_next_ant(self):
        a = mock.Ant()
        b = mock.Ant(next=a)
        self.march(b)
        self.assertTrue(a.applied)
        self.assertTrue(b.applied)

    def test_ant_with_multi_after_ants(self):
        a = mock.Ant()
        b = mock.Ant()
        c = mock.Ant(next=[a, b])
        self.march(c)
        self.assertTrue(a.applied)
        self.assertTrue(b.applied)
        self.assertTrue(c.applied)

    def test_ant_with_after_and_dep(self):
        a = mock.Ant([])
        b = mock.Ant([])
        c = mock.Ant([a], [b])
        self.march(c)
        self.assertTrue(a.applied)
        self.assertTrue(b.applied)
        self.assertTrue(c.applied)

    def test_add_non_ant(self):
        with self.assertRaises(AssertionError) as cm:
            q = mock.Queen()
            q.add([])
