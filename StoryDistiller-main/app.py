from flask import Flask, request
from storyDistiller_main.code.run_storydistiller import *

app = Flask(__name__)

@app.route('/')
def home():
    return "Story distiller app is live."

@app.route("/send_uid", methods=["POST"])
def send_uid():
    if request.method == "POST":
        pass

    return "No HTTP POST method received for send_uid"

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=3000)
