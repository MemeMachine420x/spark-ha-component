from flask import Flask, request, Response
from gradio_client import Client, handle_file
import subprocess
import os
import traceback

app = Flask(__name__)
voicePath = "/home/rangernet/spark-ha-component/voices/lisa.wav"

@app.route('/tts', methods=['POST'])
def tts():
    try:
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
        ffmpeg = '/usr/bin/ffmpeg'
        proc = subprocess.run(
            [ffmpeg, '-hide_banner', '-loglevel', 'error', '-i', result, '-f', 'mp3', 'pipe:1'],
            capture_output=True
        )
        if proc.returncode != 0:
            print("ffmpeg error:", proc.stderr.decode())
            return Response("ffmpeg failed", status=500)
        return Response(proc.stdout, mimetype='audio/mpeg')
    except Exception as e:
        traceback.print_exc()
        return Response(str(e), status=500)

@app.route('/voice', methods=['POST'])
def voice():
    voicePath = request.json.get('voice')
    return ("OK")
app.run(host='0.0.0.0', port=5000)
