"""API documentation generator tool for the Template MCP Server."""

import json
from typing import Any, Dict

from api_intelligence_mcp.utils.pylogger import get_python_logger

logger = get_python_logger()


def generate_api_documentation(
    response_json: str,
) -> Dict[str, Any]:
    """Generate schema-like documentation from JSON response.

    TOOL_NAME=generate_api_documentation
    DISPLAY_NAME=API Documentation Generator
    USECASE=Infer schema and data types from API JSON response
    INSTRUCTIONS=1. Provide valid JSON string, 2. Call function, 3. Receive inferred schema
    INPUT_DESCRIPTION=response_json (string)
    OUTPUT_DESCRIPTION=Dictionary containing inferred schema structure
    EXAMPLES=generate_api_documentation('{"id":1,"name":"John"}')
    PREREQUISITES=Valid JSON string
    RELATED_TOOLS=analyze_api_response

    CPU-bound schema inference operation.
    """
    try:
        if not response_json or not isinstance(response_json, str):
            raise ValueError("response_json must be a non-empty string")

        data = json.loads(response_json)

        def infer_type(value):
            if isinstance(value, bool):
                return "boolean"
            if isinstance(value, int):
                return "integer"
            if isinstance(value, float):
                return "float"
            if isinstance(value, str):
                return "string"
            if isinstance(value, list):
                if value:
                    return [infer_type(value[0])]
                return ["unknown"]
            if isinstance(value, dict):
                return {k: infer_type(v) for k, v in value.items()}
            return "unknown"

        schema = infer_type(data)

        logger.info("API documentation generated successfully")

        return {
            "status": "success",
            "schema": schema,
            "message": "API documentation generated successfully",
        }

    except Exception as e:
        logger.error(f"Error generating API documentation: {e}")
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to generate API documentation",
        }