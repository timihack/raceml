"""Internal immutable adapter lookup; no production adapters are registered yet."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType

from raceml.core.config import EstimatorConfig
from raceml.core.errors import BackendUnavailableError, InvalidConfigurationError
from raceml.core.protocols import BackendKind, ModelAdapter, Task


@dataclass(frozen=True, slots=True, kw_only=True)
class BackendSpec:
    algorithm: str
    task: Task
    category: BackendKind
    factory: Callable[[EstimatorConfig], ModelAdapter] = field(repr=False)
    dependency_module: str | None = None
    installation_extra: str | None = None


class Registry:
    def __init__(self, entries: Sequence[BackendSpec] = ()) -> None:
        specifications: dict[tuple[str, Task], BackendSpec] = {}
        for entry in entries:
            key = (entry.algorithm, entry.task)
            if key in specifications:
                raise InvalidConfigurationError(
                    "Duplicate backend specification for algorithm and task."
                )
            specifications[key] = entry
        self._entries = MappingProxyType(specifications)

    def resolve(self, algorithm: str, task: Task) -> BackendSpec:
        try:
            return self._entries[(algorithm, task)]
        except KeyError:
            raise InvalidConfigurationError(
                "No implemented adapter is registered for the requested algorithm/task."
            ) from None

    def create(self, config: EstimatorConfig) -> ModelAdapter:
        specification = self.resolve(config.algorithm, config.task)
        try:
            return specification.factory(config)
        except ModuleNotFoundError as exc:
            if (
                specification.dependency_module is None
                or exc.name != specification.dependency_module
            ):
                raise
            if specification.installation_extra is None:
                guidance = "Install the adapter's declared optional dependency."
            else:
                guidance = (
                    "Install the optional dependency with "
                    f"pip install 'raceml[{specification.installation_extra}]'."
                )
            raise BackendUnavailableError(guidance) from exc
