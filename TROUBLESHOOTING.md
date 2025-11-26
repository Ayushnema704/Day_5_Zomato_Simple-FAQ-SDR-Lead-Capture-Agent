# 🔧 Troubleshooting Guide - Day 5 Zomato SDR Agent

Quick solutions to common issues you might encounter with the Zomato FAQ & Lead Capture agent.

---

## 🚨 Backend Issues

### Problem: "Module not found" error
```
ModuleNotFoundError: No module named 'livekit'
```

**Solution:**
```powershell
cd backend
# Activate virtual environment
.\venv\Scripts\activate
# Install dependencies
pip install -e .
```

---

### Problem: Agent starts but doesn't respond
```
Agent is silent, no voice output
```

**Checklist:**
1. ✅ Check `.env.local` has all required API keys
2. ✅ Verify MURF_API_KEY is valid
3. ✅ Check backend terminal for errors
4. ✅ Ensure LIVEKIT_URL is correct

**Verify API Keys:**
```powershell
cd backend
cat .env.local
# Should show all keys populated
```

---

### Problem: "Connection refused" to LiveKit
```
ConnectionError: [Errno 111] Connection refused
```

**Solution:**
```powershell
# Check if LiveKit server is running
# Terminal 1 should show:
.\livekit-server.exe --dev

# Or update LIVEKIT_URL in .env.local to use cloud:
LIVEKIT_URL=wss://your-livekit-cloud-url
```

---

### Problem: FAQ not loading
```
zomato_faq.json file not found or corrupted
```

**Debug Steps:**
1. Check if file exists:
```powershell
cd backend
Test-Path "zomato_faq.json"
# Should return True
```

2. Verify JSON is valid:
```powershell
Get-Content zomato_faq.json | ConvertFrom-Json
# Should parse without errors
```

3. Check backend logs for loading errors

---

### Problem: Leads not being saved
```
leads.json empty or not created after conversation
```

**Debug Steps:**
1. Check backend terminal for save errors
2. Verify write permissions in backend folder
3. Check if `capture_lead` tool is being called:
```powershell
# Look in backend logs for:
# "Captured lead: [name]"
```

**Check Permissions:**
```powershell
cd backend
New-Item -Path "leads.json" -ItemType File -Force
# If this fails, you have permission issues
```

---

### Problem: Agent doesn't use FAQ data
```
Agent gives generic answers instead of using FAQ
```

**Possible Causes:**
1. `search_faq` tool not being called
2. FAQ file not loaded properly
3. LLM not recognizing when to search FAQ

**Debug:**
```powershell
# Check backend logs for tool invocations
# Look for lines like:
# "Searching FAQ for: [query]"
# "Found FAQ matches: ..."
```

**Test FAQ loading:**
```powershell
cd backend
python -c "from src.agent import load_faq_content; print(load_faq_content())"
# Should display FAQ data
```

---

## 🎨 Frontend Issues

### Problem: Frontend won't start
```
Error: Cannot find module 'next'
```

**Solution:**
```powershell
cd frontend
# Delete node_modules and reinstall
Remove-Item -Recurse -Force node_modules
pnpm install
```

---

### Problem: "Module not found" in frontend
```
Module not found: Can't resolve '@/components/...'
```

**Solution:**
This is usually a build cache issue:
```powershell
cd frontend
# Clear Next.js cache
Remove-Item -Recurse -Force .next
# Restart dev server
pnpm dev
```

---

### Problem: Zomato branding not showing
```
UI doesn't show Zomato logo or red theme
```

**Solution:**
1. Hard refresh browser (Ctrl+Shift+R)
2. Clear browser cache
3. Check if logo exists:
```powershell
cd frontend\public
Test-Path "logo.png"
# Should return True
```

4. Verify app-config.ts:
```powershell
cd frontend
Get-Content app-config.ts | Select-String "Zomato"
# Should show Zomato branding
```

---

### Problem: Welcome screen shows old content
```
Still shows "Active Recall Coach" or wellness messaging
```

**Solution:**
```powershell
cd frontend
# Force rebuild
Remove-Item -Recurse -Force .next
pnpm dev
# Hard refresh browser (Ctrl+Shift+R)
```

