from .model import Multiplier
from typing import Any, Callable, Awaitable

type MetricName = str
from .accuracy import get_accuracy_performance
from .hardware import get_hardware_performance

evaluation_functions: dict[MetricName, Callable[[Multiplier], Awaitable[Any]]] = {
    "accuracy": get_accuracy_performance
}
