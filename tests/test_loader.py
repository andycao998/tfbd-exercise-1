import pytest
from pathlib import Path
from pydantic import ValidationError
from warehouse_validator.models import RestockItem
from warehouse_validator.store import InvalidManifestFormatError, ManifestNotFoundError, load_manifest


def test_loading_valid_row():
    row = {"sku": "1", "warehouse": "w1", "quantity": 15, "unit_cost": 1.50, "category": "electronics"}
    item = RestockItem.model_validate(row)

    assert(item.sku == "1")
    assert(item.warehouse == "w1")
    assert(item.quantity == 15)
    assert(item.unit_cost == 1.50)
    assert(item.category == "electronics")


@pytest.mark.parametrize("row", [
    {"sku": "1", "warehouse": "w1", "quantity": 5, "unit_cost": 1.00, "category": "TESTCATEGORY"}, # Out-of-set category
    {"sku": "2", "warehouse": "s3", "quantity": -1, "unit_cost": 9.99, "category": "apparel"}, # Invalid quantity (<= 0)
    {"sku": "3", "warehouse": "n4", "quantity": 7, "unit_cost": 0.00, "category": "electronics"}, # Invalid unit_cost (<= 0)
    {"warehouse": "w2", "quantity": 8, "unit_cost": 4.00, "category": "hardware"} # Missing sku
])
def test_loading_invalid_fields(row):
    with pytest.raises(ValidationError):
        RestockItem.model_validate(row)


def test_provided_manifest_success_and_error_count():
    success_items, error_items = load_manifest(Path("data/restock_manifest.json"))

    assert len(success_items) == 8
    assert len(error_items) == 4


@pytest.mark.parametrize("path", [
    None,
    "data/nonexistent_path.json"
])
def test_missing_or_not_found_path(path):
    with pytest.raises(ManifestNotFoundError):
        load_manifest(path)


# Testing custom invalid format error using tmp_path fixture
def test_invalid_formatted_data(tmp_path):
    path = tmp_path / "bad_format_manifest.json"
    path.write_text("This is not json")

    with pytest.raises(InvalidManifestFormatError):
        load_manifest(path)