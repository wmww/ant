import ant

class Tester(ant.command.Tester):
    def __init__(self):
        super().__init__('apt', '-v')

class Update(ant.Ant):
    def __init__(self):
        self.deps = [
            ant.Command('apt', 'update')
                .with_args()
                .with_timout(3600)
                .with_passthrough()
                .with_sudo()
        ]

class Install(ant.Ant):
    def __init__(self, package):
        self.package = package
        self.deps = [Update()]

    def march(self):
        return [
            ant.Command()
                .with_args('apt', 'install', self.package.get_name())
                .with_args()
                .with_timout(3600)
                .with_passthrough()
                .with_sudo()
        ]
