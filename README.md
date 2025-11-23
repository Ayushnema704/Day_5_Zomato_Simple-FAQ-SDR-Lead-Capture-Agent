# MindfulMate - AI Wellness Companion

**Day 3 Challenge - Personal Wellness Voice Agent**

MindfulMate is an empathetic AI wellness companion built with LiveKit Agents and Murf Falcon TTS. It provides personalized daily wellness check-ins, tracks your emotional and physical well-being, and offers supportive guidance through natural voice conversations.

## About This Project

Part of the **AI Voice Agents Challenge** by [murf.ai](https://murf.ai), MindfulMate demonstrates how AI voice agents can provide mental health support and wellness tracking through natural, empathetic conversations.

### Key Features

- 🎙️ **Natural Voice Conversations** - Ultra-fast, human-like responses using Murf Falcon TTS
- 💚 **Wellness Check-ins** - Track mood, energy levels, sleep, and stress
- 📊 **Historical Tracking** - Saves and retrieves past check-ins to provide personalized insights
- 🤝 **Empathetic Support** - Designed with trauma-informed, non-judgmental conversation patterns
- 💬 **Real-time Chat** - Text-based chat alongside voice interaction

## Repository Structure

```
Mindful-Health-Agent/
├── backend/          # Python agent with wellness tracking logic
│   ├── src/
│   │   └── agent.py  # Main agent with wellness tools
│   └── wellness_log.json  # Persistent check-in storage
├── frontend/         # Next.js UI with voice interface
├── start_app.ps1     # Windows startup script
└── README.md         # This file
```

### Backend

The wellness companion agent built with LiveKit Agents framework.

**Technologies:**

- **TTS**: Murf Falcon (en-US-matthew voice, Conversation style)
- **STT**: Deepgram nova-3
- **LLM**: Google Gemini 2.5-flash
- **VAD**: Silero (Windows compatible)

**Wellness Tools:**

- `save_checkin()` - Saves wellness data to JSON with timestamps
- `retrieve_past_checkins()` - Loads and analyzes previous check-ins
- Automatic greeting on connection
- Trauma-informed conversation patterns

[→ Backend Documentation](./backend/README.md)

### Frontend

Next.js 15 application with real-time voice and chat interface.

**Features:**

- Real-time voice interaction with LiveKit
- Live chat transcript (visible by default)
- Wellness-themed branding (green accent, calming design)
- Audio visualization and controls
- "Start Wellness Check-In" button
- Responsive, accessible UI

**Customization:**
- Branding configured in `app-config.ts`
- Chat animations removed for immediate display
- Session state optimized for wellness conversations

[→ Frontend Documentation](./frontend/README.md)

## Quick Start

### Prerequisites

- **Python 3.9+** with virtual environment support
- **Node.js 18+** with pnpm (`npm install -g pnpm`)
- **LiveKit Server** - Download from [LiveKit releases](https://github.com/livekit/livekit/releases)
- **API Keys**:
  - [Murf Falcon API key](https://murf.ai/api)
  - [Google AI API key](https://makersuite.google.com/app/apikey)
  - [Deepgram API key](https://deepgram.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/Ayushnema704/Mindful-Health-Agent.git
cd Mindful-Health-Agent
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -e .

# Create .env.local with your credentials
# Copy from .env.example and fill in:
```

**backend/.env.local:**
```bash
LIVEKIT_URL=ws://127.0.0.1:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
GOOGLE_API_KEY=your_google_api_key_here
MURF_API_KEY=your_murf_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Create .env.local (same LiveKit credentials as backend)
```

**frontend/.env.local:**
```bash
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_URL=ws://127.0.0.1:7880
```

### 4. Run the Application

**Windows PowerShell:**
```powershell
# Terminal 1 - LiveKit Server
.\livekit-server.exe --dev

# Terminal 2 - Backend Agent
cd backend
.\venv\Scripts\python.exe src\agent.py dev

# Terminal 3 - Frontend
cd frontend
pnpm dev
```

**macOS/Linux:**
```bash
# Terminal 1 - LiveKit Server
livekit-server --dev

# Terminal 2 - Backend Agent
cd backend
source venv/bin/activate
python src/agent.py dev

# Terminal 3 - Frontend
cd frontend
pnpm dev
```

**Access the app:** Open http://localhost:3000 in your browser and click **"Start Wellness Check-In"**

## How It Works

1. **Connect** - Click "Start Wellness Check-In" to begin
2. **Greet** - Agent automatically greets you: "Hello! Welcome to MindfulMate. I'm here to help you with your daily wellness check-in. How are you feeling today?"
3. **Converse** - Share your feelings through voice or chat
4. **Track** - Agent saves your check-in data (mood, energy, sleep, stress) to `wellness_log.json`
5. **Reflect** - Agent recalls your past check-ins to provide personalized insights

### Sample Conversation

```
Agent: "Hello! Welcome to MindfulMate. How are you feeling today?"
User: "I'm feeling really tired and stressed about my exams."
Agent: "I hear you. Exam stress can be really exhausting..."
      [Asks about sleep, energy levels, coping strategies]
User: "I'd like to save this check-in."
Agent: [Calls save_checkin() tool]
      "I've saved your wellness check-in. Remember to take breaks!"
```

## Project Customizations

MindfulMate includes several optimizations for wellness conversations:

- **Simplified Greeting** - Skips automatic tool calls to reduce initial delay
- **Chat Visibility** - Chat transcript visible by default (`chatOpen=true`)
- **Animation Removal** - Removed framer-motion animations for immediate chat display
- **Green Branding** - Calming wellness theme with `#10b981` accent color
- **Persistent Storage** - JSON-based wellness log with timestamp tracking

## Troubleshooting

**Agent not responding?**
- Ensure all three services are running (LiveKit server, backend agent, frontend)
- Check that API keys are correct in `.env.local` files
- Restart backend agent if it shut down

**"Failed to fetch" error?**
- Restart frontend to reload environment variables: `pnpm dev`
- Verify `.env.local` exists in frontend directory

**Chat not visible?**
- Chat is now visible by default (fixed in `session-view.tsx`)

## Resources

- [Murf Falcon TTS Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [Google Gemini API](https://ai.google.dev/docs)
- [Deepgram STT](https://developers.deepgram.com/)

## Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| TTS | Murf Falcon | Ultra-fast, natural voice synthesis |
| STT | Deepgram nova-3 | High-accuracy speech recognition |
| LLM | Google Gemini 2.5-flash | Conversation intelligence |
| VAD | Silero | Voice activity detection |
| Backend | LiveKit Agents (Python) | Agent orchestration |
| Frontend | Next.js 15 + LiveKit React | Real-time UI |
| Storage | JSON | Wellness check-in persistence |

## Future Enhancements

- 📈 Data visualization for wellness trends
- 🔔 Reminder notifications for daily check-ins
- 🎯 Goal setting and progress tracking
- 🧘 Guided meditation and breathing exercises
- 📱 Mobile app version
- 🔒 User authentication and cloud storage

## License

This project is based on MIT-licensed templates from LiveKit. See individual LICENSE files in backend and frontend directories.

## Acknowledgments

- Built for the **AI Voice Agents Challenge** by [murf.ai](https://murf.ai)
- Based on [LiveKit's agent starter templates](https://github.com/livekit-examples)
- Uses [Murf Falcon TTS](https://murf.ai/api) for voice synthesis

---

**Day 3 Challenge Submission** | Built with ❤️ for wellness and mental health support
