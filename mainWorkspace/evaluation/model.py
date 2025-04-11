from typing import TypedDict

class HardwarePerformance(TypedDict):
    area: float
    delay: float
    power: float
    PDAP: float

type DesignName = str