from livekit.plugins import silero


def get_vad():

    return silero.VAD.load() 
