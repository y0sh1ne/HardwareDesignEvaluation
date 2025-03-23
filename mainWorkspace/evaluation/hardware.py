from model import DesignDut, HardwarePerformance, DesignName
from paramiko import SFTPClient
from pathlib import Path

async def get_hardware_performance(dut: DesignDut, DESIGN_NAME: DesignName, SYNTHESIS_PATH: Path, SYNTHESIS_SFTP: SFTPClient | None)->HardwarePerformance:
    area = 0
    delay = 0
    power = 0
    try:
        if SYNTHESIS_SFTP:
            with SYNTHESIS_SFTP.open(f"{SYNTHESIS_PATH}/{DESIGN_NAME}/{DESIGN_NAME}.area.log", "r") as f:
                for line in f.readlines()[21:]:
                    if line[0:19] == "Combinational area:":
                        area = float(line.split()[-1])
                        break
            with SYNTHESIS_SFTP.open(f"{SYNTHESIS_PATH}/{DESIGN_NAME}/{DESIGN_NAME}.max.timing.log", "r") as f:
                for line in f.readlines():
                    if line[2:19] == "data arrival time":
                        delay = float(line.split()[-1])
                        break
            with SYNTHESIS_SFTP.open(f"{SYNTHESIS_PATH}/{DESIGN_NAME}/{DESIGN_NAME}.power.log", "r") as f:
                power = float(f.readlines()[-2].split()[-2])
        else:
            with open(f"{SYNTHESIS_PATH}/{DESIGN_NAME}/{DESIGN_NAME}.area.log", "r") as f:
                for line in f.readlines()[21:]:
                    if line[0:19] == "Combinational area:":
                        area = float(line.split()[-1])
                        break
            with open(f"{SYNTHESIS_PATH}/{DESIGN_NAME}/{DESIGN_NAME}.max.timing.log", "r") as f:
                for line in f.readlines():
                    if line[2:19] == "data arrival time":
                        delay = float(line.split()[-1])
                        break
            with open(f"{SYNTHESIS_PATH}/{DESIGN_NAME}/{DESIGN_NAME}.power.log", "r") as f:
                power = float(f.readlines()[-2].split()[-2])
    except Exception as e:
        raise e
    return HardwarePerformance(area=area,delay=delay,power=power,PDAP=area*delay*power)