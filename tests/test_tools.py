"""Tests for API Intelligence MCP tools."""

import asyncio
import json
from unittest.mock import Mock, patch

import pytest

from template_mcp_server.src.tools.analyze_api_response import analyze_api_response
from template_mcp_server.src.tools.compare_api_responses import compare_api_responses
from template_mcp_server.src.tools.generate_api_documentation import (
    generate_api_documentation,
)
from template_mcp_server.src.tools.optimize_api_response_schema import (
    optimize_api_response_schema,
)


class TestAnalyzeAPIResponse:
    """Test the analyze_api_response tool."""

    def test_analyze_api_response_success(self):
        """Test successful API response analysis."""
        # Arrange
        response_json = '{"id": 1, "name": "John", "email": null}'

        # Act
        result = analyze_api_response(response_json)

        # Assert
        assert result["status"] == "success"
        assert result["operation"] == "api_response_analysis"
        assert result["metrics"]["field_count"] == 3
        assert "email" in result["metrics"]["null_fields"]
        assert "readable_summary" in result

    def test_analyze_api_response_empty_string(self):
        """Test analysis with empty string."""
        # Arrange
        response_json = ""

        # Act
        result = analyze_api_response(response_json)

        # Assert
        assert result["status"] == "error"
        assert "must be a non-empty string" in result["error"]

    def test_analyze_api_response_invalid_json(self):
        """Test analysis with invalid JSON."""
        # Arrange
        response_json = '{"invalid": json}'

        # Act
        result = analyze_api_response(response_json)

        # Assert
        assert result["status"] == "error"


class TestOptimizeAPIResponseSchema:
    """Test the optimize_api_response_schema tool."""

    def test_optimize_removes_nulls(self):
        """Test that null fields are removed."""
        # Arrange
        response_json = '{"id": 1, "name": "John", "email": null}'

        # Act
        result = optimize_api_response_schema(response_json)

        # Assert
        assert result["status"] == "success"
        assert "email" in result["fields_removed"]
        assert "email" not in result["optimized_response"]

    def test_optimize_removes_empty_arrays(self):
        """Test that empty arrays are removed."""
        # Arrange
        response_json = '{"id": 1, "tags": []}'

        # Act
        result = optimize_api_response_schema(response_json)

        # Assert
        assert result["status"] == "success"
        assert "tags" in result["fields_removed"]

    def test_optimize_size_reduction(self):
        """Test that size reduction is calculated."""
        # Arrange
        response_json = '{"id": 1, "name": null, "email": null, "tags": []}'

        # Act
        result = optimize_api_response_schema(response_json)

        # Assert
        assert result["status"] == "success"
        assert result["size_reduction_kb"] >= 0
        assert result["original_size_kb"] > result["optimized_size_kb"]


class TestGenerateAPIDocumentation:
    """Test the generate_api_documentation tool."""

    def test_generate_documentation_success(self):
        """Test successful documentation generation."""
        # Arrange
        endpoint = "/api/users"
        method = "GET"
        response_json = '{"id": 1, "name": "John"}'

        # Act
        result = asyncio.run(
            generate_api_documentation(endpoint, method, response_json)
        )

        # Assert
        assert result["status"] == "success"
        assert result["operation"] == "api_documentation"
        assert endpoint in result["documentation"]
        assert method in result["documentation"]

    def test_generate_documentation_empty_endpoint(self):
        """Test documentation with empty endpoint."""
        # Arrange
        endpoint = ""
        method = "GET"
        response_json = '{"id": 1}'

        # Act
        result = asyncio.run(
            generate_api_documentation(endpoint, method, response_json)
        )

        # Assert
        assert result["status"] == "error"


class TestCompareAPIResponses:
    """Test the compare_api_responses tool."""

    def test_compare_identical_responses(self):
        """Test comparison of identical responses."""
        # Arrange
        response1 = '{"id": 1, "name": "John"}'
        response2 = '{"id": 1, "name": "John"}'

        # Act
        result = asyncio.run(compare_api_responses(response1, response2))

        # Assert
        assert result["status"] == "success"
        assert result["operation"] == "api_comparison"
        assert len(result["differences"]["added_fields"]) == 0
        assert len(result["differences"]["removed_fields"]) == 0

    def test_compare_different_responses(self):
        """Test comparison of different responses."""
        # Arrange
        response1 = '{"id": 1, "name": "John"}'
        response2 = '{"id": 1, "name": "John", "email": "john@example.com"}'

        # Act
        result = asyncio.run(compare_api_responses(response1, response2))

        # Assert
        assert result["status"] == "success"
        assert len(result["differences"]["added_fields"]) > 0

    def test_compare_invalid_json(self):
        """Test comparison with invalid JSON."""
        # Arrange
        response1 = '{"invalid": json}'
        response2 = '{"id": 1}'

        # Act
        result = asyncio.run(compare_api_responses(response1, response2))

        # Assert
        assert result["status"] == "error"
