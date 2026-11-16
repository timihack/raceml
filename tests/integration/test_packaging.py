import os
import re
import shutil
import subprocess
import sys
import tarfile
import tomllib
import zipfile
from collections import defaultdict
from email.parser import BytesParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]


@pytest.mark.parametrize(
    ("path", "ignored"),
    [
        ("src/raceml/models/_ignore_probe.py", False),
        ("src/raceml/input/_ignore_probe.py", False),
        ("data/_ignore_probe.csv", True),
        ("datasets/_ignore_probe.csv", True),
        ("artifacts/_ignore_probe.bin", True),
        ("models/_ignore_probe.bin", True),
        ("benchmark-results/_ignore_probe.json", True),
    ],
)
def test_artifact_ignore_boundaries(path: str, ignored: bool) -> None:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", path],
        cwd=ROOT,
        check=False,
    )
    assert result.returncode in (0, 1)
    assert (result.returncode == 0) == ignored


@pytest.fixture(params=["*.whl", "*.tar.gz"])
def artifact(request: pytest.FixtureRequest) -> Path:
    directory = os.environ.get("RACEML_DIST_DIR")
    if directory is None:
        pytest.skip("Set RACEML_DIST_DIR after uv build to test distribution artifacts")
    candidates = list(Path(directory).resolve().glob(request.param))
    assert len(candidates) == 1, f"Expected one {request.param} in {directory}"
    return candidates[0]


def test_distribution_metadata_and_notices(artifact: Path) -> None:
    if artifact.suffix == ".whl":
        with zipfile.ZipFile(artifact) as wheel:
            metadata_paths = [
                name
                for name in wheel.namelist()
                if name.endswith(".dist-info/METADATA")
            ]
            assert len(metadata_paths) == 1
            metadata_bytes = wheel.read(metadata_paths[0])
            licenses = {
                Path(name).name: wheel.read(name)
                for name in wheel.namelist()
                if ".dist-info/licenses/" in name and not name.endswith("/")
            }
    else:
        with tarfile.open(artifact) as sdist:
            metadata_members = [
                member
                for member in sdist.getmembers()
                if member.name.endswith("/PKG-INFO") and member.name.count("/") == 1
            ]
            assert len(metadata_members) == 1
            metadata_file = sdist.extractfile(metadata_members[0])
            assert metadata_file is not None
            metadata_bytes = metadata_file.read()
            licenses = {}
            for member in sdist.getmembers():
                if member.name.count("/") == 1 and Path(member.name).name in {
                    "LICENSE",
                    "NOTICE",
                }:
                    license_file = sdist.extractfile(member)
                    assert license_file is not None
                    licenses[Path(member.name).name] = license_file.read()

    metadata = BytesParser().parsebytes(metadata_bytes)
    assert metadata["Name"] == "raceml"
    assert metadata["Version"] == PROJECT["version"]
    assert metadata["Requires-Python"] == PROJECT["requires-python"]
    assert metadata["License-Expression"] == "Apache-2.0"
    assert set(metadata.get_all("License-File", [])) == {"LICENSE", "NOTICE"}
    for name in ("LICENSE", "NOTICE"):
        assert licenses[name] == (ROOT / name).read_bytes()

    core = set()
    extras = defaultdict(set)
    for requirement in metadata.get_all("Requires-Dist", []):
        dependency, _, marker = requirement.partition(";")
        if not marker:
            core.add(dependency.strip())
        else:
            extra = re.fullmatch(r"\s*extra == ['\"]([\w-]+)['\"]\s*", marker)
            assert extra is not None, requirement
            extras[extra[1]].add(dependency.strip())
    assert core == {"numpy>=1.26"}
    assert extras == {
        extra: set(requirements)
        for extra, requirements in PROJECT["optional-dependencies"].items()
    }
    assert set(metadata.get_all("Provides-Extra", [])) == set(extras)


def test_isolated_artifact_install(artifact: Path, tmp_path: Path) -> None:
    uv = shutil.which("uv")
    assert uv is not None, "uv is required for the opt-in packaging checks"
    environment = tmp_path / "environment"
    subprocess.run(
        [uv, "venv", "--python", sys.executable, str(environment)],
        cwd=tmp_path,
        check=True,
    )
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run(
        [uv, "pip", "install", "--python", str(python), str(artifact)],
        cwd=tmp_path,
        check=True,
    )
    probe = """
import importlib.metadata
import importlib.util
from pathlib import Path
import sys
import raceml
import raceml.core.config
from raceml.core.config import EstimatorConfig
from raceml.core.errors import InvalidConfigurationError
from raceml.core.registry import Registry

assert Path(raceml.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
assert Path(raceml.core.config.__file__).resolve().is_relative_to(
    Path(sys.prefix).resolve()
)
assert importlib.metadata.version("raceml") == sys.argv[1]
config = EstimatorConfig(algorithm="example", task="classification", memory_limit="4GB")
assert config.memory_budget_bytes == 4_000_000_000
try:
    Registry().create(config)
except InvalidConfigurationError:
    pass
else:
    raise AssertionError("An unregistered algorithm must not resolve")
for name in (
    "sklearn", "lightgbm", "xgboost", "catboost",
    "optuna", "pandas", "polars", "pyarrow",
):
    assert importlib.util.find_spec(name) is None, name
    assert name not in sys.modules, name
assert importlib.util.find_spec("numpy") is not None
"""
    subprocess.run(
        [str(python), "-I", "-c", probe, PROJECT["version"]],
        cwd=tmp_path,
        check=True,
    )
