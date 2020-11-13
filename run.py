import os
import sys
import json
from flask import Flask, render_template, request, redirect, url_for, \
    jsonify, send_file
# import psycopg2

from PIL import Image
from io import BytesIO
from base64 import b64encode, b64decode

import time
import random
from tempfile import gettempdir
TMPDIR = gettempdir() + '/vasegen/'

if not os.path.exists(TMPDIR):
    os.mkdir(TMPDIR)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def paintapp():
    if request.method == 'GET':
        return render_template("paint.html")
    if request.method == 'POST':
        canvas_image = request.form['drawn_image']
        try:
            imgbytes = BytesIO(b64decode(canvas_image.split('base64,')[1]))
            img = Image.open(imgbytes)
            # assert False
        except:
            return jsonify({'status': 'failure'})
        # canvas_image = request.form['save_image']
        # filename = request.form['save_fname']
        # data = request.form['save_cdata']
        # conn = psycopg2.connect(database="paintmyown", user = "nidhin")
        # cur = conn.cursor()
        # cur.execute("INSERT INTO files (name, data, canvas_image) VALUES (%s, %s, %s)", [filename, data, canvas_image])
        # conn.commit()
        # conn.close()
        # Image.open('vase.jpg')
        # return send_file('vase.jpg', mimetype='image/jpeg')

        name = '%020x' % random.randrange(16**20)
        inname = TMPDIR + f'A_{name}.png'
        outname = TMPDIR + f'A_{name}.png'
        img.save(inname)
        while not os.path.exists(outname):
            time.sleep(.01)
        # return send_file(outname, mimetype='image/jpeg')
        return b64encode(open(outname, "rb").read())
        # return jsonify({'status': 'success', 'vase': 'asdf'})

@app.route('/failed', methods=['GET'])
def failed():
    return 'Failed to convert image to vase'

@app.route('/vase')
def vase():
    return send_file('vase.jpg', mimetype='image/jpeg')

@app.route('/vase_outline')
def vase_outline():
    return send_file('vase_outline.jpg', mimetype='image/jpeg')

# @app.route('/save', methods=['GET', 'POST'])
# def save():
#     conn = psycopg2.connect(database="paintmyown", user="nidhin")
#     cur = conn.cursor()
#     cur.execute("SELECT id, name, data, canvas_image from files")
#     files = cur.fetchall()
#     conn.close()
#     return render_template("save.html", files = files )
    
# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'GET':
#         return render_template("search.html")
#     if request.method == 'POST':
#         filename = request.form['fname']
#         conn = psycopg2.connect(database="paintmyown", user="nidhin")
#         cur = conn.cursor()
#         cur.execute("select id, name, data, canvas_image from files")
#         files = cur.fetchall()
#         conn.close()
#         return render_template("search.html", files=files, filename=filename)
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
