import unittest
import ant

class TestAnt(unittest.TestCase):
    def test_no_deps(self):
        a = ant.Ant()
        self.assertEquals(a._dependencies(), [])
