import ant
import os

class Uncompress(ant.Ant):
    def __init__(self, source, dest, allow_sudo=False):
        self.source = source
        self.dest = dest
        self.allow_sudo = allow_sudo

    def uncompress_zip(self, sudo):
        if sudo:
            kwargs = {
                'sudo': True,
                'passthrough': True,
                'timout': 20,
            }
        else:
            kwargs = {
                'passthrough': True,
            }
        self.queen.command(['unzip', '-o', self.source, '-d', self.dest], **kwargs)

    def march(self, queen):
        sudo = False
        if not os.access(self.dest, os.W_OK):
            if self.allow_sudo:
                sudo = True
            else:
                raise ant.Error('Can not write to ' + self.dest)
        if self.source.endswith('.zip'):
            self.uncompress_zip(sudo)
        else:
            raise ant.Error('no known method to unzip' + self.source)
