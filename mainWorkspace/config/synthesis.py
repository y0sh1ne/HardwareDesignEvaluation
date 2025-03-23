from pathlib import Path
class Host:
    def __init__(self):
        self.hostname: str = ""
        self.username: str = ""
        self.password: str = ""


is_enable:bool = True
is_remote:bool = True
synopsys_host: Host = Host()
synthesis_path: Path = Path("xxxx/synopsysWorkspace/synthesis")
