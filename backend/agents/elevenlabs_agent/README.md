# ElevenLabs Prize Checker Agent

## 🎯 Purpose
Automatically validates whether a hackathon project uses ElevenLabs voice AI technology by analyzing the repository's code, dependencies, API calls, and configuration files.

## 🎙️ About ElevenLabs
ElevenLabs is a leading AI voice technology platform that provides:
- **Text-to-Speech (TTS)** - Convert text to natural-sounding speech
- **Voice Cloning** - Create custom voice models
- **Voice Design** - Generate unique synthetic voices
- **Streaming** - Real-time audio generation
- **Multilingual Support** - Support for multiple languages

## ✅ What It Does

The agent:
1. **Scans GitHub repositories** using the GitHub MCP (Model Context Protocol)
2. **Detects ElevenLabs SDK usage** in Python, JavaScript/TypeScript
3. **Identifies REST API calls** to api.elevenlabs.io
4. **Finds API key references** in environment files
5. **Detects specific features** used (TTS, voice cloning, streaming, etc.)
6. **Returns structured JSON** with evidence and qualification status

## 🔍 Detection Capabilities

### Supported Integration Methods

| Method | Detection Patterns |
|--------|-------------------|
| **Python SDK** | `from elevenlabs import ElevenLabs`, `import elevenlabs` |
| **JavaScript/TypeScript SDK** | `import { ElevenLabs } from 'elevenlabs'`, `require('elevenlabs')` |
| **REST API** | `https://api.elevenlabs.io/`, `/v1/text-to-speech`, `/v1/voices` |
| **Environment Variables** | `ELEVENLABS_API_KEY`, `ELEVEN_LABS_API_KEY`, `XI_API_KEY` |

### Python SDK Detection

```python
# Package in requirements.txt or pyproject.toml
elevenlabs

# Import patterns
from elevenlabs import ElevenLabs
from elevenlabs import generate, play, stream
from elevenlabs.client import ElevenLabs
import elevenlabs

# Usage patterns
client = ElevenLabs(api_key="...")
audio = generate(text="...", voice="...")
```

### JavaScript/TypeScript SDK Detection

```javascript
// Package in package.json
"elevenlabs": "^x.x.x"
"@11labs/client": "^x.x.x"

// Import patterns
import { ElevenLabs } from 'elevenlabs';
const { ElevenLabs } = require('elevenlabs');
import ElevenLabs from 'elevenlabs';

// Usage patterns
const client = new ElevenLabs({ apiKey: "..." });
await client.textToSpeech.convert({ ... });
```

### REST API Detection

```bash
# Direct API calls (any language)
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
GET https://api.elevenlabs.io/v1/voices
GET https://api.elevenlabs.io/v1/models
POST https://api.elevenlabs.io/v1/voice-generation/generate-voice
```

### Environment Variable Detection

```bash
# .env.example or .env files
ELEVENLABS_API_KEY=sk_...
ELEVEN_LABS_API_KEY=...
XI_API_KEY=...
ELEVENLABS_KEY=...
```

### Feature Detection

The agent can identify specific ElevenLabs features:
- **text-to-speech** - Basic TTS conversion
- **voice-cloning** - Custom voice creation
- **streaming** - Real-time audio streaming
- **voice-design** - Voice generation/design

## 📋 Output Schema

```json
{
  "elevenlabs_usage_detected": true,
  "usage_evidence": "The repository is the official ElevenLabs Python SDK, with `elevenlabs.client` being the primary entry point.",
  "primary_language": "Python",
  "integration_type": "python_sdk",
  "features_detected": [
    "text-to-speech",
    "voice-cloning",
    "streaming",
    "voice-design"
  ],
  "api_key_found": true,
  "final_determination": "QUALIFIED"
}
```

### Fields Explanation

