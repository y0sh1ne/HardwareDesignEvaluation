import os
import json
import config
import cocotb
from cocotb.runner import get_runner, Verilog, VHDL
from typing import Union
from paramiko import SFTPClient
from pathlib import Path
from evaluation.model import DesignDut, Performance, AllPerformance


# region get Parameters
SYNTHESIS_SFTP: SFTPClient | None = None
if config.synthesis.is_remote:
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host = config.synthesis.synopsys_host
    client.connect(hostname=host.hostname, username=host.username, password=host.password)
    SYNTHESIS_SFTP = client.open_sftp() # type: ignore
DESIGN_NAME             = config.design.name
DESIGN_SOURCES_PATH     = config.design.source_path if config.design.source_path.exists() else Path(__file__).resolve().parent/"verilogDesigns"
PERFORMANCE_FILE_PATH   = Path(__file__).resolve().parent/"performance.json"
SYNTHESIS_PATH          = config.synthesis.synthesis_path


CALCULATE_IMAGE         = False
IMAGES_PATH             = Path(__file__).resolve().parent/"images"
# endregion


@cocotb.test() # type: ignore
async def get_design_performance(dut: DesignDut):
    with open(PERFORMANCE_FILE_PATH,"r") as f:
        all_performance: AllPerformance = json.loads(f.read())
    if DESIGN_NAME not in all_performance:
        all_performance[DESIGN_NAME] = Performance({
            "accuracy": {
                "NMED": 0,
                "MRED": 0
            },
            "hardware": {
                "area": 0,
                "delay": 0,
                "power": 0,
                "PDAP": 0,
            },
        })
    performance:Performance = all_performance[DESIGN_NAME]

    # Get hardware performance, include Area, Delay, Power and PDAP
    if config.synthesis.is_enable:
        from evaluation.hardware import get_hardware_performance
        performance["hardware"] = await get_hardware_performance(dut, DESIGN_NAME, SYNTHESIS_PATH, SYNTHESIS_SFTP)

    # Run custom evaluation functions
    from evaluation import evaluation_functions
    for metric_name, get_metric in evaluation_functions.items():
        performance[metric_name] = await get_metric(dut)

    # Write performance to file
    with open(PERFORMANCE_FILE_PATH, "w") as f:
        print(all_performance)
        f.write(json.dumps(all_performance, sort_keys=True, indent=4))


def run():
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "verilator")
    verilog_sources = [DESIGN_SOURCES_PATH / f"{DESIGN_NAME}.v"]
    build_test_args:list[Union[str, VHDL, Verilog]] = []

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        hdl_toplevel=DESIGN_NAME,
        always=True,
        build_args=build_test_args,
        includes=[DESIGN_SOURCES_PATH],
        clean=True,
    )
    runner.test(
        test_module="performanceUpdate", 
        hdl_toplevel=DESIGN_NAME,
        hdl_toplevel_lang=hdl_toplevel_lang,
        test_args=build_test_args,
    )


if __name__ == "__main__":
    run()