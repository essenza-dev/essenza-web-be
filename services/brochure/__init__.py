"""Brochure service module."""

from .dto import CreateBrochureDTO, UpdateBrochureDTO, UploadBrochureFileDTO
from .service import BrochureService

__all__ = [
    "CreateBrochureDTO",
    "UpdateBrochureDTO",
    "UploadBrochureFileDTO",
    "BrochureService",
]