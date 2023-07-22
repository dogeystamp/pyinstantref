from typing import NewType, Union
from pathlib import Path
from dataclasses import dataclass

# X11 window id
WindowId = NewType("WindowId", int)
# PID int
ProcessId = NewType("ProcessId", int)


@dataclass
class _Reference:
    """Reference to a location within a file."""
    pass


@dataclass
class _PDFReference(_Reference):
    """Reference to a location within a PDF file.

    Attributes
    ----------
    filepath
        Path of the relevant PDF file.
    """

    filepath: Path


PageNumber = NewType("PageNumber", int)


@dataclass
class PDFPage(_PDFReference):
    """Reference to a specific page in a PDF.

    Attributes
    ----------
    page
        Page number.
    """

    page: PageNumber


SectionTitle = NewType("SectionTitle", str)


@dataclass
class PDFSection(_PDFReference):
    """Reference to a specific section title in a PDF.

    Attributes
    ----------
    title
        Section title.
    """

    title: SectionTitle


PDFReference = Union[PDFPage, PDFSection]
# for now no other format is implemented
# replace this with an union if that happens
Reference = PDFReference
