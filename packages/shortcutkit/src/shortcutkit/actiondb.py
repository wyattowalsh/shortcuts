import json
from functools import cache
from pathlib import Path

from jsonschema import Draft202012Validator
from pydantic import ValidationError

from shortcutkit.models import ActionDB, ActionEntry
from shortcutkit.paths import find_repo_root


class ActionDBError(ValueError):
    pass


def actiondb_path(root: Path | None = None) -> Path:
    return (root or find_repo_root()) / "packages" / "actiondb" / "actions.json"


def actiondb_schema_path(root: Path | None = None) -> Path:
    return (root or find_repo_root()) / "packages" / "schemas" / "actiondb.schema.json"


@cache
def load_actiondb(root_text: str | None = None) -> ActionDB:
    root = Path(root_text) if root_text else find_repo_root()
    data_path = actiondb_path(root)
    schema_path = actiondb_schema_path(root)
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ActionDBError(f"{data_path}: invalid JSON: {exc}") from exc

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise ActionDBError(f"{data_path}:{location}: {first.message}")
    try:
        return ActionDB.model_validate(data)
    except ValidationError as exc:
        raise ActionDBError(f"{data_path}: {exc}") from exc


def action_map(root: Path | None = None) -> dict[str, ActionEntry]:
    db = load_actiondb(str(root or find_repo_root()))
    return {action.id: action for action in db.actions}
