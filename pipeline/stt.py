from livekit.plugins import deepgram
from config import DEEPGRAM_API_KEY


def get_stt():

    return deepgram.STT(
        api_key=DEEPGRAM_API_KEY,
        model="nova",
    )
