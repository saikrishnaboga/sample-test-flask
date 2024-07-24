from flask import Flask, render_template, request, jsonify 
app = Flask(__name__)

@app.route('/transcribe')
def index():
    return jsonify({'transcription': "transcription"})
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
