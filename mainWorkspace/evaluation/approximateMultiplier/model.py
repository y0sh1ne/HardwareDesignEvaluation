from typing import Protocol, TypedDict
from cocotb.handle import ModifiableObject, NonHierarchyObject
from cocotb.triggers import Timer
from decimal import Decimal

# Define the design interface
# The shown interface is an example for a multiplier, `a` and `b` are the inputs and `y` is the output
class MultiplierDut(Protocol):
    a: ModifiableObject
    b: ModifiableObject
    lsb: ModifiableObject
    y: NonHierarchyObject

class Multiplier:
    dut: MultiplierDut
    def __init__(self, dut:MultiplierDut):
        self.dut=dut

    type uint8 = int
    async def compute(self, a:uint8, b:uint8)-> int:
        self.dut.a.value=a
        self.dut.b.value=b
        await Timer(Decimal(2), units="ns")
        return int(self.dut.y.value) # type: ignore

# Define the performance metrics
class AccuracyPerformance(TypedDict):
    NMED:float
    MRED:float

class HardwarePerformance(TypedDict):
    area: float
    delay: float
    power: float
    PDAP: float

class Performance(TypedDict):
    accuracy: AccuracyPerformance
    hardware: HardwarePerformance

type DesignName = str
type AllPerformance = dict[DesignName,Performance]