---

## 🎤 Audio/Voice Issues

### Problem: Microphone not working
```
No audio input detected
```

**Solutions:**
1. **Browser Permissions:**
   - Chrome: Settings → Privacy → Site Settings → Microphone
   - Allow access for localhost:3000

2. **System Permissions:**
   - Windows Settings → Privacy → Microphone
   - Ensure browser has access

3. **Test Microphone:**
   - Open browser's DevTools (F12)
   - Console tab
   - Paste: `navigator.mediaDevices.getUserMedia({audio: true})`
   - Should request permission

---

### Problem: Can't hear agent voice
```
Agent talks (shows in transcript) but no audio
```

**Checklist:**
1. ✅ Check system volume
2. ✅ Check browser tab isn't muted
3. ✅ Verify MURF_API_KEY is valid
4. ✅ Check browser audio permissions
5. ✅ Try different browser (Chrome recommended)

---

### Problem: Voice is robotic/choppy
```
TTS sounds broken or stuttering
```

**Causes:**
- Slow internet connection
- API rate limiting
- Server overload

**Solution:**
```powershell
# In backend .env.local, ensure:
# Using Murf's fastest model
# Check backend logs for latency warnings
```

---

## 🌐 Connection Issues

### Problem: Frontend can't connect to backend
```
Error: WebSocket connection failed
```

**Debug:**
1. Verify backend is running:
```powershell
# Check if Python process is running
Get-Process python
```

2. Check backend logs for errors

3. Verify ports aren't blocked:
```powershell
# Test if port 7880 is accessible
Test-NetConnection -ComputerName localhost -Port 7880
```

---

### Problem: "CORS" error in browser console
```
Access to fetch blocked by CORS policy
```

**Solution:**
This shouldn't happen with the default setup, but if it does:
1. Ensure both frontend and backend are running
2. Check frontend .env.local for correct API URL
3. Restart both services

---

## 💾 Data/Persistence Issues

### Problem: Leads database empty
```
leads.json shows [] or doesn't contain captured leads
```

**Debug:**
1. Check if `leads.json` exists and has data:
```powershell
cd backend
Get-Content leads.json | ConvertFrom-Json
```

2. Verify `capture_lead` is being called:
   - Check backend logs for "Captured lead:"
   - Agent should ask for name, email, company during conversation

3. Test manually:
```powershell
cd backend
python -c "from src.agent import load_leads; print(load_leads())"
# Should show captured leads
```

---

### Problem: JSON file corrupted
```
JSONDecodeError: Expecting value
```

**Solution:**
```powershell
cd backend
# Backup corrupted file
Copy-Item leads.json leads.json.backup
# Create fresh file
echo "[]" > leads.json
```

---

### Problem: Lead data not in expected format
```
KeyError: 'email' or 'company'
```

**Verify Schema:**
```powershell
cd backend
python
>>> import json
>>> with open('leads.json') as f:
...     data = json.load(f)
>>> print(json.dumps(data[0], indent=2))
# Should have: name, email, company, role, use_case, etc.
```

**Expected Lead Structure:**
```json
{
  "timestamp": "2025-11-26T18:57:25",
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Restaurant ABC",
  "role": "Owner",
  "use_case": "Food delivery expansion",
  "team_size": "10-50",
  "timeline": "Within 3 months",
  "notes": "Interested in Hyperpure and delivery",
  "source": "Voice SDR Agent"
}
```

---

## 🔐 API Key Issues

### Problem: "Invalid API key" errors
```
401 Unauthorized or 403 Forbidden
```

**Verify Keys:**
```powershell
cd backend
# Check if keys are set
cat .env.local | Select-String "API_KEY"
# All should have values (not empty)
```

**Test Keys:**
1. **Google (Gemini):**
   ```powershell
   curl -H "Content-Type: application/json" `
   -d '{\"contents\":[{\"parts\":[{\"text\":\"Hello\"}]}]}' `
   "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-exp:generateContent?key=YOUR_KEY"
   ```

