import unittest
import ant
import mock

class TestAnt(unittest.TestCase):

    def test_single_ant(self):
        m = mock.Queen()
        s = mock.Ant([])
        m.add(s)
        self.assertFalse(s.applied, 0)
        m.march()
        self.assertTrue(s.applied, 1)

    def test_ant_with_dep(self):
        m = mock.Queen()
        s1 = mock.Ant([])
        s2 = mock.Ant([s1])
        m.add(s2)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)

    def test_ant_with_dep_on_dep(self):
        m = mock.Queen()
        s1 = mock.Ant([])
        s2 = mock.Ant([s1])
        s3 = mock.Ant([s2])
        m.add(s3)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)
        self.assertTrue(s3.applied)

    def test_ant_with_multi_dep(self):
        m = mock.Queen()
        s1 = mock.Ant([])
        s2 = mock.Ant([])
        s3 = mock.Ant([s1, s2])
        m.add(s3)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)
        self.assertTrue(s3.applied)

    def test_ant_with_after_ant(self):
        m = mock.Queen()
        s1 = mock.Ant([])
        s2 = mock.Ant([], s1)
        m.add(s2)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)

    def test_ant_with_multi_after_ants(self):
        m = mock.Queen()
        s1 = mock.Ant([])
        s2 = mock.Ant([])
        s3 = mock.Ant([], [s1, s2])
        m.add(s3)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)
        self.assertTrue(s3.applied)

    def test_ant_with_after_and_dep(self):
        m = mock.Queen()
        s1 = mock.Ant([])
        s2 = mock.Ant([])
        s3 = mock.Ant([s1], [s2])
        m.add(s3)
        m.march()
        self.assertTrue(s1.applied)
        self.assertTrue(s2.applied)
        self.assertTrue(s3.applied)

    def test_add_non_ant(self):
        with self.assertRaises(ant.Error) as cm:
            q = mock.Queen()
            q.add([])
