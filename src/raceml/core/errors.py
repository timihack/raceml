"""Typed failures shared by the estimator and adapter contracts."""


class InvalidConfigurationError(ValueError):
    """Requested configuration is invalid or cannot be resolved."""


class DataSchemaError(ValueError):
    """Prepared inputs do not satisfy the declared schema."""


class BackendUnavailableError(ImportError):
    """A selected adapter's declared dependency is unavailable."""


class NotFittedError(RuntimeError):
    """An operation requires a successful fit."""


class UnsupportedCapabilityError(NotImplementedError):
    """The selected adapter does not implement the requested operation."""


class UnsupportedUpdateError(UnsupportedCapabilityError):
    """The selected adapter cannot perform a true online update."""
