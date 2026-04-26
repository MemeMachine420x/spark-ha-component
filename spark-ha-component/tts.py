import aiohttp
import logging
from homeassistant.components.tts import Provider

_LOGGER = logging.getLogger(__name__)


def get_engine(hass, config, discovery_info=None):
    return SparkTTSProvider()


class SparkTTSProvider(Provider):
    @property
    def name(self):
        return "Spark TTS"

    @property
    def supported_languages(self):
        return ["en-US"]

    @property
    def default_language(self):
        return "en-US"

    async def async_get_tts_audio(self, message, language, options=None):
        url = "http://192.168.100.74:5000/tts"
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
