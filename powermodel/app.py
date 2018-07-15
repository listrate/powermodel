from functools import wraps
from flask import Flask, jsonify, request, session, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
import os
import pandas as pd
import numpy as np
import calendar
import datetime
import math
from powermodel import validate, parse, generateHeatmapData, generateweekdayweekendData, generatedaybreakdown, generatetimeofdaybreakdown, generatesummarydata
from util import createMD5sum

app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")

app.config['SECRET_KEY'] = os.urandom(24)

CSV_UPLOAD_FOLDER = os.path.join(os.getcwd(),'data/csv')
H5_FOLDER = os.path.join(os.getcwd(),'data/h5')
ALLOWED_EXTENSIONS = set(['csv'])

app.config['UPLOAD_FOLDER'] = CSV_UPLOAD_FOLDER

ERROR_MESSAGE = {"status": 9999}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def upload_csv():
    file_saved = None
    csv_file_path = None
    session_id = None
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            print('got it', file.filename)
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(CSV_UPLOAD_FOLDER,filename))
            csv_file_path = os.path.join(CSV_UPLOAD_FOLDER,filename)
            file_saved = True
            session_id = createMD5sum(csv_file_path)
            print(session_id)
            session['id'] = session_id
    if file_saved:
        if (validate(csv_file_path,'powercor')):
            parse(csv_file_path,session_id, 'powercor')
            return jsonify({'status': 1000, 'session_id': session_id})
        else:
            return jsonify(ERROR_MESSAGE)
    else:
        return jsonify(ERROR_MESSAGE)

@app.route('/')
def hello_world():
    return render_template("index.html")

def sessionid_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' in session:
            if os.path.exists(os.path.join(H5_FOLDER,session['id']+".h5")):
                return f(*args, **kwargs)
            else:
                return jsonify(ERROR_MESSAGE)
        else:
            return jsonify(ERROR_MESSAGE)
    return decorated_function

@app.route('/api/summary')
@sessionid_required
def summarydataendpoint():
    return jsonify(generatesummarydata(session['id']))

@app.route('/api/heatmap')
@sessionid_required
def heatmapendpoint():
    return jsonify(generateHeatmapData(session['id']))

@app.route('/api/weekdayweekend')
@sessionid_required
def weekdayweekendendpoint():
    return jsonify(generateweekdayweekendData(session['id']))

@app.route('/api/daybreakdown')
@sessionid_required
def daybreakdownedpoint():
    return jsonify(generatedaybreakdown(session['id']))

@app.route('/api/timeofdaybreakdown')
@sessionid_required
def timeofdaybreakdown():
    return jsonify(generatetimeofdaybreakdown(session['id']))

if __name__ == '__main__':
    app.run()