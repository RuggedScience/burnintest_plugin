import importlib.metadata

# 1. Fetch dynamic version from hatch-vcs
try:
    __version__ = importlib.metadata.version("burnintest-plugin")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0.dev0"

# 2. Import your public classes and enums from your internal modules
from .bitinterface import BitInterface, PluginStatus, ErrorSeverity

# 3. Explicitly declare your Public API
__all__ = [
    "__version__",
    "BitInterface",
    "PluginStatus",
    "ErrorSeverity",
]