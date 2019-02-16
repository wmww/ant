import ant
import util.command
import util.log

class Queen:
    def __init__(self, quiet=False):
        self.ants = []
        self.quiet = quiet
        if self.quiet:
            self.log = util.log.NullLogger()
        else:
            self.log = util.log.StreamLogger(self)

    def _register(self, a):
        assert isinstance(a, ant.Ant)
        assert not hasattr(a, 'queen') or a.queen == self, type(a).__name__ + ' ant added to multiple queens'
        a.queen = self
        if not hasattr(a, 'log'):
            a.log = util.log.ProxyLogger(self.log, context=a, prefix='    ')

    def add(self, a):
        assert isinstance(a, ant.Ant), 'add must only be given an Ant'
        self._register(a)
        self.ants.append(a)

    def _list_march(self, ants):
        for a in ants:
            deps = a._dependencies()
            if deps:
                self._list_march(deps)
            self.log.boring(str(a))
            self._register(a)
            next = a.march(self)
            if next != None and next != []:
                if isinstance(next, ant.Ant):
                    next = [next]
                if not isinstance(next, list):
                    raise ant.Error('.march() should have retured an ant, a list or None')
                self._list_march(next)
                self.log.boring('Done with ' + str(a))

    def command(self, args, sudo=False, **kwargs):
        if sudo:
            args = ['sudo', '-S'] + args
        return util.command.run(args, **kwargs)

    def march(self):
        self._list_march(self.ants)
