from flask import Flask, jsonify
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)

last_squares_count = 0

@app.route('/squares', methods=['GET'])
def squares():
    global last_squares_count
    squares_count = request.args.get('squares_count', default=None, type=int)
    if squares_count is None:
        return jsonify({"message": last_squares_count})
    last_squares_count = squares_count
    return jsonify({"message": squares_count})

@app.route('/add_square', methods=['POST'])
def add_square():
    global last_squares_count
    last_squares_count += 1
    return jsonify({"message": "Square added"})

def start_flask_app():
    app.run(debug=True, use_reloader=False, port=5003)

if __name__ == "__main__":
    start_flask_app()
