from pathlib import Path
class Host:
    def __init__(self):
        self.hostname: str = ""
        self.username: str = ""
        self.password: str = ""

class SynthesisConfig:
    def __init__(self):
        self.is_enable:bool = True
        self.is_remote:bool = True
        self.synopsys_host: Host = Host()
        self.synthesis_path: Path = Path("xxxx/synopsysWorkspace/synthesis")

config = SynthesisConfig()
