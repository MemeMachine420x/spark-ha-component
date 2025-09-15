from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    text = request.json.get('text')
    output_path = 'output.wav'
    subprocess.run(['python', './spark/cli/inference.py', '--text', text, '--output', output_path])
    return send_file(output_path, mimetype='audio/wav')

app.run(host='0.0.0.0', port=5000)
