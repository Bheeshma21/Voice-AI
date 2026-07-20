from livekit.plugins import cartesia
from config import CARTESIA_API_KEY


def get_tts():

    if not CARTESIA_API_KEY:
        return None

    return cartesia.TTS(
        api_key=CARTESIA_API_KEY,
        model="sonic-2"
    )   