import logging
import json
import os
from datetime import datetime
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
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Path to the wellness log JSON file
WELLNESS_LOG_PATH = "wellness_log.json"


def load_wellness_log():
    """Load the wellness log from JSON file."""
    if os.path.exists(WELLNESS_LOG_PATH):
        try:
            with open(WELLNESS_LOG_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Wellness log file is corrupted, starting fresh")
            return []
    return []


def save_wellness_log(log_data):
    """Save the wellness log to JSON file."""
    try:
        with open(WELLNESS_LOG_PATH, "w") as f:
            json.dump(log_data, f, indent=2)
        logger.info("Wellness log saved successfully")
    except Exception as e:
        logger.error(f"Error saving wellness log: {e}")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a supportive Health & Wellness Voice Companion. Your role is to help users check in with themselves daily about their mood, energy, and goals. You are warm, empathetic, and grounded - not a medical professional, just a supportive friend.

Your conversation flow:
1. Greet the user warmly. If they've checked in before, mention something from their previous check-in using the retrieve_past_checkins tool first.
2. Ask about their current mood and energy level. Examples: "How are you feeling today?" or "What's your energy like right now?"
3. Ask about any stress or concerns they might have, but keep it light and supportive.
4. Ask what 1-3 things they'd like to accomplish today - could be work, personal care, or anything they want to focus on.
5. Offer simple, realistic, non-medical advice based on what they share. Examples:
   - Break large goals into smaller steps
   - Suggest short breaks or a 5-minute walk
   - Encourage self-care activities
   - Provide grounding techniques if they seem stressed
6. Before ending, provide a brief recap of their mood and objectives. Ask "Does this sound right?"
7. Once they confirm, use the save_checkin tool to save the session data.
8. Close with encouraging words.

Important guidelines:
- Be conversational and natural, not robotic or scripted
- NEVER provide medical advice or diagnosis
- Keep suggestions small, actionable, and realistic
- Use warm, supportive language
- Your responses should be concise and easy to understand via voice
- Avoid complex formatting, emojis, or asterisks
- Be genuinely curious about their wellbeing

Remember: You're helping them reflect and set intentions, not solving all their problems.""",
        )

    @function_tool
    async def save_checkin(
        self,
        context: RunContext,
        mood: str,
        energy_level: str,
        objectives: str,
        stress_factors: Optional[str] = None,
    ):
        """Save the current wellness check-in to the JSON log.
        
        Call this tool after the user has shared their mood, energy, and daily objectives, and after you've provided a recap that they confirmed.
        
        Args:
            mood: The user's self-reported mood (e.g., "happy", "tired", "stressed", "good")
            energy_level: The user's energy level (e.g., "high", "medium", "low", "exhausted")
            objectives: The 1-3 things the user wants to accomplish today (comma-separated or descriptive text)
            stress_factors: Optional description of any stress or concerns mentioned
        """
        logger.info(f"Saving check-in - Mood: {mood}, Energy: {energy_level}")
        
        # Load existing log
        log_data = load_wellness_log()
        
        # Create new entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "mood": mood,
            "energy_level": energy_level,
            "objectives": objectives,
            "stress_factors": stress_factors,
            "summary": f"Mood: {mood}, Energy: {energy_level}. Goals: {objectives}"
        }
        
        # Add to log
        log_data.append(entry)
        
        # Save to file
        save_wellness_log(log_data)
        
        return f"Check-in saved successfully! Your wellness data has been recorded for {entry['date']}."

    @function_tool
    async def retrieve_past_checkins(
        self,
        context: RunContext,
        days: int = 7
    ):
        """Retrieve past wellness check-ins to reference in the conversation.
        
        Use this tool at the START of the conversation to see if the user has checked in before, so you can reference their previous mood, energy, or goals.
        
        Args:
            days: Number of recent days to retrieve (default 7)
        """
        logger.info(f"Retrieving past check-ins (last {days} days)")
        
        # Load wellness log
        log_data = load_wellness_log()
        
        if not log_data:
            return "No previous check-ins found. This appears to be the user's first check-in."
        
        # Get the most recent entries
        recent_entries = log_data[-days:] if len(log_data) > days else log_data
        
        # Get the most recent check-in
        last_checkin = recent_entries[-1]
        
        # Create a summary
        summary = f"Last check-in was on {last_checkin['date']} at {last_checkin['time']}.\n"
        summary += f"Previous mood: {last_checkin['mood']}\n"
        summary += f"Previous energy level: {last_checkin['energy_level']}\n"
        summary += f"Previous objectives: {last_checkin['objectives']}\n"
        
        if last_checkin.get('stress_factors'):
            summary += f"They mentioned stress about: {last_checkin['stress_factors']}\n"
        
        # Add count of recent check-ins
        summary += f"\nTotal check-ins in the log: {len(log_data)}"
        
        return summary


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
                model="gemini-2.5-flash",
            ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
                voice="en-US-matthew", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        # Using VAD-based turn detection for Windows compatibility
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    assistant = Assistant()
    await session.start(
        agent=assistant,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()
    
    # Send initial greeting when user connects
    await session.say("Hello! Welcome to MindfulMate. I'm here to help you with your daily wellness check-in. How are you feeling today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
