import json
from pathlib import Path
from pydantic import ValidationError
from warehouse_validator.models import RestockItem

class ManifestStoreError(Exception) :
    """ base exception for all errors in this module """

class ManifestNotFoundError(ManifestStoreError) :
    """ raised when the restock manifest file does not exist """

class InvalidManifestFormatError(ManifestStoreError):
    """ raised when manifest data cannot be loaded in due to format issues """

def load_manifest(path: Path | None = None) -> tuple[list[RestockItem], list[dict[str, list[str]]]]:
    # resolved_path = path if path is not None else Path("data/restock_manifest.json")

    try:
        raw_text = path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise ManifestNotFoundError(f"No restock manifest at {path}") from e
    except AttributeError as e:
        raise ManifestNotFoundError(f"No path specified") from e

    try:
        rows = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise InvalidManifestFormatError(f"Manifest data could not be loaded in from {path}") from e

    valid_items: list[RestockItem] = []
    error_items: list[dict[str, list[str]]] = []

    for row in rows:
        try: 
            valid_items.append(RestockItem.model_validate(row))
        except ValidationError as e:
            err_msgs = [f"{e['loc']} : {e['msg']}" for e in e.errors()]
            error_items.append({"sku": row.get("sku", "<no sku>"), "errors": err_msgs})

    return valid_items, error_items
