# MongoDB Prize Checker Agent

## 🎯 Purpose
Automatically validates whether a hackathon project uses MongoDB by analyzing the repository's code, dependencies, and configuration files.

## ✅ What It Does

The agent:
1. **Scans GitHub repositories** using the GitHub MCP (Model Context Protocol)
2. **Detects MongoDB usage** across multiple programming languages
3. **Identifies the driver/library** used (pymongo, mongoose, MongoDB.Driver, etc.)
4. **Returns structured JSON** with evidence and qualification status

## 🔍 Detection Capabilities

### Supported Languages & Drivers

| Language | Drivers/Libraries Detected |
|----------|---------------------------|
| **Python** | pymongo, motor, mongoengine, djongo, beanie |
| **JavaScript/TypeScript** | mongodb, mongoose, monk, mongoskin, typeorm |
| **Java** | mongo-java-driver, Spring Data MongoDB |
| **C#/.NET** | MongoDB.Driver, MongoDB.Bson |
| **Go** | mongo-driver (official) |
| **PHP** | mongodb/mongodb |
| **Ruby** | mongo, mongoid |
| **Rust** | mongodb crate |
| **Dart/Flutter** | mongo_dart |

### Detection Methods

The agent inspects:
- **Dependency files**: `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, etc.
- **Source code**: Import statements, using directives, require() calls
- **Configuration**: Environment variables, connection strings (mongodb://, mongodb+srv://)
- **Infrastructure**: Docker Compose files, Kubernetes configs

### MongoDB Atlas Detection

Specifically looks for:
- `mongodb+srv://` connection strings
- References to "Atlas" in documentation
- `cloud.mongodb.com` URLs

## 📋 Output Schema

```json
{
  "mongodb_usage_detected": true,
  "usage_evidence": "package.json lists 'mongodb' as a dependency, and 'mongoose' itself is a MongoDB ODM.",
  "primary_language": "JavaScript",
  "driver_library": "mongoose",
  "uses_atlas": false,
  "connection_method": "unknown",
  "final_determination": "QUALIFIED"
}
```

### Fields Explanation

- **mongodb_usage_detected**: `true` if MongoDB is clearly used
- **usage_evidence**: Specific file + evidence found
- **primary_language**: Main programming language detected
- **driver_library**: Specific MongoDB driver/ODM name
- **uses_atlas**: Whether MongoDB Atlas (cloud) is detected
- **connection_method**: `"local"`, `"atlas"`, `"docker"`, or `"unknown"`
- **final_determination**: 
  - `"QUALIFIED"` - Clear MongoDB usage
  - `"DISQUALIFIED"` - No MongoDB usage found
  - `"NEEDS_MANUAL_REVIEW"` - Unclear or conflicting signals

## 🚀 Usage

### Via FastAPI Endpoint

```bash
# Start the backend server
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test with curl
curl -X POST http://localhost:8000/api/agents/check-mongodb-prize \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/Automattic/mongoose"
  }'
```

### Via Python Script

```python
from google.adk.runners import InMemoryRunner
from agents.mongodb_agent import root_agent

async def check_mongodb():
    prompt = (
        f"Please check this project for the MongoDB Prize.\n"
        f"GitHub Repository: https://github.com/your-org/your-repo\n\n"
        f"SYSTEM INSTRUCTION: Do NOT explain your plan. "
        f"Use the tools immediately. Output ONLY the final JSON object."
    )
    
    runner = InMemoryRunner(agent=root_agent)
    history = await runner.run_debug(prompt, verbose=False)
    # Parse result from history...
```

### Quick Test

```bash
# Run the simple test
cd backend
uv run python test_mongodb_simple.py
```

## 🧪 Testing

We've included two test scripts:

1. **`test_mongodb_simple.py`** - Single repository test (Mongoose)
2. **`test_mongodb_agent.py`** - Comprehensive test suite with 6 different repos

```bash
# Simple test (recommended)
uv run python test_mongodb_simple.py

# Full test suite
uv run python test_mongodb_agent.py
```

