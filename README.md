# Zomato SDR - AI-Powered FAQ & Lead Capture Agent

**Day 5 Challenge - Simple FAQ SDR Voice Agent with Lead Capture**

An intelligent Sales Development Representative (SDR) voice agent for Zomato that answers FAQs about the platform and captures qualified leads through natural conversation. Built with LiveKit Agents and Murf Falcon TTS for ultra-fast voice interactions.

## About This Project

Part of the **AI Voice Agents Challenge** by [murf.ai](https://murf.ai), this project demonstrates how AI voice agents can handle customer inquiries, answer FAQs from a knowledge base, and capture lead information organically through conversation.

### Key Features

- 🎙️ **Voice-First SDR** - Natural conversational sales representative
- 📚 **FAQ Knowledge Base** - Comprehensive Zomato product information in JSON
- 🎯 **Lead Qualification** - Captures name, email, company, role, and use case
- 💾 **Lead Persistence** - Saves qualified leads to JSON database
- 🔍 **Smart FAQ Search** - Semantic search through Zomato's services and pricing
- 💬 **Real-time Chat** - Text-based chat alongside voice interaction
- ⚡ **Lightning Fast** - Powered by Murf Falcon TTS (fastest TTS API)

## Repository Structure

```
Day_5_Zomato_SDR/
├── backend/              # Python agent with SDR logic
│   ├── src/
│   │   └── agent.py      # Main SDR agent with FAQ and lead capture
│   ├── zomato_faq.json   # Knowledge base for Zomato products/services
│   └── leads.json        # Captured lead storage
├── frontend/             # Next.js UI with Zomato branding
├── start_app.ps1         # Windows startup script
├── start_app.sh          # Unix/Mac startup script
└── README.md             # This file
```

### Backend

The SDR voice agent built with LiveKit Agents framework.

**Technologies:**

- **TTS**: Murf Falcon (ultra-fast voice synthesis)
- **STT**: Deepgram Nova-3
- **LLM**: Google Gemini 2.5-flash
- **VAD**: Silero (Windows compatible)

**SDR Tools:**

- `search_faq(query)` - Searches Zomato FAQ knowledge base
- `capture_lead(name, email, company, role, use_case, team_size, timeline, notes)` - Saves qualified leads
- Consultative conversation flow
- Natural lead qualification

**Knowledge Base:**
- `zomato_faq.json` - Comprehensive FAQ about Zomato's services, pricing, and features

[→ Backend Documentation](./backend/README.md)

### Frontend

Next.js 15 application with real-time voice and chat interface.

**Features:**

- Real-time voice interaction with LiveKit
- Live chat transcript for conversation tracking
- Zomato-themed branding (red accent, food-focused design)
- Audio visualization and controls
- "Talk to Zomato" CTA button
- Responsive, accessible UI
- Professional SDR interface

**Customization:**
- Branding configured in `app-config.ts`
- Landing page highlights Zomato partnership opportunities
- Session state optimized for sales conversations

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
git clone https://github.com/Ayushnema704/Day_5_Zomato_Simple-FAQ-SDR-Lead-Capture-Agent.git
cd Day_5_Zomato_Simple-FAQ-SDR-Lead-Capture-Agent
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

**Access the app:** Open http://localhost:3000 in your browser and click **"Talk to Zomato"**

## How It Works

1. **Connect** - Click "Talk to Zomato" to begin conversation
2. **Greeting** - SDR agent welcomes you: "Hello! Thanks for reaching out to Zomato. I'm here to help you explore how we can support your business. What brings you here today?"
3. **Discovery** - Agent asks about your business needs and challenges
4. **FAQ Answering** - When you ask questions about Zomato:
   - Agent calls `search_faq(query)` to find relevant information
   - Provides accurate answers from knowledge base
   - Never makes up information
5. **Lead Qualification** - Throughout conversation, agent organically captures:
   - Name, Email, Company (essential)
   - Role, Use case, Team size, Timeline, Additional notes
6. **Lead Capture** - When sufficient information is gathered, agent saves lead to `leads.json`
7. **Next Steps** - Agent confirms interest and provides appropriate next steps

### Sample Conversation

```
Agent: "Hello! Thanks for reaching out to Zomato. What brings you here today?"
User: "I own a restaurant and want to know about your delivery services."
Agent: "Great! I'd love to help. What's the name of your restaurant?"
User: "It's called Spartan Group of Hotels."
Agent: [Captures company name]
      "And may I have your name and the best email to reach you?"
User: "I'm Michael Scott, email is michael@spartanhotels.com"
Agent: [Calls search_faq("delivery services")]
      "Thanks Michael! For delivery, Zomato provides..."
Agent: [Later, calls capture_lead(...) with all collected information]
      "I've captured all your information. Our team will reach out within 24 hours!"
```

## Project Customizations

Zomato SDR includes several optimizations for sales conversations:

- **Consultative Approach** - Focuses on understanding needs before pitching
- **FAQ Knowledge Base** - Comprehensive Zomato product information
- **Lead Persistence** - All qualified leads saved to JSON with timestamp
- **Zomato Branding** - Red theme matching Zomato's brand identity
- **Natural Conversation** - Captures information organically, not through forms
- **Smart FAQ Search** - Semantic search through services, pricing, and features

## Troubleshooting

### Common Issues

**Agent not responding?**
- Ensure all three services are running (LiveKit server, backend agent, frontend)
- Check that all API keys are correct in `.env.local` files (Murf, Google, Deepgram)
- Verify `zomato_faq.json` exists in backend folder
- Restart backend agent if it shut down

**FAQ not working?**
- Check backend logs for "Searching FAQ for: [query]"
- Verify `zomato_faq.json` is valid JSON: `Get-Content backend\zomato_faq.json | ConvertFrom-Json`
- Agent should call `search_faq` tool when asked questions about Zomato

**Leads not being saved?**
- Check if `leads.json` exists in backend folder (empty `[]` is OK initially)
- Look for "Captured lead:" messages in backend terminal
- Verify write permissions in backend directory
- Agent needs at minimum: name, email, and company to save a lead

**"Failed to fetch" error?**
- Restart frontend to reload environment variables: `pnpm dev`
- Verify `.env.local` exists in both backend and frontend directories
- Check LIVEKIT_URL is set to `ws://127.0.0.1:7880` for local development

**Microphone permission denied?**
- Allow microphone access in browser settings (Chrome/Edge: Settings → Privacy → Microphone)
- Ensure you're using localhost or HTTPS (required for microphone access)
- Test mic: Open DevTools (F12) → Console → `navigator.mediaDevices.getUserMedia({audio: true})`

**Zomato branding not showing?**
- Hard refresh browser (Ctrl+Shift+R)
- Verify `frontend/public/logo.png` exists
- Check `app-config.ts` has Zomato branding
- Clear Next.js cache: `Remove-Item -Recurse -Force frontend\.next`

### Quick Reset
```powershell
# If nothing works, clean restart:
cd backend
Remove-Item -Recurse -Force venv, *.egg-info
python -m venv venv
.\venv\Scripts\activate
pip install -e .

cd ..\frontend
Remove-Item -Recurse -Force node_modules, .next
pnpm install
```

## Resources

- [Murf Falcon TTS Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [Google Gemini API](https://ai.google.dev/docs)
- [Deepgram STT](https://developers.deepgram.com/)

## Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| TTS | Murf Falcon | Ultra-fast, natural voice synthesis |
| STT | Deepgram Nova-3 | High-accuracy speech recognition |
| LLM | Google Gemini 2.5-flash | Sales conversation intelligence |
| VAD | Silero | Voice activity detection |
| Backend | LiveKit Agents (Python) | SDR agent orchestration |
| Frontend | Next.js 15 + LiveKit React | Real-time sales UI |
| Storage | JSON | Lead database & FAQ knowledge base |

## Future Enhancements

- 📊 Lead scoring and qualification pipeline
- 🔗 CRM integration (Salesforce, HubSpot)
- 📧 Automated follow-up email generation
- 💾 Database integration (PostgreSQL/MongoDB) for scalability
- 📈 Analytics dashboard for lead metrics
- 🎯 A/B testing for conversation flows
- 📱 Mobile app version
- 🔒 User authentication and admin panel
- 🌐 Multi-language support for global markets
- 🤖 Sentiment analysis for conversation quality

## License

This project is based on MIT-licensed templates from LiveKit. See individual LICENSE files in backend and frontend directories.

## Acknowledgments

- Built for the **AI Voice Agents Challenge** by [murf.ai](https://murf.ai)
- Based on [LiveKit's agent starter templates](https://github.com/livekit-examples)
- Uses [Murf Falcon TTS](https://murf.ai/api) for voice synthesis
- Zomato is a trademark of Zomato Ltd. (This is an educational demo project)

---

**Day 5 Challenge Submission** | Built with 🍽️ for sales and customer engagement
