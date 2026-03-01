"""API response optimization tool for the Template MCP Server."""

import json
from typing import Any, Dict

from api_intelligence_mcp.utils.pylogger import get_python_logger

logger = get_python_logger()


def optimize_api_response_schema(
    response_json: str,
    remove_nulls: bool = True,
    remove_empty_arrays: bool = True,
) -> Dict[str, Any]:
    """Optimize API response by removing unnecessary fields.

    TOOL_NAME=optimize_api_response_schema
    DISPLAY_NAME=API Response Optimizer
    USECASE=Clean API JSON by removing null fields and empty arrays
    INSTRUCTIONS=1. Provide valid JSON string, 2. Configure removal flags, 3. Receive optimized JSON
    INPUT_DESCRIPTION=response_json (string), remove_nulls (bool), remove_empty_arrays (bool)
    OUTPUT_DESCRIPTION=Dictionary with optimized JSON and size comparison
    EXAMPLES=optimize_api_response_schema('{"id":1,"name":null}')
    PREREQUISITES=Valid JSON string
    RELATED_TOOLS=analyze_api_response

    CPU-bound transformation operation.
    """
    try:
        if not response_json or not isinstance(response_json, str):
            raise ValueError("response_json must be a non-empty string")

        data = json.loads(response_json)

        fields_removed = []

        def clean(obj):
            if isinstance(obj, dict):
                new_dict = {}
                for k, v in obj.items():
                    if remove_nulls and v is None:
                        fields_removed.append(k)
                        continue
                    if remove_empty_arrays and isinstance(v, list) and len(v) == 0:
                        fields_removed.append(k)
                        continue
                    new_dict[k] = clean(v)
                return new_dict
            elif isinstance(obj, list):
                return [clean(item) for item in obj]
            else:
                return obj

        original_size = round(len(response_json.encode("utf-8")) / 1024, 2)
        optimized_data = clean(data)
        optimized_json = json.dumps(optimized_data)
        optimized_size = round(len(optimized_json.encode("utf-8")) / 1024, 2)

        logger.info("API response optimized successfully")

        return {
            "status": "success",
            "optimized_response": optimized_data,
            "fields_removed": fields_removed,
            "original_size_kb": original_size,
            "optimized_size_kb": optimized_size,
            "size_reduction_kb": round(original_size - optimized_size, 2),
            "message": "API response optimized successfully",
        }

    except Exception as e:
        logger.error(f"Error optimizing API response: {e}")
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to optimize API response",
        }