from pathlib import Path
from datatypes import *
import pydbus
import subprocess


def get_metadata_pdf() -> Reference:
    """Find current page of focused PDF reader window.

    Returns
    -------
    `Reference` to the current page, or None if not found.
    """
    try:
        res = subprocess.run(
            ["xdotool", "getactivewindow"], capture_output=True, text=True
        )
        window_id: WindowId = WindowId(int(res.stdout))
        res = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowpid"],
            capture_output=True,
            text=True,
        )
        pid: ProcessId = ProcessId(int(res.stdout))
    except OSError as e:
        raise Exception("Please install `xdotool`.") from e
    except subprocess.CalledProcessError as e:
        raise Exception(
            "Could not get current active window ID. Is a window focused right now?"
        )

    try:
        res = subprocess.run(
            ["xprop", "-id", str(window_id), "WM_CLASS"], capture_output=True, text=True
        )
        # WM_CLASS(STRING) = "org.pwmt.zathura", "Zathura"
        wm_class: list[str] = [
            i.strip('"\n') for i in res.stdout.split(" = ")[-1].split(", ")
        ]
    except OSError as e:
        raise Exception("Please install `xprop`.") from e
    except subprocess.CalledProcessError as e:
        raise Exception("Could not get focused window class.") from e

    match wm_class[0]:
        case "Zathura":
            return get_metadata_zathura(pid)
        case "org.pwmt.zathura":
            return get_metadata_zathura(pid)
        case _:
            raise Exception(
                f"Can not retrieve pdf data from this type of window {wm_class}."
            )


def get_metadata_zathura(pid: ProcessId) -> Reference:
    """Given the PID of a Zathura instance, find which page of which file it's on.

    Parameters
    ----------
    pid
        Process ID of the Zathura instance to retrieve the reference from.

    Returns
    -------
    `Reference` that the Zathura instance is currently on
    """

    bus = pydbus.SessionBus()
    obj = bus.get(f"org.pwmt.zathura.PID-{pid}", "/org/pwmt/zathura")

    filename: str = obj.filename
    # zathura returns 0-indexed pages
    pagenumber: PageNumber = obj.pagenumber + 1

    return Reference(filepath=Path(filename), page=pagenumber)
