from urllib import response
from flask import Flask, jsonify, request
from flask import render_template
from flask import send_from_directory
import os
from flask_cors import CORS, cross_origin
from models import *
from datetime import datetime
from PIL import Image
app = Flask(__name__)
cors = CORS(app)

UPLOAD_FOLDER = "./static/images"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
__matcher = Matcher()


def convert_image(file):
    image = Image.open(file)
    image_rgb = image.convert('RGB')
    image_rgb.save(file)


@app.route('/')
@cross_origin()
def hello_world():
    return render_template('index.html')


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


def uploadFile(file1):
    print(file1.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], file1.filename)
    file1.save(path)
    convert_image(path)
    return file1.filename


@app.route('/api/match', methods=['POST'])
@cross_origin()
def matchImage():
    image = request.files["image"]
    filename = uploadFile(image)
    resp = __matcher.findMatch(filename)
    return jsonify(resp)
