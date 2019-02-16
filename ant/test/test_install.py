import unittest
import ant
import mock
import ant.install_apt

class TestInstall(unittest.TestCase):
    def test_install_apt(self):
        q = mock.Queen()
        q.installed = {'apt': True, 'pacman': False}
        a = ant.Install('cowsay')
        q.add(a)
        q.march()
        i = 0
        self.assertEqual(q.commands[i][0], ['apt', '-v'])
        self.assertEqual(q.commands[i][1], {'ignore_error': True})
        i += 1
        self.assertEqual(q.commands[i][0], ['pacman', '--version'])
        self.assertEqual(q.commands[i][1], {'ignore_error': True})
        i += 1
        self.assertEqual(q.commands[i][0], ['apt', 'update'])
        self.assertEqual(q.commands[i][1], {
            'timout': ant.install_apt.install_timout(),
            'sudo': True,
            'passthrough': True
        })
        i += 1
        self.assertEqual(q.commands[i][0], ['apt', 'install', 'cowsay'])
        self.assertEqual(q.commands[i][1], {
            'timout': ant.install_apt.install_timout(),
            'sudo': True,
            'passthrough': True
        })

    def test_install_pacman(self):
        q = mock.Queen()
        q.installed = {'apt': False, 'pacman': True}
        a = ant.Install('cowsay')
        q.add(a)
        q.march()
        i = 0
        self.assertEqual(q.commands[i][0], ['apt', '-v'])
        self.assertEqual(q.commands[i][1], {'ignore_error': True})
        i += 1
        self.assertEqual(q.commands[i][0], ['pacman', '--version'])
        self.assertEqual(q.commands[i][1], {'ignore_error': True})
        i += 1
        self.assertEqual(q.commands[i][0], ['pacman', '-S', 'cowsay'])
        self.assertEqual(q.commands[i][1], {
            'timout': ant.install_apt.install_timout(),
            'sudo': True,
            'passthrough': True
        })
