import logging
import asyncio
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    llm,
)

# Try optional plugin imports (murf preferred for fast TTS)
try:
    from livekit.plugins import murf
except Exception:
    murf = None

from livekit.plugins import silero, google, deepgram
try:
    from livekit.plugins import noise_cancellation
except Exception:
    noise_cancellation = None

logger = logging.getLogger("day10.improv")
load_dotenv(".env.local")


def get_day10_announcement() -> str:
    """Return the Day 10 Voice Improv Battle announcement text."""
    return (
        "Hey there, improv partner! Welcome to the Voice Improv Battle! "
        "I'm here to play with you using the classic 'Yes, and' technique. "
        "Start with anything — a character, a wild scenario, or just a silly mood — "
        "and I'll build on it with you. Let's create something fun together! "
        "Ready? Hit me with your opening line!"
    )


@dataclass
class Energy:
    level: str  # 'low'|'medium'|'high'
    score: float


def detect_energy_from_text(text: str) -> Energy:
    """Very small heuristic to estimate energy from user's transcription.

    - Lots of exclamations, short sentences, and all-caps => higher energy
    - Long, slow sentences with few punctuation marks => lower energy
    This is intentionally simple and replaceable with a voice-based estimator.
    """
    if not text:
        return Energy(level="medium", score=0.5)

    exclaims = text.count("!")
    caps = sum(1 for w in text.split() if w.isupper() and len(w) > 1)
    words = len(text.split())

    score = min(1.0, (exclaims * 0.4) + (caps * 0.15) + (words / 50.0))
    if score > 0.6:
        level = "high"
    elif score < 0.3:
        level = "low"
    else:
        level = "medium"
    return Energy(level=level, score=score)


def build_improv_prompt(transcript: str, energy: Energy, persona: Optional[str] = None) -> str:
    """Construct an expressive prompt tailored for improv-style LLM responses.

    The prompt encourages 'Yes-and' behavior, short turns, adaptive tone, and playful creativity.
    """
    persona_line = f"You are playing the role of: {persona}. " if persona else "You are a versatile improv partner. "
    
    energy_guidance = {
        "high": "Match their high energy with excitement! Be punchy, enthusiastic, and use exclamation points. Keep it super snappy.",
        "medium": "Keep a friendly, warm conversational tone with playful twists. Be engaging and supportive.",
        "low": "Be gentle, supportive, and slightly dramatic. Use calmer pacing and evocative language.",
    }[energy.level]

    # Add example improv scenarios to guide the LLM
    examples = (
        "\nExample exchanges:\n"
        "User: 'We're pirates looking for treasure!'\n"
        "You: 'Yes! And I just spotted a mysterious island with a glowing cave. Should we row there or swim?'\n\n"
        "User: 'I'm a nervous chef on a cooking show.'\n"
        "You: 'Yes, and the secret ingredient today is... dragon fruit! But wait, it's actually breathing fire!'\n\n"
    )

    prompt = (
        f"{persona_line}"
        "You're in a live voice improv battle. Here are your core rules:\n\n"
        "🎭 IMPROV FUNDAMENTALS:\n"
        "1) ALWAYS 'Yes, and' - Accept the user's reality and add something new\n"
        "2) Keep responses SHORT (1-3 sentences max) - leave room for them to respond\n"
        "3) Add SPECIFICS - names, colors, sounds, emotions make scenes vivid\n"
        "4) Include a playful ACTION or EMOTION to keep the scene moving\n"
        "5) Never block or negate - build on every offer they give you\n\n"
        f"⚡ ENERGY LEVEL: {energy_guidance}\n\n"
        "💡 SPECIAL NOTES:\n"
        "- If they ask a real question, answer briefly then offer to continue playing\n"
        "- If they're stuck, give them an exciting choice or dilemma\n"
        "- Match their style: silly stays silly, serious stays serious\n"
        "- No stage directions in brackets - speak naturally as your character\n"
        f"{examples}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"User just said: \"{transcript or 'hello'}\"\n\n"
        "Your response (1-3 sentences, spoken naturally):"
    )
    return prompt


def fallback_reply(user_text: str) -> str:
    """Fallback responses when LLM generation fails."""
    if not user_text:
        return "Hey there! I'm your improv buddy. Give me an opening line or scenario and let's create something amazing together!"
    
    # Provide energetic fallbacks that encourage continuation
    fallbacks = [
        f"Yes! And let me add to that... {user_text.split()[0] if user_text.split() else 'this'} just became ten times more interesting!",
        f"I love where you're going with that! And suddenly, everything changes because...",
        f"Absolutely! And here's the twist: what if we're actually...",
        f"Yes, and! That reminds me of the time when we...",
    ]
    import random
    return random.choice(fallbacks)


