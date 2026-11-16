from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from raceml.core.config import EstimatorConfig
from raceml.core.errors import InvalidConfigurationError


@pytest.mark.parametrize("value", [0, -1, True, False, 1.0, "4", None])
def test_invalid_cpu_cores(value: Any) -> None:
    with pytest.raises(InvalidConfigurationError, match="cpu_cores"):
        EstimatorConfig(algorithm="example", task="classification", cpu_cores=value)


@pytest.mark.parametrize("value", [-1, 2**32, True, False, 1.0, "42"])
def test_invalid_seed(value: Any) -> None:
    with pytest.raises(InvalidConfigurationError, match="random_state"):
        EstimatorConfig(algorithm="example", task="classification", random_state=value)


@pytest.mark.parametrize("value", [None, 0, 2**32 - 1])
def test_seed_boundaries(value: int | None) -> None:
    config = EstimatorConfig(
        algorithm="example", task="classification", random_state=value
    )
    assert config.get_params()["random_state"] == value


@pytest.mark.parametrize(
    ("limit", "expected"),
    [
        (None, None),
        ("1B", 1),
        ("1KB", 1000),
        ("1MB", 1000**2),
        ("4GB", 4 * 1000**3),
        ("1KiB", 1024),
        ("1MiB", 1024**2),
        (" 1 GiB ", 1024**3),
        ("1.5GiB", 3 * 1024**3 // 2),
        ("0.001KB", 1),
        ("0.0009765625KiB", 1),
        ("9007199254740993B", 9007199254740993),
    ],
)
def test_exact_observed_memory_budget(limit: str | None, expected: int | None) -> None:
    config = EstimatorConfig(algorithm="example", task="regression", memory_limit=limit)
    assert config.memory_budget_bytes == expected
    assert config.get_params()["memory_limit"] == limit


@pytest.mark.parametrize(
    "limit",
    [
        "",
        "4",
        "4gb",
        "4TB",
        "0B",
        "-1GB",
        "NaNGB",
        "infGB",
        "1e3B",
        "0.1B",
        "1.1KiB",
        "1 GB extra",
        1024,
        True,
    ],
)
def test_invalid_memory_budget(limit: Any) -> None:
    with pytest.raises(InvalidConfigurationError, match="memory_limit"):
        EstimatorConfig(algorithm="example", task="regression", memory_limit=limit)


@pytest.mark.parametrize("algorithm", [None, 1, "", " ", " example", "example "])
def test_invalid_algorithm_identifier(algorithm: Any) -> None:
    with pytest.raises(InvalidConfigurationError, match="algorithm"):
        EstimatorConfig(algorithm=algorithm, task="classification")


def test_unsupported_task() -> None:
    with pytest.raises(InvalidConfigurationError, match="task"):
        EstimatorConfig(algorithm="example", task="ranking")


@pytest.mark.parametrize(
    "params",
    [
        [],
        {1: "value"},
        {"": 1},
        {" name": 1},
        {"algorithm": "another"},
        {"cpu_cores": 4},
        {"memory_limit": "1GB"},
        {"random_state": 42},
    ],
)
def test_invalid_backend_parameter_container(params: Any) -> None:
    with pytest.raises(InvalidConfigurationError):
        EstimatorConfig(
            algorithm="example", task="classification", backend_params=params
        )


def test_requested_configuration_snapshot_and_round_trip() -> None:
    nested = {"class-a": 2.0}
    parameters = {"n_estimators": 7, "class_weight": nested}
    config = EstimatorConfig(
        algorithm="example",
        task="classification",
        cpu_cores=2,
        memory_limit="1GB",
        random_state=42,
        backend_params=parameters,
    )
    parameters["n_estimators"] = 999
    requested = config.get_params()
    assert requested == {
        "algorithm": "example",
        "cpu_cores": 2,
        "memory_limit": "1GB",
        "random_state": 42,
        "n_estimators": 7,
        "class_weight": nested,
    }
    assert requested["class_weight"] is nested
    reconstructed = EstimatorConfig(
        task="classification",
        algorithm=requested.pop("algorithm"),
        cpu_cores=requested.pop("cpu_cores"),
        memory_limit=requested.pop("memory_limit"),
        random_state=requested.pop("random_state"),
        backend_params=requested,
    )
    assert reconstructed.get_params() == config.get_params()
    requested["n_estimators"] = 1000
    assert config.get_params()["n_estimators"] == 7
    assert reconstructed.get_params()["n_estimators"] == 7
    with pytest.raises(TypeError):
        config.backend_params["n_estimators"] = 8
    with pytest.raises(FrozenInstanceError):
        config.cpu_cores = 8


def test_configuration_repr_does_not_render_backend_objects() -> None:
    class PrivateObject:
        def __repr__(self) -> str:
            raise AssertionError("Backend objects must not be rendered")

    config = EstimatorConfig(
        algorithm="example",
        task="classification",
        backend_params={"callback": PrivateObject()},
    )
    assert "callback" not in repr(config)
