from model import DesignDut
from typing import Any, Callable, Awaitable

type MetricName = str
from accuracy import get_accuracy

evaluation_functions: dict[MetricName, Callable[[DesignDut], Awaitable[Any]]] = {
    "accuracy": get_accuracy
}
