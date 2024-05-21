from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({"message": "Hello, World!"})

def start_flask_app():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    start_flask_app()
