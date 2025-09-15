import logging
import requests
import os

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)
DOMAIN = "spark_tts"

AUDIO_PATH = "www/spark_tts.wav"
AUDIO_URL = "/local/spark_tts.wav"
SPARK_TTS_API = "http://192.168.50.12:5000/tts"

def call_spark_tts(text: str) -> bool:
    try:
        response = requests.post(SPARK_TTS_API, json={"text": text})
        if response.status_code == 200:
            with open(f"/config/{AUDIO_PATH}", "wb") as f:
                f.write(response.content)
            return True
        else:
            _LOGGER.error("Spark-TTS API error: %s", response.text)
            return False
    except Exception as e:
        _LOGGER.error("Spark-TTS request failed: %s", e)
        return False

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    async def handle_speak(call: ServiceCall):
        message = call.data.get("message")
        entity_id = call.data.get("entity_id")

        if call_spark_tts(message):
            await hass.services.async_call(
                "media_player",
                "play_media",
                {
                    "entity_id": entity_id,
                    "media_content_id": AUDIO_URL,
                    "media_content_type": "music"
                },
                blocking=True
            )
        else:
            _LOGGER.error("Failed to generate audio from Spark-TTS")

    hass.services.async_register(DOMAIN, "speak", handle_speak)
    return True
