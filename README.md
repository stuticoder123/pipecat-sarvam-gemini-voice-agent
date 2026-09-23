# Pipecat Sarvam Gemini Voice Agent

A real-time browser voice agent using:

- Pipecat
- Daily WebRTC transport
- Sarvam AI Saaras STT
- Google Gemini LLM
- Sarvam AI Bulbul TTS
- python-dotenv

## Architecture

Microphone
  ↓
Daily / WebRTC
  ↓
Sarvam Saaras STT
  ↓
Gemini LLM
  ↓
Sarvam Bulbul TTS
  ↓
Daily / WebRTC
  ↓
Speaker

## Project structure

```text
pipecat-sarvam-gemini-voice-agent/
├── .env.example
├── .gitignore
├── README.md
├── agent.py
└── requirements.txt
```

## Prerequisites

- Python 3.10+
- Sarvam AI API key
- Google Gemini API key
- Daily API key

## Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Then add your real keys:

```env
SARVAM_API_KEY=...
GEMINI_API_KEY=...
DAILY_API_KEY=...
```

Never commit `.env`.

## Run

```bash
python agent.py
```

The agent will start the Pipecat pipeline and print the Daily room URL when available. Open that URL in a supported browser and allow microphone access.

## Conversation

The system prompt is configured for English, Hindi and Hinglish. Conversation history is maintained through the Pipecat LLM context aggregator.

## Troubleshooting

### Missing API key

Make sure `.env` exists and contains all three variables.

### Microphone does not work

Allow microphone permission in the browser. Use a browser/environment where WebRTC microphone access is permitted.

### Authentication errors

Check that the Sarvam, Gemini and Daily credentials are valid and active.

### Package/API mismatch

Pipecat evolves quickly. If an import or constructor has changed in the installed version, check the installed Pipecat version and its current documentation before changing the code.

## Security

- No real API keys are included in this project.
- `.env` is ignored by Git.
- Do not paste API keys into source code.
