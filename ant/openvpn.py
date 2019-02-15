import ant
from os import path
import glob

class OpenVpn(ant.Ant):
    """Given a path with zipped openvpn configuration files, installs them along with the vpnrun command"""
    def __init__(self, source_path):
        super().__init__()
        self.source_path = source_path
        self.deps = [
            ant.Command('openvpn', '--version')
                .check_exists()
                .if_false(ant.Install('openvpn')),
        ]

    def march(self, queen):
        zips = glob.glob(path.join(self.source_path, '*.zip'))
        if not zips:
            raise ant.Error('Could not find zipped VPN data files in ' + self.source_path)
        self.log.boring('Zip files: \n    ' + '\n    '.join(zips))
