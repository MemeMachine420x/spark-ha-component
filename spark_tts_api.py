from flask import Flask, request, send_file
from gradio_client import Client, handle_file
import subprocess
import os

app = Flask(__name__)
voicePath = "/home/rangernet/spark-ha-component/voices/lisa.wav"

@app.route('/tts', methods=['POST'])
def tts():
    requestText = request.json.get('text')
    print(requestText)
    client = Client("http://192.168.100.74:7860/")
    result = client.predict(
		text=requestText,
		prompt_text="",
		prompt_wav_upload=handle_file(voicePath),
		prompt_wav_record=handle_file(voicePath),
		api_name="/voice_clone"
)
    print(result)
    return send_file(result, mimetype='audio/wav')

@app.route('/voice', methods=['POST'])
def voice():
    voicePath = request.json.get('voice')
    return ("OK")
app.run(host='0.0.0.0', port=5000)
