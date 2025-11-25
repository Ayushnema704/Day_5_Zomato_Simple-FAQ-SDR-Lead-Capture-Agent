# Active Recall Coach - Teach to Learn

**Day 4 Challenge - Educational Voice Agent with Multi-Mode Learning**

Active Recall Coach is an AI-powered tutoring agent that helps you master programming concepts through the proven "teach-the-tutor" method. Built with LiveKit Agents and Murf Falcon TTS, it supports three distinct learning modes to reinforce your understanding through active recall.

## About This Project

Part of the **AI Voice Agents Challenge** by [murf.ai](https://murf.ai), Active Recall Coach demonstrates how AI voice agents can facilitate learning through interactive teaching, quizzing, and knowledge reinforcement.

### Key Features

- 🎙️ **Three Learning Modes** - Learn, Quiz, and Teach Back for comprehensive mastery
- 📚 **Learn Mode** - Agent teaches programming concepts clearly (Matthew voice)
- ❓ **Quiz Mode** - Test your knowledge with targeted questions (Alicia voice)
- 🎓 **Teach Back Mode** - Explain concepts and receive feedback (Ken voice)
- 🔄 **Seamless Mode Switching** - Switch between modes anytime during your session
- 📊 **Progress Tracking** - Logs learning sessions for future analysis
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

The active recall tutoring agent built with LiveKit Agents framework.

**Technologies:**

- **TTS**: Murf Falcon (Matthew for Learn, Alicia for Quiz, Ken for Teach Back)
- **STT**: Deepgram nova-3
- **LLM**: Google Gemini 2.5-flash
- **VAD**: Silero (Windows compatible)

**Learning Tools:**

- `get_concept(concept_id)` - Loads programming concepts from content library
- `save_learning_session(mode, concept_id, notes)` - Tracks learning progress
- Automatic mode-based behavior
- Educational, encouraging conversation patterns

**Content:**
- `tutor_content.json` - Programming concepts (variables, loops, functions, conditionals)

[→ Backend Documentation](./backend/README.md)

### Frontend

Next.js 15 application with real-time voice and chat interface.

**Features:**

- Real-time voice interaction with LiveKit
- Live chat transcript (visible by default)
- Education-themed branding (blue accent, learning-focused design)
- Audio visualization and controls
- "Start Learning Session" button
- Responsive, accessible UI
- Learning mode indicators

**Customization:**
- Branding configured in `app-config.ts`
- Landing page highlights three learning modes
- Session state optimized for educational conversations

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
git clone https://github.com/Ayushnema704/Day_4_Active_Recall_Coach.git
cd Day_4_Active_Recall_Coach
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

**Access the app:** Open http://localhost:3000 in your browser and click **"Start Learning Session"**

## How It Works

1. **Connect** - Click "Start Learning Session" to begin
2. **Greet** - Agent welcomes you: "Hello! Welcome to your Active Recall Coach. I'm here to help you master programming concepts through three learning modes: Learn, Quiz, and Teach Back. Which mode would you like to start with?"
3. **Choose Mode** - Select your learning mode through voice or chat
4. **Learn** - Agent adapts behavior based on mode:
   - **Learn Mode**: Explains concepts using summaries from content library
   - **Quiz Mode**: Asks questions to test your understanding
   - **Teach Back Mode**: Listens to your explanations and provides feedback
5. **Switch Anytime** - Say "switch to quiz mode" or "let me teach this back" to change modes
6. **Track Progress** - Learning sessions saved to `learning_log.json`

### Sample Conversation

```
Agent: "Which learning mode would you like to start with?"
User: "Let's start with learn mode."
Agent: [Calls get_concept("variables")]
      "Great! Let me explain variables. Variables are containers that store data values..."
User: "I think I understand. Can you quiz me on this?"
Agent: "Switching to quiz mode! What is a variable and why is it useful?"
User: [Explains variables]
Agent: "Excellent explanation! You've captured the key concepts..."
      [Calls save_learning_session("quiz", "variables")]
```

## Project Customizations

Active Recall Coach includes several optimizations for educational conversations:

- **Multi-Voice Support** - Different Murf Falcon voices for each mode (Matthew, Alicia, Ken)
- **Mode-Aware Agent** - Single agent adapts behavior based on user's chosen learning mode
- **Chat Visibility** - Chat transcript visible by default (`chatOpen=true`)
- **Blue Branding** - Educational theme with `#3b82f6` accent color
- **Content Library** - JSON-based concept library (`tutor_content.json`)
- **Progress Tracking** - Learning sessions logged with mode, concept, and notes

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

**Microphone permission denied?**
- Allow microphone access in your browser settings
- Try using HTTPS or localhost (required for microphone access)

**Agent not switching modes?**
- Be explicit: "Switch to quiz mode" or "I want to try teach back mode"
- Agent will confirm the mode switch

## Resources

- [Murf Falcon TTS Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [Google Gemini API](https://ai.google.dev/docs)
- [Deepgram STT](https://developers.deepgram.com/)

## Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| TTS | Murf Falcon | Multi-voice support (Matthew, Alicia, Ken) |
| STT | Deepgram nova-3 | High-accuracy speech recognition |
| LLM | Google Gemini 2.5-flash | Educational conversation intelligence |
| VAD | Silero | Voice activity detection |
| Backend | LiveKit Agents (Python) | Agent orchestration with mode switching |
| Frontend | Next.js 15 + LiveKit React | Real-time learning UI |
| Storage | JSON | Learning sessions & concept library |

## Future Enhancements

- 📊 Mastery scoring system (track concept understanding over time)
- 🎯 Personalized learning paths based on weakest concepts
- 🔢 Teach-back evaluator with automated scoring (0-100)
- 💾 Database integration (SQLite/MongoDB) for richer data
- 📚 Expanded content library with more programming topics
- 🏆 Achievement system and learning streaks
- 📱 Mobile app version
- 🔒 User authentication and progress sync

## License

This project is based on MIT-licensed templates from LiveKit. See individual LICENSE files in backend and frontend directories.

## Acknowledgments

- Built for the **AI Voice Agents Challenge** by [murf.ai](https://murf.ai)
- Based on [LiveKit's agent starter templates](https://github.com/livekit-examples)
- Uses [Murf Falcon TTS](https://murf.ai/api) for voice synthesis

---

**Day 4 Challenge Submission** | Built with 📚 for education and active learning
