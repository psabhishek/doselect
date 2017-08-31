import argparse

from flask import Flask, render_template, redirect, url_for, request,jsonify
import shutil

import binascii
import os, sys, subprocess

import time
import requests
import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))




def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    target = os.path.join(APP_ROOT, 'output/')
    image = os.path.join(APP_ROOT, 'image/')

    if not os.path.isdir(target):
        error =  "Please Sign up!!"
    with open(os.path.join(target, 'txt.json')) as outfile:
        data = json.load(outfile)
    if request.method == 'POST':
        if request.form['key'] not in data.keys():
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('upload'))
    return render_template('login.html', error=error)


@app.route('/create' , methods = ['POST'])
def create_image():
    import pdb;pdb.set_trace()

    data = request.get_json()
    if data["type"] == "POST SINGLE IMAGE":
        error = None
        target = os.path.join(APP_ROOT, 'output/')
        image_file = data['image']
        image_name = image_file.split("/")[-1]
        with open(os.path.join(target, 'txt.json')) as outfile:
            abc = json.load(outfile)
        if data['key'] in abc.keys():
            image = os.path.join(APP_ROOT, 'image/')
            image = os.path.join(image,data['key'])
        shutil.copy2(image_file,os.path.join(image,image_name))


    return "IMAGE UPLOADED"
# use this json contract
# {
# 	"key": "-1552698053",
# 	"image": "/home/abhishek/Pictures/Screenshot from 2017-08-26 02-36-57.png",
# 	"Type": "POST SINGLE IMAGE"
# }

@app.route('/getImage' , methods = ['POST'])
def Get_image():
    import pdb;pdb.set_trace()
    data = request.get_json()
    if data["type"] == "GET IMAGES":
        error = None
        target = os.path.join(APP_ROOT, 'image/')
        target = os.path.join(target,data['key'])
        if not os.path.isdir(target):
            error = "Please Sign up!!"
        image_name = data['image']

        image = os.path.join(APP_ROOT, 'image/')
        image = os.path.join(image,data['key'])
        image = os.path.join(image,image_name)

        open_file(image)


    return "IMAGE UPLOADED"





@app.route("/")
def index():
    return render_template("upload.html")




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    target = os.path.join(APP_ROOT, 'output/')
    image = os.path.join(APP_ROOT, 'image/')
    if not os.path.isdir(image):
        os.mkdir(image)
    if not os.path.isdir(target):
        os.mkdir(target)
    with open(os.path.join(target, 'txt.json')) as outfile:
        data = json.load(outfile)


    if request.method == 'POST':
        crc = str(binascii.crc32(str(request.form['username'])))
        if crc in data.keys():
            error = 'registered'
        else:
            import pdb;pdb.set_trace()
            data[crc] = (request.form['username'], request.form['password'])
            data.update(data)
            image = os.path.join(image,crc)
            if not os.path.isdir(image):
                os.mkdir(image)

            with open(os.path.join(target, 'txt.json'), 'w') as f:
                json.dump(data, f)
                return str(crc)
    return render_template('signup.html', error=error)



@app.route("/upload", methods=['POST'])
def upload():
    import pdb;pdb.set_trace()
    target = os.path.join(APP_ROOT, 'images/')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template("complete.html")

if __name__ == "__main__":
    app.run(port=4555, debug=True)