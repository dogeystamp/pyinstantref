from os import environ
from urllib.parse import urlencode
from datatypes import PDFPage, PDFSection, PDFReference, Reference
from typing import assert_never
from pathlib import Path

def format_pdf_link(ref: PDFReference) -> str:
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

    params = {}

    match ref:
        case PDFPage():
            params["page"] = ref.page
        case PDFSection():
            params["section"] = ref.title
        case _ as obj:
            assert_never(obj)

    if relative:
        return f'#lref("{format_path}?{urlencode(params)}", pdfref: true)[]'
    else:
        return f'#link("pdfref://{format_path}?{urlencode(params)}")[]'

def ref(ref: Reference) -> str:
    """Formats a Reference."""

    # for now no other types are implemented
    # replace this with a match/case when that happens
    return format_pdf_link(ref)
