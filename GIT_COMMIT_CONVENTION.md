
# Git Commit Convention

We follow the Conventional Commits format for consistent and readable Git history.

## Format

`<type>(<optional-scope>): <description>`

## Common Commit Types

| Type | Purpose | Example |
|---|---|---|
| `feat` | Add a new feature | `feat: add document search` |
| `fix` | Fix a bug | `fix: handle missing document IDs` |
| `chore` | Project setup or maintenance | `chore: configure project environment` |
| `docs` | Documentation changes | `docs: update README` |
| `refactor` | Improve code structure without changing behavior | `refactor: simplify tool registration` |
| `test` | Add or update tests | `test: add MCP server tests` |
| `build` | Build system or dependency changes | `build: update dependencies` |
| `perf` | Improve performance | `perf: optimize document search` |
| `style` | Formatting changes without changing behavior | `style: format Python files` |
| `ci` | CI/CD configuration changes | `ci: add automated tests workflow` |

## Examples from This Project

### Initial project setup
`chore: initialize AI research team project`

### MCP server implementation
`feat(mcp-server): add research document search and retrieval tools`

### MCP client implementation
`feat(mcp-client): add MCP server connection and tool execution`

### LangChain adapter
`feat(adapter): convert MCP tools to LangChain tools`

### LangGraph workflow
`feat(langgraph): orchestrate research agents`

### LangSmith tracing
`feat(langsmith): add workflow tracing`

### API implementation
`feat(api): expose research workflow through FastAPI`

### Bug fix
`fix(mcp-client): handle failed tool calls`

### Documentation
`docs: document local setup and deployment`

## Guidelines

1. Use lowercase types and scopes.
2. Write descriptions in the imperative form, such as `add`, `fix`, or `update`.
3. Keep descriptions short and specific.
4. Use a scope when it helps identify the affected component.
5. Use `feat` for new functionality, `fix` for bug fixes, and `chore` for maintenance.
6. Do not include API keys, passwords, or other secrets in commit messages.
7. Keep each commit focused on one logical change.

## Important

Conventional Commits is a convention, not a requirement enforced by Git itself. Git accepts ordinary commit messages, but following a consistent format makes project history easier to review.
