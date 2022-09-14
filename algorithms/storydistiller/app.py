'''
api to run algorithm from HTTP
'''
from flask import Flask, request, jsonify
import subprocess


app = Flask(__name__)

# home route
@app.route('/')
def home():
    return "Story distiller app is live."

# run algorithm
@app.route("/execute", methods=["POST"])
def execute():
    if request.method != "POST":
        return 'error'

    try:
        apk_path = request.get_json()["apk_path"]
        output_dir = request.get_json()["output_dir"]
        emulator = request.get_json()["emulator"]
        
        print('STARTING STORYDISTILLER %s %s %s' % (emulator, apk_path, output_dir))
        
        subprocess.run(["python", "/home/StoryDistiller-main/code/run_storydistiller.py", emulator, apk_path, output_dir])
        
        return jsonify( {"result": "SUCCESS"} ), 200
        
    except Exception as e:
        return str(e)
    
if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=3002)