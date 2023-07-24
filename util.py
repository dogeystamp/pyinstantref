import subprocess
import pydbus
from dataclasses import dataclass
from typing import Optional


@dataclass
class RofiResult:
    """Data returned from Rofi.

    Attributes
    ----------
    index
        Index within entries of the selected entry.
        `None` if nothing was selected.
    value
        Selected entry's string value.
        `None` if the value is not in the list or nothing was selected.
    custom_bind
        ID of custom bind used to select entry. None if no custom bind was used.
    """

    index: Optional[int]
    value: str
    custom_bind: Optional[int]


def rofi(
    entries: list[str], prompt: str = "> ", fuzzy=True, extra_args=[]
) -> Optional[RofiResult]:
    """Start a Rofi prompt.

    Returns
    -------
    None if the prompt was cancelled, or a `RofiResult`.
    """
    args = ["rofi", "-dmenu", "-sep", "\\0"]
    args += ["-p", prompt]

    if fuzzy:
        args += ["-matching", "fuzzy"]

    args += extra_args

    ret = RofiResult(None, "", None)

    res = subprocess.run(
        args, input="\0".join(entries), stdout=subprocess.PIPE, text=True
    )
    match res.returncode:
        case 0:
            pass
        case 1:
            return None
        case x if x >= 10 and x <= 28:
            ret.custom_bind = x - 9
        case _ as retc:
            raise RuntimeError(f"Rofi returned an unexpected return code `{retc}`.")
    ret.value = res.stdout.strip()
    try:
        ret.index = entries.index(ret.value)
    except ValueError:
        pass

    return ret


def notify(title: str, txt: str) -> None:
    """Send a text notification."""
    bus = pydbus.SessionBus()
    notifs = bus.get(".Notifications")
    notifs.Notify("instantref", 0, "dialog-information", title, txt, [], {}, 5000)
