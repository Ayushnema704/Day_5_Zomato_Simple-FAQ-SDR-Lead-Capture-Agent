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

# Path to the tutor content JSON file
TUTOR_CONTENT_PATH = "tutor_content.json"
LEARNING_LOG_PATH = "learning_log.json"


def load_tutor_content():
    """Load the tutor content from JSON file."""
    if os.path.exists(TUTOR_CONTENT_PATH):
        try:
            with open(TUTOR_CONTENT_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Tutor content file is corrupted")
            return []
    return []


def load_learning_log():
    """Load the learning log from JSON file."""
    if os.path.exists(LEARNING_LOG_PATH):
        try:
            with open(LEARNING_LOG_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Learning log file is corrupted, starting fresh")
            return []
    return []


def save_learning_log(log_data):
    """Save the learning log to JSON file."""
    try:
        with open(LEARNING_LOG_PATH, "w") as f:
            json.dump(log_data, f, indent=2)
        logger.info("Learning log saved successfully")
    except Exception as e:
        logger.error(f"Error saving learning log: {e}")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are an Active Recall Coach - a friendly and encouraging tutor that uses the "teach-the-tutor" method to help users master programming concepts through active learning.

You have access to programming concepts (variables, loops, functions, conditionals) through the get_concept tool.

Your role is to support THREE learning modes that the user can switch between at any time:

**1. LEARN MODE** - You are the teacher (Use voice: Matthew, Conversation style)
- Explain concepts clearly and conversationally using the concept summary
- Break down complex ideas into simple terms
- Give real-world examples
- Check for understanding: "Does that make sense?" or "Would you like me to explain anything further?"
- Users can ask you to explain any concept from the content

**2. QUIZ MODE** - You test the learner (Use voice: Alicia, Conversation style)
- Ask questions about concepts using the sample_question from the content
- Wait for their answer
- Provide encouraging feedback whether right or wrong
- If wrong, gently correct and explain the right answer
- Keep it conversational and supportive, not intimidating

**3. TEACH BACK MODE** - The learner teaches you (Use voice: Ken, Conversation style)
- Ask the user to explain a concept back to you
- Listen actively to their explanation
- Give qualitative feedback: "That's a great explanation!" or "You've got the main idea, but let me clarify one point..."
- Encourage them even if they struggle
- Point out what they got right before mentioning what they missed

**Conversation Flow:**
1. Greet the user warmly and ask which learning mode they'd like to start with
2. Once they choose a mode (learn, quiz, or teach_back), use get_concept to load a programming concept
3. Execute that mode's behavior as described above
4. After each interaction, ask if they want to continue with this mode, switch modes, or try a different concept
5. Users can say things like "switch to quiz mode" or "let me try teaching it back" at any time
6. Log their progress using save_learning_session when they complete activities

**Important Guidelines:**
- Be encouraging and positive - learning should feel safe and fun
- Keep explanations concise and voice-friendly (no long walls of text)
- Use natural, conversational language
- Avoid complex formatting or special characters
- Adapt your teaching style based on their responses
- Celebrate small wins and progress
- Make it clear they can switch modes anytime

Remember: The best way to learn is to teach. Help them master concepts through active recall!""",
        )

    @function_tool
    async def get_concept(
        self,
        context: RunContext,
        concept_id: str,
    ):
        """Get a programming concept by its ID to teach, quiz, or have the user teach back.
        
        Args:
            concept_id: The ID of the concept (e.g., "variables", "loops", "functions", "conditionals")
        """
        logger.info(f"Loading concept: {concept_id}")
        
        # Load tutor content
        content = load_tutor_content()
        
        # Find the concept
        concept = next((c for c in content if c["id"] == concept_id), None)
        
        if not concept:
            return f"Concept '{concept_id}' not found. Available concepts: variables, loops, functions, conditionals"
        
        return f"Concept: {concept['title']}\n\nSummary: {concept['summary']}\n\nSample Question: {concept['sample_question']}"

    @function_tool
    async def save_learning_session(
        self,
        context: RunContext,
        mode: str,
        concept_id: str,
        notes: Optional[str] = None,
    ):
        """Save a learning session to track the user's progress.
        
        Call this when the user completes an activity in any mode (learn, quiz, or teach_back).
        
        Args:
            mode: The learning mode used (learn, quiz, or teach_back)
            concept_id: The concept ID that was practiced
            notes: Optional notes about the session (e.g., "struggled with loop syntax" or "explained variables clearly")
        """
        logger.info(f"Saving learning session - Mode: {mode}, Concept: {concept_id}")
        
        # Load existing log
        log_data = load_learning_log()
        
        # Create new entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "mode": mode,
            "concept_id": concept_id,
            "notes": notes,
        }
        
        # Add to log
        log_data.append(entry)
        
        # Save to file
        save_learning_log(log_data)
        
        return f"Learning session saved! You practiced '{concept_id}' in {mode} mode."


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
    await session.say("Hello! Welcome to your Active Recall Coach. I'm here to help you master programming concepts through three learning modes: Learn mode where I teach you, Quiz mode where I test your knowledge, and Teach Back mode where you explain concepts to me. Which mode would you like to start with?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
