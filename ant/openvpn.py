import ant

class OpenVpn(ant.Ant):
    """Given a path with zipped openvpn configuration files, installs them along with the vpnrun command"""
    def __init__(self, source_path):
        self.deps = [
            ant.CheckCommand('openvpn', '-v')
                .if_false(ant.Install('openvpn'))
        ]
