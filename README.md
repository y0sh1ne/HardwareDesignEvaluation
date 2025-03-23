# HardwareDesignEvaluation

HardwareDesignEvaluation is a python project for calculate the metric of hardware design written in HardwareDesignLanguage.(Only support verilog now)


## Features
- Get hardware performance metric of design through synopsys.
- Get customized metric of design through custom defined function.

## Requirements (My Environment)
- remoteWorkspace
    - Linux version 3.10.0-1160.81.1.el7.x86_64 (mockbuild@kbuilder.bsys.centos.org) (gcc version 4.8.5 20150623 (Red Hat 4.8.5-44) (GCC) )
    - dc_shell version    -  R-2020.09-SP4
- mainWorkspace
    - Ubuntu 22.04 LTS
    - Python 3.13 (library requirement in `mainWorkspace/requirements.txt`)
    - verilator v5.032 (Must, because of the python library `cocotb`)

## Structure
```
.
├── README.md
├── mainWorkspace
│   ├── performance.json       # The performance metric of design
|   ├── performanceUpdate.py   # The main file to run
│   ├── README.md
│   ├── requirements.txt
|   ├── config                  # config files
|   |   ├── ...
│   ├── evaluation
|   |   ├── ...
│   ├── verilogDesigns          # Your design file (verilog)
|   |   ├── MY_DESIGN.v
|   |   ├── ...
├── synopsysWorkspace
│   ├── README.md               # How to use synopsysWorkspace
│   ├── rtl_design          
|   |   ├── MY_DESIGN.v         # Your design file (verilog)
|   |   ├── ...
|   ├── synthesis               # run dc_shell here
|   |   ├── sdc
|   |   |   ├── main.sdc        # the sdc file
|   |   ├── tcl
|   |   |   ├── main.tcl        # the tcl file which really works
|   |   |   ├── MY_DESIGN.tcl   # tcl to define the DESIGN_NAME and call the main.tcl
|   |   |   ├── ...
|   |   ├── MY_DESIGN           # the directory to store the synthesis result
|   |   |   ├── xxx.log
|   |   |   ├── ...

```

## How to use

The guide will be introduced under the assumption that your Synopsys is installed on remote server.

### 1. synopsysWorkspace
- Download the synopsysWorkspace directory on your remote server.
- Put your design file in `rtl_design` directory. Make sure the design file is named as `MY_DESIGN.v` and the module name is `MY_DESIGN`.
- Create a tcl file named `MY_DESIGN.tcl` in `synopsysWorkspce/synthesis/tcl` directory. The content of `MY_DESIGN.tcl` should be like:
    ```tcl
    set ::CURRENT_DESIGN "MY_DESIGN"
    source tcl/main.tcl
    ```
- Modify the parameters like library and path in file `synopsysWorkspace/synthesis/tclmain.tcl` according to your environment.
- Run the following command to start synthesis:
    ```bash
    cd synopsysWorkspace/synthesis
    dc_shell -f tcl/MY_DESIGN.tcl
    ```
- After the synthesis is done, you can find the synthesis result in `synopsysWorkspace/synthesis/MY_DESIGN` directory.

### 2. mainWorkspace
- Download the mainWorkspace directory on your local server.
- Modify the parameters in `mainWorkspace/config` according to your environment.
- Define your structure of `DesignDut` and `Performance` in `mainWorkspace/evaluation/model.py`.
    - `DesignDut` is the structure of your design. A DesignDut for Multiplier is defined in `mainWorkspace/evaluation/model.py` as an example.
    - `Performance` is the structure of the performance metric of your design. A Performance for Multiplier is defined in `mainWorkspace/evaluation/model.py` as an example.
- Write your evaluation function in `mainWorkspace/evaluation` directory. `mainWorkspace/evaluation/accuracy.py` is an example.
- Run `mainWorkspace/performanceUpdate.py`.

