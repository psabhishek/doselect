import argparse

from flask import Flask, render_template, redirect, url_for, request,jsonify,send_from_directory
import shutil

import binascii
import os, sys, subprocess

import time
import requests
import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_ROOT = os.path.join(APP_ROOT,'static')


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
    image = os.path.join(IMG_ROOT, 'image/')

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


@app.route('/create',methods = ['POST','GET'])
def create_image():

    data = request.get_json()
    if request.method == "POST":
        error = None
        target = os.path.join(APP_ROOT, 'output/')
        key = request.form['key']
        img_path = request.form['file_name']
        img_path = img_path.split("/")[:-1]
        with open(os.path.join(target, 'txt.json')) as outfile:
            abc = json.load(outfile)
        if request.form['file_name'] in abc.keys():
            image = os.path.join(IMG_ROOT, 'image/')
            image = os.path.join(image, key)
        image_file = data['image']
        image_name = image_file.split("/")[-1]

        if data['key'] in abc.keys():
            image = os.path.join(IMG_ROOT, 'image/')
            image = os.path.join(image,data['key'])
        #upload.save(image)
        shutil.copy2(image_file,os.path.join(image,image_name))


        return "IMAGE UPLOADED"
    return render_template("push.html")
# use this json contract
# {
# 	"key": "-1552698053",
# 	"image": "/home/abhishek/Pictures/1.png",
# 	"Type": "POST SINGLE IMAGE"
# }


@app.route('/getImage' , methods = ['POST',"GET"])
def Get_image():
    data = request.get_json()
    if data["type"] == "GET IMAGES":
        error = None
        target = os.path.join(IMG_ROOT, 'image/')
        target = os.path.join(target,data['key'])
        if not os.path.isdir(target):
            error = "Please Sign up!!"
        image_name = data['image']

        image = os.path.join(IMG_ROOT, 'image/')
        image_path = os.path.join(image,data['key'])
        image_name= os.path.join(image_path,data['image'])
    return render_template("galary.html")



@app.route("/")
def index():

    return render_template("upload.html")




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    target = os.path.join(APP_ROOT, 'output/')
    image = os.path.join(APP_ROOT, 'images/')
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
            data[crc] = (request.form['username'], request.form['password'])
            data.update(data)
            image = os.path.join(image,crc)
            if not os.path.isdir(image):
                os.mkdir(image)

            with open(os.path.join(target, 'txt.json'), 'w') as f:
                json.dump(data, f)
                return str(crc)
    return render_template('signup.html', error=error)

@app.route('/delete',methods = ['POST','GET'])
def delete():
    error = None
    if request.method == 'POST':

        data = request.get_json()

        image = os.path.join(APP_ROOT, 'images/')
        data = request.form['key']
        path = os.path.join(image,data)
        img = request.form['file_name']
        img_path = os.path.join(path,img)
        if os.path.join(path, request.form['file_name']):
            os.remove(os.path.join(path, request.form['file_name']))
            return "IMAGE DELETED"
        else:
            error = 'NO SUCH FILE FOUND'


    return render_template('delete.html', error=error)





@app.route("/upload", methods=['POST'])
def upload():
    key_dir = os.path.join(APP_ROOT, 'output/')
    target = os.path.join(APP_ROOT, 'images/')
    key = request.form['key']
    target = os.path.join(target, key)
    with open(os.path.join(key_dir, 'txt.json')) as outfile:
        abc = json.load(outfile)
    if key in abc.keys():
        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
    else:
        return "WRONG KEY"
    # return send_from_directory(target,filename, as_attachment = True)
    return "UPLOADED"


@app.route('/gallery', methods=['POST',"GET"])
def get_gallery():
    if request.method == 'POST':
        key_dir = os.path.join(APP_ROOT, 'output/')
        target = os.path.join(APP_ROOT, 'images/')
        key = request.form['key']
        target = os.path.join(target, key)
        with open(os.path.join(key_dir, 'txt.json')) as outfile:
            abc = json.load(outfile)
        if key in abc.keys():
            image_names = os.listdir(target)
            print(image_names)
        return render_template("gallery.html", image_names=image_names, target = key)
    return render_template("KEY.html")

@app.route('/simgleImg', methods=['POST',"GET"])
def get_img():

    if request.method == 'POST':


        key_dir = os.path.join(APP_ROOT, 'output/')
        target = os.path.join(APP_ROOT, 'images/')
        key = request.form['key']
        target = os.path.join(target, key)
        with open(os.path.join(key_dir, 'txt.json')) as outfile:
            abc = json.load(outfile)
        if key in abc.keys():
            image_names = request.form['name']
            print(image_names)
        return render_template("complete.html", image_names=image_names, target=key)
    return render_template("push.html")



@app.route('/upload/<key>/<filename>')
def send_single(filename,key):
    route =  os.path.join(APP_ROOT,"images")
    route = os.path.join(route,key)
    return send_from_directory(route, filename)


@app.route('/upload/<key>/<filename>')
def send_image(filename,key):
    route =  os.path.join(APP_ROOT,"images")
    route = os.path.join(route,key)
    return send_from_directory(route, filename)


if __name__ == "__main__":
    app.run(port=4555, debug=True)

