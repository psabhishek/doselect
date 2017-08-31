import argparse

from flask import Flask, render_template, redirect, url_for, request
import binascii
import os
import time

import requests

import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))



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
        crc = str(binascii.crc32(str(request.form['username'])+ str(request.form['password'])))
        if crc in data.keys() :
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



def f(n):
   if n<=0:
      return 0
   return n + f(int(n/2))
x = f(4)
print x


def a (b, c, d):
    pass


x =1
b =1
c =1
a(x,b,c)