- **elevenlabs_usage_detected**: `true` if ElevenLabs is clearly used
- **usage_evidence**: Specific file + evidence found (imports, API calls, etc.)
- **primary_language**: Main programming language detected
- **integration_type**: 
  - `"python_sdk"` - Using Python SDK
  - `"javascript_sdk"` - Using JS/TS SDK
  - `"rest_api"` - Direct REST API calls
  - `"unknown"` - Usage detected but method unclear
- **features_detected**: Array of ElevenLabs features identified
- **api_key_found**: Whether API key references were found
- **final_determination**: 
  - `"QUALIFIED"` - Clear ElevenLabs usage
  - `"DISQUALIFIED"` - No ElevenLabs usage found
  - `"NEEDS_MANUAL_REVIEW"` - Unclear or conflicting signals

## 🚀 Usage

### Via FastAPI Endpoint

```bash
# Start the backend server
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test with curl
curl -X POST http://localhost:8000/api/agents/check-elevenlabs-prize \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/elevenlabs/elevenlabs-python"
  }'
```

### Via Python Script

```python
from google.adk.runners import InMemoryRunner
from agents.elevenlabs_agent import root_agent

async def check_elevenlabs():
    prompt = (
        f"Please check this project for the ElevenLabs Prize.\n"
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
uv run python test_elevenlabs_simple.py

# Run comprehensive test suite
uv run python test_elevenlabs_agent.py
```

## 🧪 Testing

We've included two test scripts:

1. **`test_elevenlabs_simple.py`** - Single repository test (ElevenLabs Python SDK)
2. **`test_elevenlabs_agent.py`** - Comprehensive test suite with 4 different repos

```bash
# Simple test (recommended)
uv run python test_elevenlabs_simple.py

# Full test suite
uv run python test_elevenlabs_agent.py
```

## 📊 Test Results

From our testing with `elevenlabs-python` repository:

```json
{
  "elevenlabs_usage_detected": true,
  "usage_evidence": "The repository is the official ElevenLabs Python SDK...",
  "primary_language": "Python",
  "integration_type": "python_sdk",
  "features_detected": [
    "text-to-speech",
    "voice-cloning",
    "streaming",
    "voice-design"
  ],
  "api_key_found": true,
  "final_determination": "QUALIFIED"
}
```

**✅ Result: QUALIFIED**

## 🔧 Configuration

### Required Environment Variables

```bash
# .env file
GITHUB_TOKEN=ghp_...              # For GitHub MCP access
OPENROUTER_API_KEY=sk-or-v1-...  # For LiteLLM/Gemini model
```

### Agent Configuration

Located in `backend/agents/elevenlabs_agent/agent.py`:

```python
root_agent = Agent(
    model=LiteLlm(
        model="openrouter/google/gemini-2.5-flash",
        api_key=OPENROUTER_API_KEY,
        api_base="https://openrouter.ai/api/v1"
    ),
    name="elevenlabs_prize_checker",
    instruction=ELEVENLABS_CHECKER_INSTRUCTION,
    tools=[McpToolset(...)]  # GitHub MCP
)
```

## 🎨 Example Use Cases

### 1. Hackathon Prize Validation
```bash
curl -X POST http://localhost:8000/api/agents/check-elevenlabs-prize \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/team-name/voice-app"}'
```

### 2. Voice AI Project Detection
Automatically detect if projects are using ElevenLabs for:
- Podcasts/audiobook generation
- Voice assistants
- Accessibility features (screen readers)
- Voiceover automation
- Interactive voice experiences

### 3. Integration Examples
The agent can identify various integration patterns:

**Simple Text-to-Speech:**
```python
from elevenlabs import generate
audio = generate(text="Hello world", voice="Rachel")
```

**Voice Cloning:**
```python
from elevenlabs import clone
voice = clone(name="My Voice", files=["sample1.mp3"])
```

**Streaming:**
```python
from elevenlabs import stream
stream(generate(text="...", voice="...", stream=True))
```

