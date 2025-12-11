from .addons import DefaultAddons
from .async_api import AsyncCamoufox, AsyncNewBrowser
from .sync_api import Camoufox, NewBrowser
from .utils import launch_options
from .realistic_input import RealisticKeyboard, type_realistic

__all__ = [
    "Camoufox",
    "NewBrowser",
    "AsyncCamoufox",
    "AsyncNewBrowser",
    "DefaultAddons",
    "launch_options",
    "RealisticKeyboard",
    "type_realistic",
]
