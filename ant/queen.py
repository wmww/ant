import ant
import util.command

class Queen:
    def __init__(self):
        self.ants = []

    def add(self, a):
        if not isinstance(a, ant.Ant):
            raise ant.Error('add must only be given an Ant')
        self.ants.append(a)

    def _list_march(self, ants):
        for a in ants:
            self._list_march(a._dependencies())
            next = a.march(self)
            if next != None:
                if isinstance(next, ant.Ant):
                    next = [next]
                if not isinstance(next, list):
                    raise ant.Error('.march() should have retured an ant, a list or None')
                self._list_march(next)

    def run_command(self, args, **kwargs):
        return util.command.run(args, **kwargs)

    def march(self):
        self._list_march(self.ants)