**REST API:**
```bash
curl -X POST https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM \
  -H "xi-api-key: YOUR_API_KEY" \
  -d '{"text": "Hello"}'
```

## 🔍 Detection Logic

### What Counts as ElevenLabs Usage?

✅ **QUALIFIED:**
- Python/JS SDK installed in dependencies
- Import statements for ElevenLabs packages
- Direct API calls to api.elevenlabs.io
- Environment variables with ElevenLabs API keys
- Code demonstrating TTS/voice features

❌ **DISQUALIFIED:**
- No ElevenLabs references found
- Using different TTS services (Google TTS, Amazon Polly, Azure Speech)
- Generic text-to-speech without ElevenLabs

⚠️ **NEEDS_MANUAL_REVIEW:**
- Only mentioned in README without code
- Ambiguous references
- Planned but not implemented

### Distinguishing from Similar Services

The agent specifically checks for **ElevenLabs** and will NOT flag:
- `pyttsx3` (offline Python TTS)
- `gTTS` (Google Text-to-Speech)
- `amazon-polly-sdk` (AWS Polly)
- `@google-cloud/text-to-speech` (Google Cloud)
- `microsoft-cognitiveservices-speech-sdk` (Azure)

## ⚠️ Known Limitations

1. **Private repositories**: Requires GitHub token with repo access
2. **Obfuscated code**: Won't detect if package names are heavily obfuscated
3. **Dynamic imports**: May miss runtime-loaded SDK imports
4. **README-only mentions**: Returns `NEEDS_MANUAL_REVIEW` if only in docs
5. **Custom wrappers**: May not detect if heavily abstracted

## 🐛 Troubleshooting

### "missing required parameter: path" Error
The GitHub MCP tool requires a `path` parameter. Agent auto-retries with correct params.

### False Negatives
If the agent doesn't detect ElevenLabs usage:
- Check if the package is actually installed (`requirements.txt`, `package.json`)
- Verify imports are in Python/JS files (not just README)
- Ensure the repo is public or GitHub token has access

### False Positives
The agent is conservative - should rarely give false positives. If it does:
- Check the `usage_evidence` field for details
- Verify if it's genuinely using ElevenLabs API

## 📁 File Structure

```
backend/
├── agents/
│   ├── elevenlabs_agent/
│   │   ├── __init__.py          # Module exports
│   │   ├── agent.py             # Agent definition
│   │   └── README.md            # This file
│   └── prompts.py               # ELEVENLABS_CHECKER_INSTRUCTION
├── app/
│   └── main.py                  # FastAPI endpoint
├── test_elevenlabs_agent.py     # Full test suite
└── test_elevenlabs_simple.py    # Quick test
```

## 🔄 Future Improvements

- [ ] Detect specific voice IDs used
- [ ] Identify which ElevenLabs models are referenced
- [ ] Extract voice cloning samples
- [ ] Detect multilingual usage
- [ ] Identify streaming vs batch usage
- [ ] Support for ElevenLabs webhook integrations
- [ ] Detect usage of ElevenLabs Projects/Workspaces

## 📚 Related Agents

- **Gemini Prize Checker** - Validates Google Gemini API usage
- **MongoDB Prize Checker** - Validates MongoDB database usage
- **.Tech Prize Checker** - Validates .tech domain usage
- **Code Reviewer Agent** - Evaluates code quality

## 🤝 Contributing

To improve detection:

1. Edit `ELEVENLABS_CHECKER_INSTRUCTION` in `agents/prompts.py`
2. Add new detection patterns
3. Update feature list
4. Add test case to `test_elevenlabs_agent.py`

## 📄 License

Part of the MLH Sidekick project.

---

## 🎯 Quick Reference

**Endpoint:** `POST /api/agents/check-elevenlabs-prize`  
**Input:** `{"repo_url": "https://github.com/..."}`  
**Output:** JSON with detection results  
**Test Command:** `uv run python test_elevenlabs_simple.py`  
**Status:** ✅ Production Ready
