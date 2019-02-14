import unittest
import ant
import ant.install_apt
from mock_command_queen import MockCommandQueen

class TestInstall(unittest.TestCase):
    def test_install_apt(self):
        q = MockCommandQueen()
        q.installed = {'apt': True, 'pacman': False}
        a = ant.Install('cowsay')
        q.add(a)
        q.march()
        self.assertEqual(q.commands[0][0], ['apt', '-v'])
        self.assertEqual(q.commands[0][1], {'ignore_error': True})
        self.assertEqual(q.commands[1][0], ['sudo', '-S', 'apt', 'update'])
        self.assertEqual(q.commands[1][1], {
            'timout': ant.install_apt.install_timout(),
            'passthrough': True
        })
        self.assertEqual(q.commands[2][0], ['sudo', '-S', 'apt', 'install', 'cowsay'])
        self.assertEqual(q.commands[2][1], {
            'timout': ant.install_apt.install_timout(),
            'passthrough': True
        })
