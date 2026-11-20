from pathlib import Path

import pytest

from finance_analyst.schema import SchemaError, load_quarters

DATA = Path(__file__).parent.parent / "finance_analyst" / "data" / "quarters.csv"


def test_loads_eight_quarters():
    records = load_quarters(DATA)
    assert len(records) == 8
    assert records["2025Q1"].marketing_spend == 50_000
    assert records["2025Q1"].new_customers == 1_000


def test_missing_value_becomes_none_not_guess():
    records = load_quarters(DATA)
    assert records["2026Q2"].marketing_spend is None
    assert records["2026Q2"].missing_fields() == ["marketing_spend"]


def test_complete_row_has_no_missing_fields():
    assert load_quarters(DATA)["2025Q2"].missing_fields() == []


def test_zero_customers_is_loaded_as_is():
    # The loader does not hide bad data; metrics.cac() will refuse it.
    assert load_quarters(DATA)["2026Q4"].new_customers == 0


def test_missing_column_raises(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("quarter,marketing_spend\n2025Q1,100\n")
    with pytest.raises(SchemaError, match="missing columns"):
        load_quarters(bad)


def test_bad_quarter_label_raises(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(
        "quarter,marketing_spend,new_customers,lifespan_months,"
        "monthly_revenue_per_user\nJan-2025,100,10,12,50\n"
    )
    with pytest.raises(SchemaError, match="quarter"):
        load_quarters(bad)


def test_non_numeric_value_raises(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(
        "quarter,marketing_spend,new_customers,lifespan_months,"
        "monthly_revenue_per_user\n2025Q1,abc,10,12,50\n"
    )
    with pytest.raises(SchemaError):
        load_quarters(bad)


def test_missing_file_raises(tmp_path):
    with pytest.raises(SchemaError, match="not found"):
        load_quarters(tmp_path / "nope.csv")
