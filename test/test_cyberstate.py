import unittest
import cyberstate as cs

class TestCS(unittest.TestCase):
    class MockState(cs.State):
        def __init__(self, dep):
            self.applied = 0
            self.dep = dep

        def dependencies(self):
            return self.dep

        def apply(self):
            for d in self.dep:
                if isinstance(d, TestCS.MockState) and d.applied == 0:
                    raise "State applied before dependency"
            self.applied += 1

    def test_single_state(self):
        m = cs.Manager()
        s = TestCS.MockState([])
        m.add(s)
        self.assertEqual(s.applied, 0)
        m.apply()
        self.assertEqual(s.applied, 1)

    def test_state_with_dep(self):
        m = cs.Manager()
        s1 = TestCS.MockState([])
        s2 = TestCS.MockState([s1])
        m.add(s2)
        self.assertEqual(s1.applied, 0)
        self.assertEqual(s2.applied, 0)
        m.apply()
        self.assertEqual(s1.applied, 1)
        self.assertEqual(s2.applied, 1)
