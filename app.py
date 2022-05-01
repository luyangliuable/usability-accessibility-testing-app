from flask import Flask

app = Flask(__name__)
@app.route('/')
def home():
    return 'Flask with docker!'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
