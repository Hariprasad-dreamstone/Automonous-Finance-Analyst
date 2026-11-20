"""Data loading and validation.

Rows are validated with Pydantic. Missing or invalid values are kept as None
(and reported) instead of being guessed, so downstream code can refuse to
answer rather than invent a number.
"""
import csv
import re
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, field_validator

REQUIRED_COLUMNS = {
    "quarter",
    "marketing_spend",
    "new_customers",
    "lifespan_months",
    "monthly_revenue_per_user",
}
QUARTER_PATTERN = re.compile(r"^\d{4}Q[1-4]$")


class SchemaError(ValueError):
    """Raised when the file itself is unusable (e.g. missing columns)."""


class QuarterRecord(BaseModel):
    quarter: str
    marketing_spend: Optional[float] = None
    new_customers: Optional[int] = None
    lifespan_months: Optional[float] = None
    monthly_revenue_per_user: Optional[float] = None

    @field_validator("quarter")
    @classmethod
    def check_quarter(cls, value: str) -> str:
        value = value.strip().upper()
        if not QUARTER_PATTERN.match(value):
            raise ValueError(f"quarter must look like 2025Q1, got {value!r}")
        return value

    @field_validator(
        "marketing_spend", "new_customers", "lifespan_months",
        "monthly_revenue_per_user", mode="before",
    )
    @classmethod
    def blank_to_none(cls, value):
        if value is None:
            return None
        if isinstance(value, str) and value.strip() == "":
            return None
        return value

    def missing_fields(self) -> list:
        return [
            name for name in REQUIRED_COLUMNS - {"quarter"}
            if getattr(self, name) is None
        ]


def load_quarters(path) -> dict:
    """Load a CSV into {quarter: QuarterRecord}. Raises SchemaError for bad files."""
    path = Path(path)
    if not path.exists():
        raise SchemaError(f"file not found: {path}")
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise SchemaError(f"missing columns: {sorted(missing)}")
        records = {}
        for line_number, row in enumerate(reader, start=2):
            try:
                record = QuarterRecord(**{k: row[k] for k in REQUIRED_COLUMNS})
            except ValueError as error:
                raise SchemaError(f"line {line_number}: {error}") from error
            records[record.quarter] = record
    if not records:
        raise SchemaError("file contains no rows")
    return records
