from flask import Flask, render_template

app = Flask(__name__)

@app.route('/transcribe')
def index():
    print("Enetered transcribe end point")
    return jsonify({'transcription': "implemenet"})


if __name__ == '__main__':
    app.run(debug=True)
