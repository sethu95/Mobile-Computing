import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, jsonify,render_template
import json
from test import *

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("home_screen.html")

@app.route("/about")
def about():
    return render_template("about_screen.html")

@app.route("/")
def index():
	return render_template("home_screen.html")




@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == 'GET': 
        return render_template("upload_screen.html")
    if request.method == 'POST':
        json_data = request.json
        print("reply sent")
        # -> do the function call for python
        json_return = main(json_data)
        return jsonify(json_return)
        #return jsonify(json_data)
        
if __name__ == "__main__":
    app.run(debug=True)