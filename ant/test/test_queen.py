import unittest
import ant

class MockAnt(ant.Ant):
    def __init__(self, deps, after=None):
        self.applied = False
        self.after = after
        self.deps = deps

    def march(self):
        for d in self.deps:
            if isinstance(d, MockAnt):
                assert d.applied > 0
        assert not self.applied
        self.applied = True
        return self.after

class TestAnt(unittest.TestCase):

    def test_single_ant(self):
        m = ant.Queen()
        s = MockAnt([])
        m.add(s)
        self.assertFalse(s.applied, 0)
        m.march()
        self.assertTrue(s.applied, 1)

    def test_ant_with_dep(self):
        m = ant.Queen()
        s1 = MockAnt([])
        s2 = MockAnt([s1])
        m.add(s2)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)

    def test_ant_with_multi_dep(self):
        m = ant.Queen()
        s1 = MockAnt([])
        s2 = MockAnt([])
        s3 = MockAnt([s1, s2])
        m.add(s3)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)
        self.assertTrue(s3.applied)

    def test_ant_with_after_ant(self):
        m = ant.Queen()
        s1 = MockAnt([])
        s2 = MockAnt([], s1)
        m.add(s2)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)

    def test_ant_with_multi_after_ants(self):
        m = ant.Queen()
        s1 = MockAnt([])
        s2 = MockAnt([])
        s3 = MockAnt([], [s1, s2])
        m.add(s3)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)
        self.assertTrue(s3.applied)

    def test_add_non_ant(self):
        with self.assertRaises(ant.Error) as cm:
            q = ant.Queen()
            q.add([])
