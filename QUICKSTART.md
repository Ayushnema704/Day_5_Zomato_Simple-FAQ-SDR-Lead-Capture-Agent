# 🚀 Quick Start Guide - Day 10 Voice Improv Battle

## ✅ Current Status

Your project is **READY TO USE**! Here's what's already running:

- ✅ Frontend: **Running on http://localhost:3000**
- ✅ Backend Agent: **Running and processing audio**
- ✅ LiveKit Server: **Active on ws://127.0.0.1:7880**

---

## 🎯 Test Your Agent RIGHT NOW

1. **Open your browser**: http://localhost:3000

2. **Click "Connect"** or **"Join Day 10 Challenge"**

3. **Allow microphone access** when prompted

4. **Start talking!** Try these example scenarios:

   - *"We're astronauts who just discovered a singing alien!"*
   - *"I'm a nervous superhero on my first day!"*
   - *"Let's pretend we're time travelers at a medieval feast!"*
   - *"We're detectives investigating a cookie theft!"*

5. **Watch the agent respond** with "Yes, and..." style improv!

---

## 🎭 What Makes This Special

### Energy Detection
The agent analyzes your speech and adapts its energy:
- **High energy** (lots of !, CAPS) → Quick, punchy responses
- **Medium energy** → Friendly, playful tone
- **Low energy** → Gentle, supportive, dramatic

### "Yes, and..." Technique
Every response:
- ✅ Accepts your reality
- ✅ Adds something new
- ✅ Keeps the scene moving
- ✅ Stays brief (1-3 sentences)

### Example Exchange

**You**: *"We're pirates looking for treasure!"*

**Agent**: *"Yes! And I just spotted a mysterious island with a glowing cave. Should we row there or swim?"*

**You**: *"Let's swim! But I can't swim very well..."*

**Agent**: *"Don't worry! And look, there are friendly dolphins offering us a ride! Quick, grab a fin!"*

---

## 📝 Known Issues (All Safe to Ignore)

### Backend Logs

✅ **"error: failed to fetch server settings: http status: 404"**
- This is from LiveKit SDK trying to fetch cloud settings
- Doesn't affect functionality - your agent is working fine!
- You can see STT metrics flowing (Deepgram nova-3)

✅ **"audio filter cannot be enabled: LiveKit Cloud is required"**
- Already handled in code with `ENABLE_AUDIO_FILTER=false`
- Only needed for LiveKit Cloud deployments

### Frontend

✅ **Previous "exit code 1" message**
- Frontend is actually running correctly on port 3000
- This was a terminal display issue, not a real error

---

## 🎤 Testing Tips

### Good Opening Lines
- Start with a character: *"I'm a nervous chef..."*
- Start with a location: *"We're on a spaceship..."*
- Start with a problem: *"The dragon stole my homework!"*
- Start with a mood: *"I'm feeling super dramatic today!"*

### What to Look For
✅ Agent always accepts your idea (never says "no")
✅ Responses are short and leave room for you
✅ Energy matches yours
✅ Each response adds something new
✅ Conversation feels playful and fun

---

## 🔧 If Something Goes Wrong

### No Audio Output
```powershell
# Check if backend is running
cd backend
python src\agent.py dev
```

### Can't Connect
```powershell
# Restart LiveKit server
.\livekit-server.exe --dev
```

### Frontend Not Loading
```powershell
# Restart frontend
cd frontend
pnpm dev
```

### Check All Services
```powershell
# Check what's running
Get-Process -Name node,python,livekit* -ErrorAction SilentlyContinue | Format-Table Id,ProcessName,CPU -AutoSize

# Check ports
netstat -ano | Select-String "LISTENING" | Select-String ":3000|:7880"
```

---

## 📤 Ready to Submit?

### Submission Checklist

- [ ] Test agent with 3-5 different scenarios
- [ ] Verify "Yes, and" responses work
- [ ] Confirm energy detection adapts
- [ ] Take a screenshot or screen recording
- [ ] Post on LinkedIn with these key points:
  - Building a voice agent for Day 10 challenge
  - Using **Murf Falcon - the fastest TTS API**
  - Mention improv "Yes, and" technique
  - Tag relevant people/companies
- [ ] Submit form: https://forms.gle/pV8AnocDfk1RZgyD7

### Deadline
**December 2, 2025 at 12PM IST** - Don't miss it!

---

## 🎬 Next Steps

1. **Test now**: Open http://localhost:3000 and play!
2. **Record demo**: Screen record a fun improv exchange
3. **Post LinkedIn**: Before 12PM IST Dec 2
4. **Submit form**: https://forms.gle/pV8AnocDfk1RZgyD7

---

## 💡 Advanced: Customize Your Agent

### Change Personality
Edit `backend/src/agent.py`:
```python
def build_improv_prompt(transcript: str, energy: Energy, persona: Optional[str] = None):
    # Add your own persona
    persona = "a witty pirate captain"
```

### Adjust Energy Thresholds
```python
def detect_energy_from_text(text: str) -> Energy:
    # Modify scoring logic
    score = min(1.0, (exclaims * 0.4) + (caps * 0.15))
```

### Add Custom Fallbacks
```python
def fallback_reply(user_text: str) -> str:
    fallbacks = [
        "Your custom fallback here!",
        # Add more...
    ]
```

---

## 🆘 Support

Questions? Post in **🤖︱voice-agents-challenge** Discord channel.

---

**You're all set! Go play with your improv agent! 🎭🎤**
