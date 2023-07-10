#!/usr/bin/env python3

from pdf_data import get_metadata_pdf
from datatypes import *
from enum import Enum, auto
from os import environ
from urllib.parse import urlencode
import subprocess


class LinkFormat(Enum):
    TYPST = auto()


def clip_copy(txt: str):
    try:
        subprocess.run(["xsel", "-ib"], text=True, input=txt)
    except OSError as e:
        raise Exception("Please install `xsel`.") from e


def format_typst(ref: Reference) -> str:
    path_str = environ.get("TYPST_ROOT", None)
    if path_str is None:
        raise KeyError("Please set TYPST_ROOT to format links with Typst.")
    typst_root = Path(path_str)

    relative: bool = ref.filepath.is_relative_to(typst_root)
    format_path: str

    if relative:
        format_path = "/" + str(ref.filepath.relative_to(typst_root))
    else:
        format_path = str(ref.filepath.absolute())

    params = dict(page=ref.page)

    if relative:
        return f'#lref("{format_path}?{urlencode(params)}", pdfref: true)[]'
    else:
        return f'#link("pdfref://{format_path}?{urlencode(params)}")[]'


def copy_ref(ref: Reference, format: LinkFormat) -> None:
    """Formats Reference and copies it to clipboard."""
    match format:
        case LinkFormat.TYPST:
            link_txt = format_typst(ref)

    clip_copy(link_txt)


if __name__ == "__main__":
    ref = get_metadata_pdf()

    format = LinkFormat.TYPST
    copy_ref(ref, format)
