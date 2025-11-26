from dataclasses import dataclass, fields, field
from typing import Any, Dict


@dataclass
class BaseDTO:
    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO object to dictionary, handling file uploads safely."""
        result = {}
        for field_info in fields(self):
            value = getattr(self, field_info.name)
            result[field_info.name] = value
        return result


__all__ = ["BaseDTO", "dataclass", "field"]
