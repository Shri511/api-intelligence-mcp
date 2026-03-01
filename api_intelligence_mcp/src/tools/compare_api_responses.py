"""API response comparison tool for the Template MCP Server."""

import json
from typing import Any, Dict, Set

from api_intelligence_mcp.utils.pylogger import get_python_logger

logger = get_python_logger()


def compare_api_responses(
    old_response: str,
    new_response: str,
) -> Dict[str, Any]:
    """Compare two API JSON responses for structural differences.

    TOOL_NAME=compare_api_responses
    DISPLAY_NAME=API Response Comparator
    USECASE=Detect added, removed, and type-changed fields between API versions
    INSTRUCTIONS=1. Provide old and new JSON strings, 2. Call function, 3. Receive comparison result
    INPUT_DESCRIPTION=old_response (string), new_response (string)
    OUTPUT_DESCRIPTION=Dictionary listing structural differences and breaking change detection
    EXAMPLES=compare_api_responses('{"id":1}', '{"id":1,"name":"John"}')
    PREREQUISITES=Both inputs must be valid JSON strings
    RELATED_TOOLS=analyze_api_response

    CPU-bound structural comparison.
    """
    try:
        old_data = json.loads(old_response)
        new_data = json.loads(new_response)

        def extract_schema(obj, parent="") -> Dict[str, str]:
            schema = {}
            if isinstance(obj, dict):
                for k, v in obj.items():
                    path = f"{parent}.{k}" if parent else k
                    schema.update(extract_schema(v, path))
            else:
                schema[parent] = type(obj).__name__
            return schema

        old_schema = extract_schema(old_data)
        new_schema = extract_schema(new_data)

        old_fields: Set[str] = set(old_schema.keys())
        new_fields: Set[str] = set(new_schema.keys())

        added_fields = list(new_fields - old_fields)
        removed_fields = list(old_fields - new_fields)

        type_changes = []
        for field in old_fields & new_fields:
            if old_schema[field] != new_schema[field]:
                type_changes.append(
                    f"{field}: {old_schema[field]} -> {new_schema[field]}"
                )

        breaking_changes = bool(removed_fields or type_changes)

        logger.info("API responses compared successfully")

        return {
            "status": "success",
            "added_fields": added_fields,
            "removed_fields": removed_fields,
            "type_changes": type_changes,
            "breaking_changes_detected": breaking_changes,
            "message": "API comparison completed successfully",
        }

    except Exception as e:
        logger.error(f"Error comparing API responses: {e}")
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to compare API responses",
        }