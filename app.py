from flask import Flask, render_template

app = Flask(__name__)

def transcribe_audio(file_path):
    print("Entered transcribe_audio")
    result = model.transcribe(file_path, fp16=False)
    print(result)
    return result["text"]

@app.route('/transcribe')
def index():
    print("Enetered transcribe end point")
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


if __name__ == '__main__':
    app.run(debug=True)




# @app.route('/transcribe', methods=['POST'])
# def transcribe_endpoint():
#     print("Enetered transcribe end point")
#     if model is None:
#         return jsonify({'error': 'Whisper model is not loaded correctly.'}), 500

#     if 'audio' not in request.files:
#         return jsonify({'error': 'No audio file provided'}), 400

#     file = request.files['audio']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     # Use tempfile to create a temporary directory and file
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(tmpdirname, filename)
#         file.save(file_path)

#         try:
#             transcription = transcribe_audio(file_path)
#             return jsonify({'transcription': transcription})
#         except Exception as e:
#             # Log the exception and return a 500 error with a generic message
#             print(f"Error during transcription: {e}")
#             return jsonify({'error': 'An error occurred during transcription.'}), 500
