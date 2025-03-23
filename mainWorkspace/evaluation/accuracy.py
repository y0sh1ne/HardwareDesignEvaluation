from .model import DesignDut, AccuracyPerformance
from cocotb.triggers import Timer
from decimal import Decimal

async def get_accuracy(dut: DesignDut)->AccuracyPerformance:
    VALUE_RANGE = 256
    MAX_VALUE = VALUE_RANGE-1
    EXACT = [[i*j for j in range(VALUE_RANGE)] for i in range(VALUE_RANGE)]
    approx_result = [[0]*VALUE_RANGE for _ in range(VALUE_RANGE)]
    for i in range(VALUE_RANGE):
        for j in range(VALUE_RANGE):
            dut.a.value = i
            dut.b.value = j
            await Timer(Decimal(2), units="ns")
            approx_result[i][j] = int(dut.y.value) # type: ignore
    NMED = sum(abs(EXACT[i][j]-approx_result[i][j]) for i in range(VALUE_RANGE) for j in range(VALUE_RANGE))/(MAX_VALUE*MAX_VALUE*VALUE_RANGE*VALUE_RANGE)
    MRED = sum(abs(EXACT[i][j]-approx_result[i][j])/EXACT[i][j] for i in range(1,VALUE_RANGE) for j in range(1,VALUE_RANGE))/(MAX_VALUE*MAX_VALUE)
    return AccuracyPerformance(NMED=NMED,MRED=MRED)