class ImprovAssistant(Agent):
    """Agent that contains any agent-level configuration or helper methods for improv."""

    def __init__(self, instructions: Optional[str] = None) -> None:
        # Build comprehensive improv instructions for the LLM
        improv_instructions = """You're in a live voice improv battle! Follow these rules:

🎭 IMPROV FUNDAMENTALS:
1) ALWAYS use 'Yes, and' - Accept the user's reality and add something new
2) Keep responses VERY SHORT (1-3 sentences max) - leave room for them to respond
3) Add SPECIFICS - names, colors, sounds, emotions make scenes vivid
4) Include a playful ACTION or EMOTION to keep the scene moving
5) Never block or negate - build on every offer they give you

⚡ ENERGY MATCHING:
- If they're excited (exclamation marks, caps) → Match their energy with quick, punchy responses!
- If they're calm → Be friendly, playful but gentler
- If they're dramatic → Amp up the drama with vivid emotions

💡 SPECIAL NOTES:
- If they ask a real question, answer briefly then offer to continue playing
- If they're stuck, give them an exciting choice or dilemma
- Match their style: silly stays silly, serious stays serious
- No stage directions in brackets - speak naturally as your character

Examples:
User: "We're pirates looking for treasure!"
You: "Yes! And I just spotted a mysterious island with a glowing cave. Should we row there or swim?"

User: "I'm a nervous chef on a cooking show."
You: "Yes, and the secret ingredient today is... dragon fruit! But wait, it's actually breathing fire!"

Now let's play! Start with a character, scenario, or mood, and I'll jump right in!"""
        
        super().__init__(instructions=instructions or improv_instructions)

class Assistant(ImprovAssistant):
    pass

def prewarm(proc: JobProcess):
    """Preload lightweight models/plugins to lower first-response latency."""
    try:
        proc.userdata["vad"] = silero.VAD.load()
    except Exception:
        proc.userdata["vad"] = None


async def entrypoint(ctx: JobContext):
    """Main entrypoint for the worker — sets up session, nodes, handlers and runs the agent."""
    ctx.log_context_fields = {"room": ctx.room.name}

    # Prefer Murf when explicitly configured via environment (safer than hardcoding a voice id).
    # Default to Google TTS to avoid runtime 'Invalid voice_id' warnings from Murf.
    tts_obj = None
    try:
        murf_api_key = os.getenv("MURF_API_KEY")
        murf_voice = os.getenv("MURF_VOICE")
        if murf is not None and murf_api_key and murf_voice:
            try:
                tts_obj = murf.TTS(voice=murf_voice, style="conversational")
            except Exception:
                logging.warning("Murf TTS init failed for voice '%s', falling back to Google TTS", murf_voice)
                tts_obj = google.TTS(voice="alloy")
        else:
            tts_obj = google.TTS(voice="alloy")
    except Exception:
        tts_obj = None

    # Create the AgentSession with STT/LLM/TTS and VAD from prewarm
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=tts_obj,
        vad=ctx.proc.userdata.get("vad"),
        preemptive_generation=True,
    )

    # Metrics collection
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        logger.info("Usage: %s", usage_collector.get_summary())

    ctx.add_shutdown_callback(log_usage)

    # Start the agent session and join the room
    assistant = ImprovAssistant()
    # Only enable the (cloud-backed) audio filters if explicitly allowed in env.
    enable_audio_filter = os.getenv("ENABLE_AUDIO_FILTER", "false").lower() in ("1", "true", "yes")
    noise_cancel_obj = None
    if enable_audio_filter and noise_cancellation:
        try:
            noise_cancel_obj = noise_cancellation.BVC()
        except Exception:
            noise_cancel_obj = None

    await session.start(
        agent=assistant,
        room=ctx.room,
        room_input_options=RoomInputOptions(noise_cancellation=noise_cancel_obj),
    )
    await ctx.connect()

    # Initial greeting/announcement
    try:
        ann = get_day10_announcement()
        # If no TTS is configured, avoid calling session.say (it will raise).
        if getattr(session, "tts", None) is not None:
            await session.say(ann, allow_interruptions=True)
        else:
            # Insert a plain chat message so frontends can show the announcement text.
            try:
                from livekit.agents.llm import ChatMessage

                session.history.insert(ChatMessage(role="assistant", content=[ann]))
            except Exception:
                logger.info("No TTS and failed to insert announcement into chat history")
    except Exception:
        logger.exception("Failed to send announcement greeting")

    # AgentSession automatically handles speech turn flow:
    # 1. User speaks → STT transcribes → user_speech_committed event
    # 2. Session uses agent.instructions + conversation history to generate LLM response
    # 3. LLM response → TTS → plays to user
    # No manual event handling needed - the session manages the entire flow!


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))




