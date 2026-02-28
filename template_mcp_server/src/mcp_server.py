"""API Intelligence MCP Server implementation.

This module contains the main API Intelligence MCP Server class that provides
tools for API analysis, optimization, documentation, and comparison.
It uses FastMCP to register and manage MCP capabilities.
"""

from fastmcp import FastMCP

from template_mcp_server.src.settings import settings

# Import API intelligence tools
from template_mcp_server.src.tools.analyze_api_response import analyze_api_response
from template_mcp_server.src.tools.compare_api_responses import compare_api_responses
from template_mcp_server.src.tools.generate_api_documentation import (
    generate_api_documentation,
)
from template_mcp_server.src.tools.optimize_api_response_schema import (
    optimize_api_response_schema,
)

from template_mcp_server.utils.pylogger import (
    force_reconfigure_all_loggers,
    get_python_logger,
)

logger = get_python_logger()


class TemplateMCPServer:
    """API Intelligence MCP Server implementation following tools-first architecture.

    This server provides AI-powered tools for API development workflows including:
    - API response analysis and validation
    - Schema optimization suggestions
    - Automated documentation generation
    - API response comparison and diff analysis
    """

    def __init__(self):
        """Initialize the API Intelligence MCP server with API tools."""
        try:
            # Initialize FastMCP server
            self.mcp = FastMCP("api-intelligence")

            # Force reconfigure all loggers after FastMCP initialization to ensure structured logging
            force_reconfigure_all_loggers(settings.PYTHON_LOG_LEVEL)

            self._register_mcp_tools()

            logger.info("API Intelligence MCP Server initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize API Intelligence MCP Server: {e}")
            raise

    def _register_mcp_tools(self) -> None:
        """Register API intelligence tools (tools-first architecture).

        Registers all available API development tools with the FastMCP server.
        Tools included:
        - analyze_api_response: Intelligent parsing and validation of API responses
        - optimize_api_response_schema: Automated schema optimization suggestions
        - generate_api_documentation: Context-aware API documentation generation
        - compare_api_responses: Smart diff analysis across API versions
        """
        # Register API intelligence tools
        self.mcp.tool()(analyze_api_response)
        self.mcp.tool()(optimize_api_response_schema)
        self.mcp.tool()(generate_api_documentation)
        self.mcp.tool()(compare_api_responses)
