from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import io
import logging
from werkzeug.utils import secure_filename
import tempfile
import whisper

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Check if running on AWS Lambda
if 'LAMBDA_TASK_ROOT' in os.environ:
    os.environ['PATH'] = os.environ['PATH'] + ':/opt/bin:/var/task/ffmpeg-layer/bin'
    
# Set up Azure OpenAI API credentials
openai.api_type = "azure"
openai.api_base = "https://nw-tech-wu.openai.azure.com/"
openai.api_version = "2024-02-01"
openai.api_key = "fce9b34907b848a6902e5c37ddfc8512"

# Dummy model and transcribe_audio function for demonstration purposes
# model = "dummy_model"  # Replace this with actual model loading logic


# Initialize Whisper model
try:
    model = whisper.load_model("base")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    model = None

@app.route('/home')
def getHome():
    return 'Hello World'

def transcribe_audio(file_path):
    print("entered audio")
    result = model.transcribe(file_path, fp16=False)
    print(result)
    return result["text"]

@app.route('/transcribe', methods=['POST'])
def transcribe_endpoint():
    print("Entered into transcribe")
    if model is None:
        return jsonify({'error': 'Whisper model is not loaded correctly.'}), 500

    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Use tempfile to create a temporary directory and file
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = secure_filename(file.filename)
        file_path = os.path.join(tmpdirname, filename)
        file.save(file_path)

        try:
            transcription = transcribe_audio(file_path)
            return jsonify({'transcription': transcription})
        except Exception as e:
            # Log the exception and return a 500 error with a generic message
            print(f"Error during transcription: {e}")
            return jsonify({'error': 'An error occurred during transcription.'}), 500


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    transcript = data['transcript']
    question = data['question']

    # Combine transcript and question into a single prompt
    prompt = f"Transcript:\n{transcript}\n\nQuestion: {question}\nAnswer:"

    # Prepare messages for Azure OpenAI
    messages = [{"role": "system", "content": prompt}]

    # Query Azure OpenAI GPT-4
    response = openai.ChatCompletion.create(
        deployment_id="gpt-4o",  # Replace with your actual deployment ID
        messages=messages,
    )

    answer = response.choices[0].message['content'].strip()
    return jsonify({'answer': answer})

    
if __name__ == '__main__':
    app.run(debug=True)


# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/saikrishnaboga/backend-voice-ai.git
# git push -u origin main
