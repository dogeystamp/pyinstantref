from pathlib import Path
from datatypes import *
from typing import cast, Any
from util import rofi
import pydbus
import subprocess
import fitz


def get_section_pdf() -> PDFSection:
    page_ref: PDFPage = get_page_pdf()
    with fitz.Document(page_ref.filepath) as doc:
        toc = [FitzBookmark(*x) for x in cast(Any, doc).get_toc()]
        page_headers = [x for x in toc if x.page == page_ref.page]

        rofi_res = rofi([f"{x.title}" for x in page_headers], prompt="Select header: ")
        if rofi_res is None or rofi_res.index is None:
            raise RuntimeError("No header was selected.")
        selected_header = page_headers[rofi_res.index]

        return PDFSection(filepath=page_ref.filepath, title=selected_header.title)


def get_page_pdf() -> PDFPage:
    """Find current page of focused PDF reader window.

    Returns
    -------
    `PDFPage` reference to the current page.
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
            return get_page_zathura(pid)
        case "org.pwmt.zathura":
            return get_page_zathura(pid)
        case _:
            raise Exception(
                f"Can not retrieve pdf data from this type of window {wm_class}."
            )


def get_page_zathura(pid: ProcessId) -> PDFPage:
    """Given the PID of a Zathura instance, find which page of which file it's on.

    Parameters
    ----------
    pid
        Process ID of the Zathura instance to retrieve the reference from.

    Returns
    -------
    `PDFPage` that the Zathura instance is currently on.
    """

    bus = pydbus.SessionBus()
    obj = bus.get(f"org.pwmt.zathura.PID-{pid}", "/org/pwmt/zathura")

    filename: str = obj.filename
    # zathura returns 0-indexed pages
    pagenumber: PageNumber = obj.pagenumber + 1

    return PDFPage(filepath=Path(filename), page=pagenumber)
