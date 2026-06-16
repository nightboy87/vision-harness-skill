from __future__ import annotations

import json
from pathlib import Path


def validate_json(instance_path: str, schema_path: str) -> None:
    try:
        import jsonschema
    except Exception:
        print("jsonschema is not installed; skipping schema validation.")
        return
    instance = json.loads(Path(instance_path).read_text(encoding="utf-8"))
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    jsonschema.validate(instance=instance, schema=schema)
    print(f"OK: {instance_path} validates against {schema_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("instance")
    parser.add_argument("schema")
    args = parser.parse_args()
    validate_json(args.instance, args.schema)
