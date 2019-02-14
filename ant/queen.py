import ant

class Queen:
    def __init__(self):
        self.ants = []

    def add(self, a):
        if not isinstance(a, ant.Ant):
            raise ant.Error('add must only be given an Ant')
        self.ants.append(a)

    def _all_march(ants):
        for a in ants:
            Queen._all_march(a._dependencies())
            next = a.march()
            if next != None:
                if isinstance(next, ant.Ant):
                    next = [next]
                if not isinstance(next, list):
                    raise ant.Error('.march() should have retured an ant, a list or None')
                Queen._all_march(next)

    def march(self):
        Queen._all_march(self.ants)
