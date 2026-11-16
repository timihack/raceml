"""Requested estimator settings, independent of backend installation."""

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from fractions import Fraction
from types import MappingProxyType
from typing import Any

from raceml.core.errors import InvalidConfigurationError
from raceml.core.protocols import Task

_MEMORY_PATTERN = re.compile(r"([0-9]+(?:\.[0-9]+)?)[ \t]*(B|KB|MB|GB|KiB|MiB|GiB)")
_MEMORY_UNITS = {
    "B": 1,
    "KB": 1000,
    "MB": 1000**2,
    "GB": 1000**3,
    "KiB": 1024,
    "MiB": 1024**2,
    "GiB": 1024**3,
}
_RESERVED_PARAMS = frozenset({"algorithm", "cpu_cores", "memory_limit", "random_state"})


def _memory_budget_bytes(limit: str | None) -> int | None:
    if limit is None:
        return None
    if not isinstance(limit, str):
        raise InvalidConfigurationError("memory_limit must be a string or None.")
    match = _MEMORY_PATTERN.fullmatch(limit.strip())
    if match is None:
        raise InvalidConfigurationError(
            "memory_limit needs a positive decimal quantity and a supported byte unit."
        )
    try:
        budget = Fraction(match[1]) * _MEMORY_UNITS[match[2]]
    except ValueError as exc:
        raise InvalidConfigurationError("Invalid memory_limit quantity.") from exc
    if budget <= 0 or budget.denominator != 1:
        raise InvalidConfigurationError(
            "memory_limit must resolve to a positive whole number of bytes."
        )
    return budget.numerator


@dataclass(frozen=True, slots=True, kw_only=True)
class EstimatorConfig:
    algorithm: str
    task: Task
    cpu_cores: int = 1
    memory_limit: str | None = None
    random_state: int | None = None
    backend_params: Mapping[str, Any] = field(default_factory=dict, repr=False)
    memory_budget_bytes: int | None = field(init=False)

    def __post_init__(self) -> None:
        if (
            not isinstance(self.algorithm, str)
            or not self.algorithm
            or self.algorithm != self.algorithm.strip()
        ):
            raise InvalidConfigurationError("algorithm must be an explicit identifier.")
        if self.task not in ("classification", "regression"):
            raise InvalidConfigurationError("Unsupported estimator task.")
        if (
            not isinstance(self.cpu_cores, int)
            or isinstance(self.cpu_cores, bool)
            or self.cpu_cores <= 0
        ):
            raise InvalidConfigurationError("cpu_cores must be a positive integer.")
        if self.random_state is not None and (
            not isinstance(self.random_state, int)
            or isinstance(self.random_state, bool)
            or not 0 <= self.random_state < 2**32
        ):
            raise InvalidConfigurationError(
                "random_state must be None or an integer in [0, 2**32 - 1]."
            )
        if not isinstance(self.backend_params, Mapping):
            raise InvalidConfigurationError("backend_params must be a mapping.")
        if any(
            not isinstance(name, str) or not name or name != name.strip()
            for name in self.backend_params
        ):
            raise InvalidConfigurationError(
                "Backend parameter names must be nonempty strings without outer spaces."
            )
        if _RESERVED_PARAMS.intersection(self.backend_params):
            raise InvalidConfigurationError(
                "Backend parameters cannot replace RaceML constructor settings."
            )
        object.__setattr__(
            self, "memory_budget_bytes", _memory_budget_bytes(self.memory_limit)
        )
        object.__setattr__(
            self, "backend_params", MappingProxyType(dict(self.backend_params))
        )

    def get_params(self) -> dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "cpu_cores": self.cpu_cores,
            "memory_limit": self.memory_limit,
            "random_state": self.random_state,
            **self.backend_params,
        }