2. **Deepgram:**
   ```powershell
   curl -H "Authorization: Token YOUR_KEY" `
   "https://api.deepgram.com/v1/projects"
   ```

---

## 🐛 General Debugging Tips

### Enable Verbose Logging
```python
# In backend/src/agent.py, add at top:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Backend Logs
Look for these key messages:
- ✅ "Agent session started"
- ✅ "Searching FAQ for: [query]"
- ✅ "Captured lead: [name]"
- ✅ "Leads saved successfully"

### Check Frontend Console
Open DevTools (F12) and look for:
- ✅ WebSocket connected
- ✅ No CORS errors
- ✅ Audio permissions granted

### Test Individual Components

**Test Backend Only:**
```powershell
cd backend
.\venv\Scripts\python.exe src\agent.py dev
# Should start without frontend
```

**Test Frontend Only:**
```powershell
cd frontend
pnpm dev
# Should show UI (even if backend not running)
```

---

## 📱 Browser-Specific Issues

### Chrome
- Usually works best
- Check chrome://settings/content/microphone

### Firefox
- May need to enable WebRTC
- about:config → media.navigator.enabled = true

### Edge
- Similar to Chrome
- Check edge://settings/content/microphone

### Safari
- May have stricter permissions
- Check Settings → Safari → Microphone

---

## 🔄 Complete Reset

If nothing else works:

```powershell
# 1. Stop all processes
# Close all PowerShell windows

# 2. Clean backend
cd backend
Remove-Item -Recurse -Force venv
Remove-Item -Recurse -Force *.egg-info
python -m venv venv
.\venv\Scripts\activate
pip install -e .

# 3. Clean frontend
cd ..\frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Recurse -Force .next
pnpm install

# 4. Restart
cd ..
.\start_app.ps1
```

---

## 📞 Getting Help

If you're still stuck:

1. **Check Logs:**
   - Backend terminal output
   - Browser DevTools console
   - Look for specific error messages

2. **Isolate the Problem:**
   - Does backend start? ✅
   - Does frontend start? ✅
   - Can you connect? ✅
   - Does audio work? ✅
   - Do tools work? ✅

3. **Ask for Help:**
   - Post in Discord: ⁠🤖︱voice-agents-challenge
   - Include:
     - What you tried
     - Error messages
     - Screenshots
     - OS/Browser info

4. **Search Resources:**
   - [LiveKit Docs](https://docs.livekit.io/)
   - [GitHub Issues](https://github.com/livekit/agents/issues)
   - [Murf API Docs](https://murf.ai/api/docs)
   - [Discord Community](https://livekit.io/discord)

---

## ✅ Verification Checklist

Before asking for help, verify:
- [ ] Python 3.9+ installed: `python --version`
- [ ] pnpm installed: `pnpm --version`
- [ ] All API keys in `.env.local` (Murf, Google, Deepgram)
- [ ] Virtual environment activated (backend)
- [ ] Dependencies installed (`pip install -e .`)
- [ ] No firewall blocking ports 7880, 3000
- [ ] Microphone permissions granted
- [ ] Using supported browser (Chrome/Edge recommended)
- [ ] `zomato_faq.json` exists in backend folder
- [ ] `leads.json` created (empty array `[]` is OK)

---

## 🎯 Success Indicators

Your Zomato SDR setup is working if:
- ✅ Backend shows "Agent session started"
- ✅ Frontend loads at http://localhost:3000
- ✅ You see Zomato branding and logo
- ✅ You can click "Talk to Zomato"
- ✅ You hear the agent introduce itself as Zomato SDR
- ✅ Agent answers FAQ questions accurately
- ✅ Agent captures your contact information
- ✅ `leads.json` populated after conversation
- ✅ Chat transcript shows conversation flow

---

## 🧪 Testing the SDR Agent

**Test FAQ Search:**
1. Say: "What does Zomato do?"
2. Agent should search FAQ and provide accurate answer
3. Check backend logs for "Searching FAQ for: What does Zomato do"

**Test Lead Capture:**
1. Have a natural conversation
2. Provide name, email, company when asked
3. Check `leads.json` for your entry
4. Should include timestamp, contact info, and notes

---

**Remember: Most issues are simple configuration problems. Check API keys and file permissions first!** 🔧
