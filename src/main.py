from xcore.sdk import AutoDispatchMixin, action, ok
from .ipc import IPCCommands
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

class Plugin(IPCCommands):
    pass
