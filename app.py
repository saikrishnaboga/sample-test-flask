from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/transcribe')
def index():
    print("Enetered transcribe end point")
    return jsonify({'transcription': "implemenet"})


if __name__ == '__main__':
    app.run(debug=True)
