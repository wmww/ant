import ant

class Check(ant.Ant):
    """
    An ant that represents some sort of true/false check
    the attribute self.is_true should be unset until march, at which point it should be set to True or False
    """

    def check(self, queen):
        """Called after deps have marched inside this ant's march"""
        raise NotImplementedError()

    def get_if_true_ants(self):
        if not hasattr(self, 'if_true_ants'):
            self.if_true_ants = []
        return self.if_true_ants

    def get_if_false_ants(self):
        if not hasattr(self, 'if_false_ants'):
            self.if_false_ants = []
        return self.if_false_ants

    def if_true(self, a):
        """This ant will only march if the check passes"""
        assert isinstance(a, ant.Ant)
        self.get_if_true_ants().append(a)
        return self

    def if_false(self, a):
        """This ant will only march if the check doesn't pass"""
        assert isinstance(a, ant.Ant)
        self.get_if_false_ants().append(a)
        return self

    def is_true(self):
        assert hasattr(self, 'result')
        return self.result

    def march(self, queen):
        self.result = self.check(queen)
        if self.result:
            return self.get_if_true_ants()
        else:
            return self.get_if_false_ants()
