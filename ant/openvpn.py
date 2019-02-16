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
        zip_paths = glob.glob(path.join(self.source_path, '*.zip'))
        if zip_paths:
            self.log.boring('Zip files: \n    ' + '\n    '.join(zip_paths))
        else:
            self.log.yikes('Could not find zipped VPN data files in ' + self.source_path)
        next_ants = [ant.Uncompress(zip_path, '/etc/openvpn/', allow_sudo=True) for zip_path in zip_paths]
        return next_ants
