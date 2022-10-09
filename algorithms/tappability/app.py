'''
api to run algorithm from HTTP
'''
from flask import Flask, request, jsonify
import subprocess


app = Flask(__name__)

# home route
@app.route('/')
def home():
    return "Tappable app is live."

# run algorithm
@app.route("/execute", methods=["POST"])
def execute():
    if request.method != "POST":
        return 'error'

    try:
        image_dir = request.get_json()["image_dir"]
        json_dir = request.get_json()["json_dir"]
        output_dir = request.get_json()["output_dir"]
        threshold = request.get_json()["threshold"]
        
        print('STARTING TAPSHOE %s %s %s %s' % (image_dir, json_dir, output_dir, threshold))
        
        subprocess.run([
            "python3", 
            "/home/pipeline/pipeline.py", 
            "-i", image_dir, 
            "-j", json_dir,
            "-o", output_dir,
            "-t", threshold
            ])
        
        return jsonify( {"result": "SUCCESS"} ), 200
        
    except Exception as e:
        return str(e)
    
if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=3007)