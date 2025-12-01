# 🎭 Day 10: Voice Improv Battle

**AI Voice Agent Challenge** | Final Task | Deadline: December 2, 12PM IST

---

## 🎯 Challenge Overview

Build a real-time **Voice Improv Battle** agent that:
- Listens to user input via voice
- Responds like an improv actor using "Yes, and..." technique
- Adapts energy and tone dynamically
- Creates engaging, playful conversations

### 📌 Important Links

- **Task Description**: https://github.com/murf-ai/ten-days-of-voice-agents-2025/blob/day-10/challenges/Day%2010%20Task.md
- **Submission Form**: https://forms.gle/pV8AnocDfk1RZgyD7
- **LinkedIn**: Mention you're using **Murf Falcon - the fastest TTS API**

### 📚 Resources

- [Prompting Guide](https://docs.livekit.io/agents/build/prompting/)
- [Tools & Functions](https://docs.livekit.io/agents/build/tools/)
- [Session Events](https://docs.livekit.io/agents/build/nodes/#on_user_turn_completed)
- [Transcription Node](https://docs.livekit.io/agents/build/nodes/#transcription-node)

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 18+** and **pnpm** (for frontend)
- **LiveKit Server** (included as `livekit-server.exe`)
- API Keys:
  - [Deepgram](https://console.deepgram.com/) - Speech-to-Text
  - [Google AI Studio](https://aistudio.google.com/app/apikey) - LLM (Gemini)
  - [Murf AI](https://murf.ai/) - Text-to-Speech (optional but recommended)

### Step 1: Start LiveKit Server

```powershell
# Run the included LiveKit server
.\livekit-server.exe --dev
```

Leave this running in a separate terminal.

### Step 2: Configure Backend

```powershell
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -e .

# Copy and configure environment variables
copy .env.example .env.local
# Edit .env.local and add your API keys
```

**Required environment variables** in `backend/.env.local`:
```env
DEEPGRAM_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
MURF_API_KEY=your_key_here  # Optional but recommended
MURF_VOICE=en-US-mia        # Or another Murf voice
```

### Step 3: Start Backend Agent

```powershell
# From backend folder with activated venv
python src\agent.py dev
```

**Note**: On Windows, you may see IPC/watcher errors. These are safe to ignore, or run without auto-reload:
```powershell
python src\agent.py start
```

### Step 4: Configure & Start Frontend

```powershell
cd frontend

# Install dependencies
pnpm install

# Copy and configure environment variables
copy .env.example .env.local
# The defaults in .env.example should work for local development

# Start dev server
pnpm dev
```

### Step 5: Test Your Agent

1. Open **http://localhost:3000**
2. Click **"Connect"** or **"Join Day 10 Challenge"**
3. Allow microphone access
4. Start talking! The agent will respond with improv-style replies

---

## 🎭 How the Improv Agent Works

### Key Features

1. **Energy Detection**: Analyzes your speech patterns (exclamations, caps, pace) to match your energy
2. **"Yes, and" Logic**: Always accepts and builds on your ideas
3. **Dynamic Prompting**: Constructs LLM prompts based on conversation context and energy level
4. **Short Turns**: Keeps responses brief (1-3 sentences) for natural back-and-forth
5. **Playful Personality**: Uses vivid language and emotional beats

### Architecture

```
User Voice → Deepgram STT → Energy Detection → 
  LLM (Gemini) with Improv Prompt → Murf TTS → Audio Output
```

### Customization

Edit `backend/src/agent.py` to customize:
- **Personality**: Modify `build_improv_prompt()` function
- **Energy thresholds**: Adjust `detect_energy_from_text()` scoring
- **Fallback responses**: Update `fallback_reply()` function
- **Announcement**: Change `get_day10_announcement()` text

---

## 🔧 Troubleshooting

### Backend Issues

**Error: "Invalid voice_id murf-falcon"**
- Set `MURF_VOICE` in `.env.local` to a valid Murf voice ID
- Or remove `MURF_API_KEY` to use Google TTS instead

**Error: "audio filter cannot be enabled: LiveKit Cloud is required"**
- Set `ENABLE_AUDIO_FILTER=false` in `.env.local` (default for local dev)

**Error: "failed to fetch server settings: http status: 404"**
- Ensure LiveKit server is running: `.\livekit-server.exe --dev`
- Check `LIVEKIT_URL` matches the server address (default: `ws://127.0.0.1:7880`)

**Tests failing with 401/API errors**
- Add valid API keys to `.env.local`
- Or skip tests for now (they require live API access)

**Windows IPC/Watcher errors**
- Use `python src\agent.py start` instead of `dev` to disable auto-reload

### Frontend Issues

**`pnpm dev` exits with code 1**
- Check that LiveKit server is running
- Verify `.env.local` has correct `LIVEKIT_URL`
- Try clearing Next.js cache: `pnpm clean` or `rm -rf .next`

**Cannot connect to agent**
- Ensure backend agent is running (`python src\agent.py dev`)
- Check browser console for WebSocket errors
- Verify all three services are running (LiveKit server, backend, frontend)

**No audio output**
- Check browser microphone permissions
- Ensure `MURF_API_KEY` or Google TTS is configured in backend
- Look for TTS errors in backend terminal logs

---

## 📝 Submission Checklist

- [ ] Agent responds with improv-style "Yes, and" replies
- [ ] Energy detection adapts to user's tone
- [ ] Conversations feel natural and playful
- [ ] Post on LinkedIn BEFORE 12PM IST Dec 2
- [ ] Mention using **Murf Falcon - the fastest TTS API**
- [ ] Submit form: https://forms.gle/pV8AnocDfk1RZgyD7

---

## 🎓 What You'll Learn

- Real-time voice agent architecture with LiveKit
- Dynamic prompt engineering for conversational AI
- Energy/sentiment detection from transcriptions
- Event-driven agent design patterns
- Integrating STT, LLM, and TTS pipelines

---

## 📦 Project Structure

```
Day_10/
├── backend/
│   ├── src/
│   │   └── agent.py          # Main agent logic & improv mechanics
│   ├── tests/
│   ├── .env.example          # Environment template
│   └── pyproject.toml        # Python dependencies
├── frontend/
│   ├── app/                  # Next.js pages
│   ├── components/           # React components
│   ├── .env.example          # Frontend config template
│   └── package.json          # Node dependencies
├── livekit-server.exe        # Local LiveKit server
└── README.md                 # This file
```

---

## 🤝 Support

For questions, post in the **🤖︱voice-agents-challenge** Discord channel.

---

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Good luck with your Voice Improv Battle agent! 🎭🎤** 
