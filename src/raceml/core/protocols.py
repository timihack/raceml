"""Internal adapter contracts without optional backend imports."""

from typing import Any, Literal, Protocol, TypedDict

Task = Literal["classification", "regression"]
BackendKind = Literal["integrated", "native"]


class ModelCapabilities(TypedDict):
    predict_proba: bool
    online_update: bool
    warm_start: bool
    full_retrain: bool
    persistence: bool


class ModelAdapter(Protocol):
    def fit(self, X: Any, y: Any, **kwargs: Any) -> None: ...

    def predict(self, X: Any) -> Any: ...

    def get_params(self) -> dict[str, Any]: ...

    def capabilities(self) -> ModelCapabilities: ...

    def metadata(self) -> dict[str, Any]: ...
