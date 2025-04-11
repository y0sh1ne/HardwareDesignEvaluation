from pathlib import Path

# synopsys server host information
class Host:
    def __init__(self):
        self.hostname: str = ""
        self.username: str = ""
        self.password: str = ""

class SynthesisConfig:
    def __init__(self):
        self.is_enable:bool = True          # Enable or disable synthesis
        self.is_remote:bool = True          # Run synthesis on remote server or local machine
        self.synopsys_host: Host = Host()   # if remote, synopsys host information
        self.synthesis_dir: Path = Path("xxxx/synopsysWorkspace/synthesis") # Path to the synopsysWorkspace on server host

config = SynthesisConfig()
