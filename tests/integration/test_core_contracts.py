import subprocess
import sys
from typing import Any

from raceml.core.config import EstimatorConfig
from raceml.core.errors import UnsupportedCapabilityError
from raceml.core.protocols import ModelAdapter, ModelCapabilities
from raceml.core.registry import BackendSpec, Registry


class RecordingAdapter:
    def __init__(self, config: EstimatorConfig) -> None:
        self.config = config
        self.fit_arguments: tuple[Any, Any, dict[str, Any]] | None = None

    def fit(self, X: Any, y: Any, **kwargs: Any) -> None:
        self.fit_arguments = (X, y, kwargs)

    def predict(self, X: Any) -> Any:
        raise UnsupportedCapabilityError("This test adapter does not train a model")

    def get_params(self) -> dict[str, Any]:
        return self.config.get_params()

    def capabilities(self) -> ModelCapabilities:
        return {
            "predict_proba": False,
            "online_update": False,
            "warm_start": False,
            "full_retrain": False,
            "persistence": False,
        }

    def metadata(self) -> dict[str, Any]:
        return {"test_only": True, "task": self.config.task}


def test_configuration_registry_and_minimal_adapter_contract() -> None:
    created: list[RecordingAdapter] = []

    def factory(config: EstimatorConfig) -> ModelAdapter:
        adapter = RecordingAdapter(config)
        created.append(adapter)
        return adapter

    registry = Registry(
        [
            BackendSpec(
                algorithm="recording",
                task="classification",
                category="integrated",
                factory=factory,
            )
        ]
    )
    config = EstimatorConfig(
        algorithm="recording",
        task="classification",
        cpu_cores=2,
        random_state=42,
        backend_params={"n_estimators": 10},
    )
    assert registry.resolve("recording", "classification").category == "integrated"
    assert created == []
    adapter = registry.create(config)
    assert adapter is created[0]
    assert created[0].config is config
    assert created[0].fit_arguments is None
    assert adapter.get_params() == config.get_params()
    assert adapter.metadata() == {"test_only": True, "task": "classification"}

    X, y, validation_data = object(), object(), (object(), object())
    adapter.fit(X, y, validation_data=validation_data)
    assert created[0].fit_arguments == (X, y, {"validation_data": validation_data})
    assert not hasattr(adapter, "update")
    assert not hasattr(adapter, "predict_proba")
    assert not adapter.capabilities()["online_update"]


def test_core_import_and_inspection_do_not_import_backends_or_tuner() -> None:
    probe = """
import importlib.abc
import sys

blocked = (
    "numpy", "pandas", "polars", "pyarrow", "sklearn", "lightgbm", "xgboost",
    "catboost", "optuna", "raceml.automl",
)

class BlockOptionalImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if any(fullname == root or fullname.startswith(root + ".") for root in blocked):
            raise AssertionError("Unexpected optional import: " + fullname)
        return None

sys.meta_path.insert(0, BlockOptionalImports())
from raceml.core.config import EstimatorConfig
from raceml.core.registry import Registry
from raceml.core.errors import InvalidConfigurationError

config = EstimatorConfig(algorithm="example", task="classification", memory_limit="4GB")
assert config.get_params()["memory_limit"] == "4GB"
assert config.memory_budget_bytes == 4_000_000_000
try:
    Registry().resolve("example", "classification")
except InvalidConfigurationError:
    pass
else:
    raise AssertionError("An empty registry must not invent an adapter")
assert not any(name in sys.modules for name in blocked)
"""
    subprocess.run([sys.executable, "-I", "-B", "-c", probe], check=True)
