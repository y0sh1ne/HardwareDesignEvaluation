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
│   ├── performanceUpdate.py   # The main file to run
│   ├── README.md
│   ├── requirements.txt
│   ├── config                  # config files
│   │   ├── ...
│   │
│   ├── evaluation
│   │   ├── ...
│   │
│   ├── verilogDesigns
│       ├── MY_DESIGN1           # Your design file (verilog)
│           ├── MY_DESIGN.v
│           ├── ...
│
├── synopsysWorkspace
    ├── main.tcl                # the tcl file to run synthesis
    ├── main.sdc                # the sdc file
    ├── MY_DESIGN1
    │   ├── rtl_design          
    │   │   ├── MY_DESIGN.v
    │   │   ├── ...
    │   │
    │   ├── results             # the directory to store the synthesis result
    │       ├── xxx.log
    │       ├── ...
    │
    ├── MY_DESIGN2
    ├── ...

```

## How to use

The guide will be introduced under the assumption that your Synopsys is installed on remote server.

### 1. synopsysWorkspace
- Download the synopsysWorkspace directory on your remote server.

### 2. mainWorkspace
- **Install**: Download the mainWorkspace directory on your local server.
- **Config**: Modify the parameters in `mainWorkspace/config` according to your environment.
  - Give the design name (for example, `MY_DESIGN1`) in `mainWorkspace/config/design.py`.
  - If you want to use the synopsys, modify the parameters in `mainWorkspace/config/synopsys.python` according to your environment.
- **Write Your Verilog**: Make directory in `mainWorkspace/verilogDesigns` and put your design file in it. The directory name, main verilog file name and the top module name should be the same. 
    > For example, if your design is `MY_DESIGN1.v`, the directory name should be `MY_DESIGN1` and the top module name in `MY_DESIGN1.v` should be `MY_DESIGN1`.
- **Define your Metric Function**:
  - create a directory in `mainWorkspace/evaluation` and name it as your design name (for example, `MY_DESIGN1`).
  - Create `model.py`, `__init__.py`, `{metricName}.py`.
    - `model.py` is the file to define your design structure and performance metric structure.
    - define the function with type `Callable[[MyDesin], Awaitable[Any]]` to calculate metric in `{metricName}.py`.
    - define a evaluation_function_list of the functions in `{metricName}.py`s in `__init__.py`, use loop to call the functions in `mainWorkspace/performanceUpdate.py`.
- **Get the Result** Run `mainWorkspace/performanceUpdate.py`.

> `mainWorkspace/evaluation/approximateMultiplier` is an example of how to define the metric functions and Design Structures.