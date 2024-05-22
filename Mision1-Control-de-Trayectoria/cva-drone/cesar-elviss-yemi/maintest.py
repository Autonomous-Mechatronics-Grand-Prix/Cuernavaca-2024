import threading
from testapi import app
import requests
import time

squares_count = 3

def start_flask_app():
    app.run(debug=True, use_reloader=False, port=5003)

server_thread = threading.Thread(target=start_flask_app)
server_thread.start()

""" time.sleep(1) """

""" response = requests.get("http://localhost:5003/squares", params={"squares_count": squares_count})
print(response.json())

response2 = requests.post("http://localhost:5003/add_square")
print(response2.json()) """
