from typing import Any

import pytest

from raceml.core.config import EstimatorConfig
from raceml.core.errors import (
    BackendUnavailableError,
    InvalidConfigurationError,
    UnsupportedCapabilityError,
)
from raceml.core.protocols import ModelAdapter
from raceml.core.registry import BackendSpec, Registry


def never_build(config: EstimatorConfig) -> ModelAdapter:
    raise AssertionError("Resolving a descriptor must not construct an adapter")


def specification(**kwargs: Any) -> BackendSpec:
    return BackendSpec(
        algorithm="example",
        task="classification",
        category="integrated",
        factory=never_build,
        **kwargs,
    )


def test_resolution_is_lazy_and_task_specific() -> None:
    classifier = specification()
    regressor = BackendSpec(
        algorithm="example",
        task="regression",
        category="integrated",
        factory=never_build,
    )
    entries = [classifier, regressor]
    registry = Registry(entries)
    entries.clear()
    assert registry.resolve("example", "classification") is classifier
    assert registry.resolve("example", "regression") is regressor


def test_duplicate_entry_is_rejected() -> None:
    entry = specification()
    with pytest.raises(InvalidConfigurationError, match="Duplicate"):
        Registry([entry, entry])


@pytest.mark.parametrize(
    ("algorithm", "task"),
    [("unknown", "classification"), ("example", "regression")],
)
def test_unknown_algorithm_and_task_mismatch(algorithm: str, task: Any) -> None:
    registry = Registry([specification()])
    config = EstimatorConfig(algorithm=algorithm, task=task)
    with pytest.raises(InvalidConfigurationError, match="No implemented adapter"):
        registry.create(config)


def test_empty_registry_does_not_advertise_a_real_backend() -> None:
    with pytest.raises(InvalidConfigurationError):
        Registry().resolve("lightgbm", "classification")


def test_declared_missing_backend_has_guidance_without_fallback() -> None:
    calls = []
    missing = ModuleNotFoundError("Missing test dependency", name="example_backend")

    def unavailable(config: EstimatorConfig) -> ModelAdapter:
        calls.append(config)
        raise missing

    entry = BackendSpec(
        algorithm="example",
        task="classification",
        category="integrated",
        factory=unavailable,
        dependency_module="example_backend",
        installation_extra="example-extra",
    )
    config = EstimatorConfig(algorithm="example", task="classification")
    registry = Registry([entry])
    with pytest.raises(
        BackendUnavailableError, match=r"raceml\[example-extra\]"
    ) as err:
        registry.create(config)
    assert err.value.__cause__ is missing
    assert calls == [config]


def test_missing_dependency_without_an_extra_has_generic_guidance() -> None:
    def unavailable(config: EstimatorConfig) -> ModelAdapter:
        raise ModuleNotFoundError(name="example_backend")

    registry = Registry(
        [
            BackendSpec(
                algorithm="example",
                task="classification",
                category="integrated",
                factory=unavailable,
                dependency_module="example_backend",
            )
        ]
    )
    with pytest.raises(BackendUnavailableError, match="declared optional dependency"):
        registry.create(EstimatorConfig(algorithm="example", task="classification"))


@pytest.mark.parametrize(
    "failure",
    [
        ModuleNotFoundError("Transitive failure", name="unrelated_dependency"),
        ModuleNotFoundError("Internal module failure", name="example_backend.internal"),
        ImportError("Broken extension"),
        RuntimeError("Factory bug"),
        UnsupportedCapabilityError("Unverified backend version"),
    ],
)
def test_other_factory_failures_are_not_disguised(failure: Exception) -> None:
    def failed(config: EstimatorConfig) -> ModelAdapter:
        raise failure

    registry = Registry(
        [
            BackendSpec(
                algorithm="example",
                task="classification",
                category="integrated",
                factory=failed,
                dependency_module="example_backend",
                installation_extra="example-extra",
            )
        ]
    )
    with pytest.raises(type(failure)) as err:
        registry.create(EstimatorConfig(algorithm="example", task="classification"))
    assert err.value is failure
