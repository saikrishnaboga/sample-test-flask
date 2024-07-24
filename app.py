from flask import Flask, render_template, request, jsonify 
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/transcribe')
def index():
    return jsonify({'transcription': "transcription"})


if __name__ == '__main__':
    app.run(debug=True)
