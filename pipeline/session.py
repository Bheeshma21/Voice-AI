from livekit.agents import AgentSession

from pipeline.stt import get_stt
from pipeline.tts import get_tts
from pipeline.vad import get_vad

from livekit.plugins import groq
from config import GROQ_API_KEY


def create_session():

    session_args = {

        "stt": get_stt(),

        "llm": groq.LLM(
            api_key=GROQ_API_KEY,
            model="llama-3.1-8b-instant"
        ),

        "vad": get_vad(),

        "turn_detection": "vad",

        "min_endpointing_delay": 1.5,

        "max_endpointing_delay": 5.0,

        "allow_interruptions": True,

        "preemptive_generation": False,
    }


    tts = get_tts()

    if tts:
        session_args["tts"] = tts


    return AgentSession(**session_args)