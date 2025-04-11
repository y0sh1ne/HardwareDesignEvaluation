import paramiko
import shutil
import os
from .model import HardwarePerformance, DesignName
from pathlib import Path
from typing import Optional

# region File Handling Functions
def upload_design_dir(src: Path, dst: Path, is_remote: bool, sftp: Optional[paramiko.SFTPClient]):
    """
    Upload dir `src` to `dst`, if is remote, use `paramiko`, otherwise use `shutil`.

    :param src: source dir path
    :param dst: destination dir path
    :param is_remote: whether to upload to remote server
    :param host: remote server host information
    """
    if not src.is_dir():
        raise ValueError(f"Source {src} is not a directory")

    if is_remote:
        if sftp is None:
            raise ValueError("SFTP client is not provided for remote upload")
        def ensure_remote_dir(path: Path):
            try:
                sftp.stat(str(path.as_posix()))
            except FileNotFoundError:
                ensure_remote_dir(path.parent)
                sftp.mkdir(str(path.as_posix()))

        print("Uploading to remote server...")
        for root, dirs, files in os.walk(src):
            relative_path = Path(root).relative_to(src)
            remote_dir = dst / relative_path

            ensure_remote_dir(remote_dir)

            for file in files:
                local_file = Path(root) / file
                remote_file = remote_dir / file
                print(f"Uploading {local_file} to {remote_file}")
                sftp.put(str(local_file), str(remote_file.as_posix()),confirm=True)
        print(f"Upload Success: {dst}")

    else:
        print("Copying to local...")
        shutil.copytree(src, dst, dirs_exist_ok=True)
# endregion


async def get_hardware_performance(DESIGN_NAME: DesignName, DESIGNS_DIR:Path, SYNTHESIS_DIR: Path, is_remote: bool, hostname:str, username:str, password:str)->HardwarePerformance:
    area = 0
    delay = 0
    power = 0

    if is_remote:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, username=username, password=password)
        sftp = ssh_client.open_sftp()
        
        upload_design_dir(DESIGNS_DIR/DESIGN_NAME, SYNTHESIS_DIR/DESIGN_NAME/'rtl_design', is_remote=is_remote, sftp=sftp)
        sftp.stat(str((SYNTHESIS_DIR/DESIGN_NAME/'rtl_design').as_posix()))
        stdin, stdout, stderr = ssh_client.exec_command(f"cd {SYNTHESIS_DIR} && dc_shell -x 'set ::CURRENT_DESIGN {DESIGN_NAME}' -f main.tcl")
        exit_status = stdout.channel.recv_exit_status()


        with sftp.open(f"{SYNTHESIS_DIR/DESIGN_NAME/'result'/f'{DESIGN_NAME}.area.log'}", "r") as f:
            for line in f.readlines()[21:]:
                if line[0:19] == "Combinational area:":
                    area = float(line.split()[-1])
                    break
        with sftp.open(f"{SYNTHESIS_DIR/DESIGN_NAME/'result'/f'{DESIGN_NAME}.max.timing.log'}", "r") as f:
            for line in f.readlines():
                if line[2:19] == "data arrival time":
                    delay = float(line.split()[-1])
                    break
        with sftp.open(f"{SYNTHESIS_DIR/DESIGN_NAME/'result'/f'{DESIGN_NAME}.power.log'}", "r") as f:
            power = float(f.readlines()[-2].split()[-2])
        sftp.close()
        ssh_client.close()
    return HardwarePerformance(area=area,delay=delay,power=power,PDAP=area*delay*power)