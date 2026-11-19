import csv
import runpy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
TABLE = "outlier_coincidence.csv"
COLUMNS = ("geo", "time", "count", "variables")
FIRST = ("Geo2", "2021-11-22", "2", "Channel0_spend, Promo")
SECOND = ("Geo7", "2023-09-04", "1", "Channel1_spend")


def write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)


@pytest.fixture
def compare_tables(tmp_path, monkeypatch):
    reference = tmp_path / "reference"
    run = tmp_path / "run"
    historical_tables = reference / "outputs/tables"
    reproduced_tables = run / "outputs/tables"
    historical_tables.mkdir(parents=True)
    reproduced_tables.mkdir(parents=True)
    compare = runpy.run_path(str(ROOT / "scripts/compare_runs.py"))["compare"]
    monkeypatch.setitem(compare.__globals__, "ROOT", reference)

    def compare_csv(left, right, filename=TABLE, columns=COLUMNS, reproduced_columns=None):
        write_csv(historical_tables / filename, columns, left)
        write_csv(reproduced_tables / filename, reproduced_columns or columns, right)
        result, = compare(run)
        return result

    return compare_csv


def test_outlier_coincidence_accepts_reordered_rows_with_duplicates(compare_tables):
    result = compare_tables([FIRST, FIRST, SECOND], [SECOND, FIRST, FIRST])
    assert result == {"file": TABLE, "status": "equivalent", "rows": 3, "byte_equal": False}


def test_outlier_coincidence_rejects_different_multiplicities(compare_tables):
    result = compare_tables([FIRST, FIRST, SECOND], [FIRST, SECOND, SECOND])
    assert result["status"] == "different"
    assert "1 ocorrência(s) ausente(s) e 1 adicional(is)" in result["detail"]


@pytest.mark.parametrize(
    ("column", "replacement"),
    [(0, "Geo9"), (1, "2021-11-29"), (2, "100000001"), (3, "Channel0_spend, Other")],
)
def test_outlier_coincidence_rejects_exact_field_changes(compare_tables, column, replacement):
    # Um passo inteiro nesse valor caberia na tolerância relativa das outras tabelas.
    original = (*FIRST[:2], "100000000", FIRST[3])
    changed = list(original)
    changed[column] = replacement
    assert compare_tables([original, SECOND], [SECOND, changed])["status"] == "different"


def test_outlier_coincidence_rejects_different_columns(compare_tables):
    result = compare_tables([FIRST], [FIRST], reproduced_columns=("geo", "time", "count", "channels"))
    assert result["status"] == "different"
    assert "Colunas diferentes" in result["detail"]


def test_outlier_coincidence_rejects_malformed_rows(compare_tables):
    result = compare_tables([FIRST[:-1]], [FIRST[:-1]])
    assert result["status"] == "different"
    assert "Quantidade de campos inválida" in result["detail"]


@pytest.mark.parametrize(
    ("reproduced", "expected_status"),
    [([("Geo2", 1.00000005), ("Geo7", 2.0)], "equivalent"),
     ([("Geo7", 2.0), ("Geo2", 1.0)], "different")],
)
def test_other_tables_keep_positional_comparison_and_numeric_tolerance(compare_tables, reproduced, expected_status):
    historical = [("Geo2", 1.0), ("Geo7", 2.0)]
    result = compare_tables(historical, reproduced, filename="another_table.csv", columns=("geo", "value"))
    assert result["status"] == expected_status
