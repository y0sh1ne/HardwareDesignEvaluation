from typing import Protocol, TypedDict
from cocotb.handle import ModifiableObject, NonHierarchyObject

# Define the design interface
# The shown interface is an example for a multiplier, `a` and `b` are the inputs and `y` is the output
class DesignDut(Protocol):
    a: ModifiableObject
    b: ModifiableObject
    y: NonHierarchyObject

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