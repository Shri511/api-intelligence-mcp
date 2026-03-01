"""Tests for the MCP server module."""

from unittest.mock import Mock, patch

import pytest

from api_intelligence_mcp.src.mcp import TemplateMCPServer


class TestTemplateMCPServer:
    """Test the TemplateMCPServer class."""

    @patch("api_intelligence_mcp.src.mcp.force_reconfigure_all_loggers")
    @patch("api_intelligence_mcp.src.mcp.settings")
    @patch("api_intelligence_mcp.src.mcp.FastMCP")
    @patch("api_intelligence_mcp.src.mcp.logger")
    def test_init_success(
        self, mock_logger, mock_fastmcp, mock_settings, mock_force_reconfigure
    ):
        """Test successful initialization of TemplateMCPServer."""
        # Arrange
        mock_mcp = Mock()
        mock_fastmcp.return_value = mock_mcp
        mock_settings.PYTHON_LOG_LEVEL = "INFO"

        # Act
        server = TemplateMCPServer()

        # Assert
        assert server.mcp == mock_mcp
        mock_logger.info.assert_called_with(
            "API Intelligence MCP Server initialized successfully"
        )
        # In tools-first architecture, we only register tools
        mock_mcp.tool.assert_called()

    @patch("api_intelligence_mcp.src.mcp.force_reconfigure_all_loggers")
    @patch("api_intelligence_mcp.src.mcp.settings")
    @patch("api_intelligence_mcp.src.mcp.FastMCP")
    @patch("api_intelligence_mcp.src.mcp.logger")
    def test_init_failure(
        self, mock_logger, mock_fastmcp, mock_settings, mock_force_reconfigure
    ):
        """Test initialization failure handling."""
        # Arrange
        mock_fastmcp.side_effect = Exception("Test error")
        mock_settings.PYTHON_LOG_LEVEL = "INFO"

        # Act & Assert
        with pytest.raises(Exception, match="Test error"):
            TemplateMCPServer()

        mock_logger.error.assert_called_with(
            "Failed to initialize API Intelligence MCP Server: Test error"
        )

    @patch("api_intelligence_mcp.src.mcp.force_reconfigure_all_loggers")
    @patch("api_intelligence_mcp.src.mcp.settings")
    @patch("api_intelligence_mcp.src.mcp.FastMCP")
    def test_register_mcp_tools(
        self, mock_fastmcp, mock_settings, mock_force_reconfigure
    ):
        """Test MCP tools registration."""
        # Arrange
        mock_mcp = Mock()
        mock_fastmcp.return_value = mock_mcp
        mock_settings.PYTHON_LOG_LEVEL = "INFO"
        server = TemplateMCPServer()

        # Act
        server._register_mcp_tools()

        # Assert
        mock_mcp.tool.assert_called()

    @patch("api_intelligence_mcp.src.mcp.force_reconfigure_all_loggers")
    @patch("api_intelligence_mcp.src.mcp.settings")
    @patch("api_intelligence_mcp.src.mcp.FastMCP")
    def test_register_mcp_tools_functionality(
        self, mock_fastmcp, mock_settings, mock_force_reconfigure
    ):
        """Test that MCP tools registration includes all expected tools."""
        # Arrange
        mock_mcp = Mock()
        mock_fastmcp.return_value = mock_mcp
        mock_settings.PYTHON_LOG_LEVEL = "INFO"
        server = TemplateMCPServer()

        # Act
        server._register_mcp_tools()

        # Assert
        # Verify that tool() was called multiple times (once for each tool)
        assert (
            mock_mcp.tool.call_count >= 4
        )  # analyze_api_response, optimize_api_response_schema, generate_api_documentation, compare_api_responses

    def test_server_attributes(self):
        """Test that server has required attributes for tools-first architecture."""
        # Arrange & Act
        with (
            patch("api_intelligence_mcp.src.mcp.settings") as mock_settings,
            patch("api_intelligence_mcp.src.mcp.FastMCP"),
            patch("api_intelligence_mcp.src.mcp.force_reconfigure_all_loggers"),
        ):
            mock_settings.PYTHON_LOG_LEVEL = "INFO"
            server = TemplateMCPServer()

        # Assert
        assert hasattr(server, "mcp")
        assert hasattr(server, "_register_mcp_tools")

    def test_tools_first_architecture_compliance(self):
        """Test that server adheres to tools-first architecture by not having resource/prompt methods."""
        # Arrange & Act
        with (
            patch("api_intelligence_mcp.src.mcp.settings") as mock_settings,
            patch("api_intelligence_mcp.src.mcp.FastMCP"),
            patch("api_intelligence_mcp.src.mcp.force_reconfigure_all_loggers"),
        ):
            mock_settings.PYTHON_LOG_LEVEL = "INFO"
            server = TemplateMCPServer()

        # Assert - These methods should NOT exist in tools-first architecture
        assert not hasattr(server, "_register_mcp_resources"), (
            "_register_mcp_resources should not exist in tools-first architecture"
        )
        assert not hasattr(server, "_register_mcp_prompts"), (
            "_register_mcp_prompts should not exist in tools-first architecture"
        )
