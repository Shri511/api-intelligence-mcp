"""API response analysis tool for the Template MCP Server.

Enhanced version with structured field inventory.
"""

import json
from typing import Any, Dict, List

from template_mcp_server.utils.pylogger import get_python_logger

logger = get_python_logger()


def analyze_api_response(
    response_json: str,
) -> Dict[str, Any]:
    """Analyze structure, size, and quality of an API JSON response.

    TOOL_NAME=analyze_api_response
    DISPLAY_NAME=API Response Analyzer
    USECASE=Analyze JSON API response structure and generate structured metrics, field inventory, and readable summary
    INSTRUCTIONS=1. Provide valid JSON string, 2. Call function, 3. Receive structured analysis and summary
    INPUT_DESCRIPTION=response_json (string): JSON API response
    OUTPUT_DESCRIPTION=Dictionary containing metrics, full field list, suggestions, and readable summary
    EXAMPLES=analyze_api_response('{"id":1,"name":"John"}')
    PREREQUISITES=Valid JSON string
    RELATED_TOOLS=optimize_api_response_schema, generate_api_documentation, compare_api_responses

    CPU-bound deterministic analysis operation.
    """
    try:
        if not response_json or not isinstance(response_json, str):
            raise ValueError("response_json must be a non-empty string")

        data = json.loads(response_json)

        null_fields: List[str] = []
        empty_arrays: List[str] = []
        fields: List[Dict[str, Any]] = []
        max_depth = 0

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
                return "array"
            if isinstance(value, dict):
                return "object"
            if value is None:
                return "null"
            return "unknown"

        def traverse(obj, parent_path="", depth=1):
            nonlocal max_depth
            max_depth = max(max_depth, depth)

            if isinstance(obj, dict):
                for k, v in obj.items():
                    path = f"{parent_path}.{k}" if parent_path else k

                    field_info = {
                        "path": path,
                        "type": infer_type(v),
                        "depth": depth,
                        "nullable": v is None,
                        "is_array": isinstance(v, list),
                        "is_object": isinstance(v, dict),
                    }

                    fields.append(field_info)

                    if v is None:
                        null_fields.append(path)

                    if isinstance(v, list) and len(v) == 0:
                        empty_arrays.append(path)

                    traverse(v, path, depth + 1)

            elif isinstance(obj, list):
                for index, item in enumerate(obj):
                    traverse(item, f"{parent_path}[{index}]", depth + 1)

        traverse(data)

        payload_size_kb = round(len(response_json.encode("utf-8")) / 1024, 2)

        suggestions = []
        if null_fields:
            suggestions.append("Avoid returning null values")
        if empty_arrays:
            suggestions.append("Avoid returning empty arrays where possible")
        if payload_size_kb > 100:
            suggestions.append("Consider pagination or response compression")

        # Human-readable summary
        summary_lines = [
            "API RESPONSE ANALYSIS SUMMARY",
            "-" * 40,
            f"• Total Fields: {len(fields)}",
            f"• Payload Size: {payload_size_kb} KB",
            f"• Maximum Nesting Depth: {max_depth}",
        ]

        summary_lines.append(
            f"• Null Fields Detected: {', '.join(null_fields) if null_fields else 'None'}"
        )

        summary_lines.append(
            f"• Empty Arrays Detected: {', '.join(empty_arrays) if empty_arrays else 'None'}"
        )

        if suggestions:
            summary_lines.append("\nOptimization Suggestions:")
            for s in suggestions:
                summary_lines.append(f"  - {s}")
        else:
            summary_lines.append("\nNo optimization issues detected.")

        readable_summary = "\n".join(summary_lines)

        logger.info("API response analyzed successfully with full field inventory")

        return {
            "status": "success",
            "operation": "api_response_analysis",
            "metrics": {
                "field_count": len(fields),
                "null_fields": null_fields,
                "empty_arrays": empty_arrays,
                "payload_size_kb": payload_size_kb,
                "max_nesting_depth": max_depth,
                "fields": fields,
            },
            "suggestions": suggestions,
            "readable_summary": readable_summary,
            "message": "API response analyzed successfully",
        }

    except Exception as e:
        logger.error(f"Error analyzing API response: {e}")
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze API response",
        }