import aiohttp
import logging
from homeassistant.components.tts import TextToSpeechEntity
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

class SparkTTSEntity(TextToSpeechEntity, Entity):
    def __init__(self, hass):
        self._name = "Spark TTS"

    @property
    def name(self):
        return self._name

    @property
    def supported_languages(self):
        return ["en-US"]  # Adjust if you support more

    async def async_get_tts_audio(self, message, language, options=None):
        url = "http://192.168.50.32:5000/tts"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={"text": message}) as response:
                    if response.status != 200:
                        _LOGGER.error("Spark TTS server error: %s", response.status)
                        return None, None
                    audio_bytes = await response.read()
                    return "mp3", audio_bytes
        except Exception as e:
            _LOGGER.error("Error calling Spark TTS: %s", e)
            return None, None

