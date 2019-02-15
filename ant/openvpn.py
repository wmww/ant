import ant
from os import path

class OpenVpn(ant.Ant):
    """Given a path with zipped openvpn configuration files, installs them along with the vpnrun command"""
    def __init__(self, source_path):
        self.source_path = source_path
        self.get_zips_command = ant.Command('ls', source_path)
        self.deps = [
            ant.Command('openvpn', '--version')
                .check_exists()
                .if_false(ant.Install('openvpn')),
            self.get_zips_command
                .with_ignore_error()
        ]

    def march(self, queen):
        if not self.get_zips_command.result.is_success():
            raise ant.Error('Could not find zipped VPN data files in ' + self.source_path)
        zips = self.get_zips_command.result.stdout.split()
        zips = [i for i in zips if i.endswith('.zip')]
        print(zips)
