import os
import sys
import glob
import json
from flask import Flask, render_template, request, redirect, url_for, \
    jsonify, send_file, abort
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

colors = [
    '#000000',
    '#B0171F',
    '#DA70D6',
    '#8A2BE2',
    '#0000FF',
    '#4876FF',
    '#CAE1FF',
    '#6E7B8B',
    '#00C78C',
    '#00FA9A',
    '#00FF7F',
    '#00C957',
    '#3D9140',
    '#32CD32',
    '#00EE00',
    '#008B00',
    '#76EE00',
    '#CAFF70',
    '#FFFF00',
    '#CDCD00',
    '#FFF68F',
    '#FFFACD',
    '#FFEC8B',
    '#FFD700',
    '#F5DEB3',
    '#FFE4B5',
    '#EECFA1',
    '#FF9912',
    '#8E388E',
    '#7171C6',
    '#7D9EC0',
    '#388E8E',
    '#71C671',
    '#8E8E38',
    '#C5C1AA',
    '#C67171',
    '#555555',
    '#848484',
    '#F4F4F4',
    '#EE0000',
    '#FF4040',
    '#EE6363',
    '#FFC1C1',
    '#FF7256',
    '#FF4500',
    '#F4A460',
    '#FF8000',
    '#FFD700',
    '#8B864E',
    '#9ACD32',
    '#66CD00',
    '#BDFCC9',
    '#76EEC6',
    '#40E0D0',
    '#E0EEEE',
    '#98F5FF',
    '#33A1C9',
    '#F0F8FF',
    '#4682B4',
    '#C6E2FF',
    '#9B30FF',
    '#EE82EE',
    '#FFC0CB',
    '#7CFC00',
]
colors = [
    '000000',
    'd1431d',
    'e8914c',
    'ff0000',
    '00ff00',
    '0000ff',
    'ffff00',
    '00ffff',
    'ff00ff',
]
colors = ['#' + color for color in colors]


@app.route('/', methods=['GET', 'POST'])
def paintapp():
    if request.method == 'GET':
        context = {'colors':colors, 'per_row':3}
        return render_template("paint.html", **context)
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
        outname = TMPDIR + f'B_{name}.png'
        outtouch = TMPDIR + f'B_{name}'
        img.save(inname)
        while not os.path.exists(outtouch):
            time.sleep(.01)
        # return send_file(outname, mimetype='image/jpeg')
        # time.sleep(1)
        # Image.open(outname).show()
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

frags = glob.glob('fragments/*.jpg')
split_id = lambda f: int(os.path.splitext(os.path.split(f)[-1])[0])
id_dict = {split_id(f): f for f in frags}
ind_dict = {n: f for n, f in enumerate(frags)}

presets = glob.glob('presets/*.jpg')
presets = {split_id(f): f for f in presets}

@app.route('/fragment/<int:n>')
def frag_ind(n):
    if n > len(ind_dict) or n < 1:
        return abort(404)
    return send_file(ind_dict[n-1], mimetype='image/jpeg')

@app.route('/metid/<int:img_id>')
def frag_id(img_id):
    if img_id not in id_dict:
        return abort(404)
    return send_file(ind_dict[img_id], mimetype='image/jpeg')

@app.route('/preset/<int:img_id>')
def preset_id(img_id):
    if img_id not in presets:
        return abort(404)
    return send_file(presets[img_id], mimetype='image/jpeg')


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
    app.run(host='0.0.0.0', port=port, debug=True)
