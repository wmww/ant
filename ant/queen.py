import ant
import util.command
import util.log

class Queen:
    def __init__(self):
        self.ants = []
        self.log = util.log.StreamLogger(self)

    def add(self, a):
        assert isinstance(a, ant.Ant), 'add must only be given an Ant'
        assert not hasattr(a, 'queen'), type(a).__name__ + ' ant added to multiple queens'
        a.queen = self
        a.log = util.log.StreamLogger(a, prefix='    ')
        self.ants.append(a)

    def _list_march(self, ants):
        for a in ants:
            deps = a._dependencies()
            if deps:
                self._list_march(deps)
            self.log.boring(str(a))
            next = a.march(self)
            if next != None and next != []:
                if isinstance(next, ant.Ant):
                    next = [next]
                if not isinstance(next, list):
                    raise ant.Error('.march() should have retured an ant, a list or None')
                self._list_march(next)
                self.log.boring('Done with ' + str(a))

    def run_command(self, args, **kwargs):
        return util.command.run(args, **kwargs)

    def march(self):
        self._list_march(self.ants)
