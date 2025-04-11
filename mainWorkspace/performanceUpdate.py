import os
import json
import config
import cocotb
from cocotb.runner import get_runner, Verilog, VHDL
from typing import Union
from pathlib import Path
from evaluation.hardware import get_hardware_performance
from evaluation.approximateMultiplier.model import Multiplier, MultiplierDut, Performance, AllPerformance

# region get Parameters
DESIGN_NAME             = config.design.name
DESIGN_SOURCES_DIR     = config.design.source_path if config.design.source_path else Path(__file__).resolve().parent/"verilogDesigns"
PERFORMANCE_FILE_PATH   = Path(__file__).resolve().parent/"performance.json"
SYNTHESIS_DIR          = config.synthesis.synthesis_dir


CALCULATE_IMAGE         = False
IMAGES_PATH             = Path(__file__).resolve().parent/"images"
# endregion


@cocotb.test() # type: ignore
async def get_design_performance(dut: MultiplierDut):
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
        performance["hardware"] = await get_hardware_performance(DESIGN_NAME, DESIGN_SOURCES_DIR, SYNTHESIS_DIR, config.synthesis.is_remote, config.synthesis.synopsys_host.hostname, config.synthesis.synopsys_host.username, config.synthesis.synopsys_host.password)

    # Run custom evaluation functions
    from evaluation.approximateMultiplier import evaluation_functions
    multiplier = Multiplier(dut)
    for metric_name, get_metric in evaluation_functions.items():
        performance[metric_name] = await get_metric(multiplier)

    # Write performance to file
    with open(PERFORMANCE_FILE_PATH, "w") as f:
        print(all_performance)
        f.write(json.dumps(all_performance, sort_keys=True, indent=4))


def run():
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "verilator")
    verilog_sources = [DESIGN_SOURCES_DIR / DESIGN_NAME / f"{DESIGN_NAME}.v"]
    build_test_args:list[Union[str, VHDL, Verilog]] = []

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        hdl_toplevel=DESIGN_NAME,
        always=True,
        build_args=build_test_args,
        includes=[DESIGN_SOURCES_DIR/DESIGN_NAME],
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