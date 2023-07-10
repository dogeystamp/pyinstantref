from typing import NewType
from pathlib import Path
from dataclasses import dataclass

# X11 window id
WindowId = NewType("WindowId", int)
# PID int
ProcessId = NewType("ProcessId", int)
# page number
PageNumber = NewType("PageNumber", int)


# reference to a specific page in a specific pdf
@dataclass
class Reference:
    filepath: Path
    page: PageNumber
