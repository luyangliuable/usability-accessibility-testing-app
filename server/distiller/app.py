from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Story distiller is online"

@app.route('/check_working')
def check_working():
    return "Story distiller is online"

if __name__ == "__main__":
    app.run(host='localhost', port=3002, debug=True)