## 📊 Test Results

From our testing with `mongoose` repository:

```
✅ MongoDB Usage: DETECTED
💻 Language: JavaScript
📦 Driver/Library: mongoose
☁️  Uses Atlas: False
🔌 Connection: unknown
📝 Evidence: package.json lists 'mongodb' as a dependency
🏆 Final Determination: QUALIFIED
```

## 🔧 Configuration

### Required Environment Variables

```bash
# .env file
GITHUB_TOKEN=ghp_...              # For GitHub MCP access
OPENROUTER_API_KEY=sk-or-v1-...  # For LiteLLM/Gemini model
```

### Agent Configuration

Located in `backend/agents/mongodb_agent/agent.py`:

```python
root_agent = Agent(
    model=LiteLlm(
        model="openrouter/google/gemini-2.5-flash",
        api_key=OPENROUTER_API_KEY,
        api_base="https://openrouter.ai/api/v1"
    ),
    name="mongodb_prize_checker",
    instruction=MONGODB_CHECKER_INSTRUCTION,
    tools=[McpToolset(...)]  # GitHub MCP
)
```

## 🎨 Example Use Cases

### 1. Hackathon Prize Validation
```bash
curl -X POST http://localhost:8000/api/agents/check-mongodb-prize \
  -d '{"repo_url": "https://github.com/team-name/hackathon-project"}'
```

### 2. Bulk Validation
```python
repos = [
    "https://github.com/user1/project1",
    "https://github.com/user2/project2",
]

for repo in repos:
    result = await check_mongodb_prize(repo)
    if result["final_determination"] == "QUALIFIED":
        print(f"✅ {repo} - QUALIFIED")
```

### 3. Manual Review Queue
```python
# Flag projects needing human review
if result["final_determination"] == "NEEDS_MANUAL_REVIEW":
    send_to_review_queue(repo_url, result["usage_evidence"])
```

## ⚠️ Known Limitations

1. **Private repositories**: Requires GitHub token with repo access
2. **Archived repositories**: Some older repos may have API access issues
3. **Large repositories**: May timeout on extremely large codebases
4. **Obfuscated code**: Won't detect MongoDB if heavily obfuscated
5. **README-only claims**: If MongoDB is only mentioned in README without code, returns `NEEDS_MANUAL_REVIEW`

## 🐛 Troubleshooting

### "missing required parameter: path" Error
The GitHub MCP tool requires a `path` parameter. Agent auto-retries with correct params.

### "KeyError: Context variable not found"
ADK treats `{}` as template variables. Use regular parentheses in examples.

### Cleanup Warning at End
Cosmetic async generator warning - doesn't affect results. Can be ignored.

## 📁 File Structure

```
backend/
├── agents/
│   ├── mongodb_agent/
│   │   ├── __init__.py          # Module exports
│   │   └── agent.py             # Agent definition
│   └── prompts.py               # MONGODB_CHECKER_INSTRUCTION
├── app/
│   └── main.py                  # FastAPI endpoint
├── test_mongodb_agent.py        # Full test suite
└── test_mongodb_simple.py       # Quick test
```

## 🔄 Future Improvements

- [ ] Add caching to avoid re-scanning same repos
- [ ] Detect MongoDB Atlas cluster IDs
- [ ] Extract specific MongoDB versions used
- [ ] Support for private repositories
- [ ] Detect MongoDB usage in CI/CD configs
- [ ] Handle monorepos with multiple services

## 📚 Related Agents

- **Gemini Prize Checker** - Validates Google Gemini API usage
- **.Tech Prize Checker** - Validates .tech domain usage
- **Code Reviewer Agent** - Evaluates code quality

## 🤝 Contributing

To add support for a new language:

1. Edit `MONGODB_CHECKER_INSTRUCTION` in `agents/prompts.py`
2. Add the language's dependency file patterns
3. Add import statement examples
4. Add test case to `test_mongodb_agent.py`

## 📄 License

Part of the MLH Sidekick project.
