from pathlib import Path

class DesignConfig:
    def __init__(self):
        self.name: str = "designName"        # name of your verilog top module
        self.source_path: Path | None = None # directory path of the verilog source files (Absolute path is recommended). When None, the default path is "mainWorkspace/verilogDesigns"
config = DesignConfig()
