# API Intelligence Tools - Quick Reference

## 🔍 analyze_api_response

**Purpose:** Intelligent parsing and validation of API responses

**Input:**
```json
{
  "response_json": "{\"id\": 1, \"name\": \"John\", \"email\": null, \"tags\": []}"
}
```

**Output:**
```json
{
  "status": "success",
  "metrics": {
    "field_count": 4,
    "null_fields": ["email"],
    "empty_arrays": ["tags"],
    "payload_size_kb": 0.08,
    "max_nesting_depth": 1,
    "fields": [...]
  },
  "suggestions": [
    "Avoid returning null values",
    "Avoid returning empty arrays where possible"
  ],
  "readable_summary": "..."
}
```

**Use Cases:**
- Debug API response structure
- Identify optimization opportunities
- Validate API contracts
- Performance analysis

---

## ⚡ optimize_api_response_schema

**Purpose:** Automated schema optimization with size reduction

**Input:**
```json
{
  "response_json": "{\"id\": 1, \"name\": \"John\", \"email\": null, \"tags\": []}",
  "remove_nulls": true,
  "remove_empty_arrays": true
}
```

**Output:**
```json
{
  "status": "success",
  "optimized_response": {"id": 1, "name": "John"},
  "fields_removed": ["email", "tags"],
  "original_size_kb": 0.08,
  "optimized_size_kb": 0.05,
  "size_reduction_kb": 0.03
}
```

**Use Cases:**
- Reduce payload size
- Clean up API responses
- Improve performance
- Bandwidth optimization

---

## 📝 generate_api_documentation

**Purpose:** Context-aware API documentation generation

**Input:**
```json
{
  "endpoint": "/api/users",
  "method": "GET",
  "response_json": "{\"id\": 1, \"name\": \"John\", \"email\": \"john@example.com\"}"
}
```

**Output:**
```json
{
  "status": "success",
  "documentation": "# API Documentation\n\n## Endpoint: /api/users\n...",
  "fields": [
    {"name": "id", "type": "integer", "description": "..."},
    {"name": "name", "type": "string", "description": "..."},
    {"name": "email", "type": "string", "description": "..."}
  ]
}
```

**Use Cases:**
- Auto-generate API docs
- Keep documentation in sync
- Onboard new developers
- API contract documentation

---

## 🔄 compare_api_responses

**Purpose:** Smart diff analysis across API versions

**Input:**
```json
{
  "response1": "{\"id\": 1, \"name\": \"John\"}",
  "response2": "{\"id\": 1, \"name\": \"John\", \"email\": \"john@example.com\", \"age\": 30}"
}
```

**Output:**
```json
{
  "status": "success",
  "differences": {
    "added_fields": ["email", "age"],
    "removed_fields": [],
    "type_changes": [],
    "breaking_changes": false
  },
  "summary": "2 fields added, 0 fields removed",
  "migration_guide": "..."
}
```

**Use Cases:**
- API version comparison
- Regression testing
- Breaking change detection
- Migration planning

---

## Testing the Tools

### Using curl:

```bash
# Analyze API Response
curl -X POST "http://localhost:3000/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "analyze_api_response",
      "arguments": {
        "response_json": "{\"id\": 1, \"name\": \"John\", \"email\": null}"
      }
    }
  }'

# Optimize Schema
curl -X POST "http://localhost:3000/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "optimize_api_response_schema",
      "arguments": {
        "response_json": "{\"id\": 1, \"email\": null, \"tags\": []}",
        "remove_nulls": true,
        "remove_empty_arrays": true
      }
    }
  }'

# Generate Documentation
curl -X POST "http://localhost:3000/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "generate_api_documentation",
      "arguments": {
        "endpoint": "/api/users",
        "method": "GET",
        "response_json": "{\"id\": 1, \"name\": \"John\"}"
      }
    }
  }'

# Compare Responses
curl -X POST "http://localhost:3000/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "compare_api_responses",
      "arguments": {
        "response1": "{\"id\": 1, \"name\": \"John\"}",
        "response2": "{\"id\": 1, \"name\": \"John\", \"email\": \"john@example.com\"}"
      }
    }
  }'
```

---

## Integration with AI Assistants

These tools are designed to be discovered and used by AI assistants through MCP:

1. **AI discovers available tools** via MCP protocol
2. **AI analyzes user request** and determines which tool(s) to use
3. **AI orchestrates tool calls** with appropriate parameters
4. **AI interprets results** and provides insights to the user

Example workflow:
```
User: "Analyze this API response and optimize it"
AI: → calls analyze_api_response
    → reviews suggestions
    → calls optimize_api_response_schema
    → presents before/after comparison
```

---

## Tool Chaining Examples

### Example 1: Complete API Analysis
1. `analyze_api_response` - Identify issues
2. `optimize_api_response_schema` - Apply fixes
3. `compare_api_responses` - Show improvements

### Example 2: API Documentation Workflow
1. `analyze_api_response` - Understand structure
2. `generate_api_documentation` - Create docs
3. `compare_api_responses` - Document changes between versions

### Example 3: API Migration
1. `compare_api_responses` - Identify differences
2. `analyze_api_response` - Validate new version
3. `generate_api_documentation` - Update docs

---

Built with ❤️ during DevConf Pune 2025
