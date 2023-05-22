from flask import Flask, render_template, request, jsonify, redirect, Response, send_file
import pandas as pd 
import os
import time
import shutil
import datetime
from gcaa import GCAA

def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


app = Flask(__name__)

@app.route('/')
def main_page():
    delete_files_in_directory('app/Daily_Traffic/')
    delete_files_in_directory('app/NO DML/')
    delete_files_in_directory('app/output/')

    if (os.path.exists('output_files.zip')):
        os.remove('output_files.zip')

    return render_template('Upload2.html')

@app.route('/loading')
def loading_page():
    return render_template('processing2.html')

@app.route('/upload')
def upload():
    return render_template('Upload2.html')

@app.route('/processing')
def processing_page():
    GCAA()
    return render_template('download2.html')

@app.route('/reroute')
def reroute():
    return redirect('/')

# Enables admin to download all currently uploaded files
@app.route('/download_output', methods = ['GET'])
def output_download():
    if request.method == 'GET':
        shutil.make_archive('output_files', format='zip', root_dir='app/output')
        files_path = '../output_files.zip'
        return send_file(files_path, as_attachment=True)

@app.route('/DML_file', methods = [ "POST"])
def DML_file():
    if request.method == 'POST':
        f = request.files['file']
        file_path = "app/Daily_Traffic/"+f.filename
        f.save(file_path)
    return 'success'

@app.route('/NON_DML_file', methods = [ "POST"])
def NON_DML_file():
    if request.method == 'POST':
        f = request.files['file']
        file_path = "app/NO DML/"+f.filename
        f.save(file_path)
    return 'success'

@app.route('/download')
def download_page():
    return render_template('download2.html')

# @app.route('/process')
# def automation_process():
#     # Add the python function to be used
#     GCAA()
#     return 'sucess'

# Enables admin to delete the uploaded files from the system
@app.route('/download_NONDML/<filename>', methods = ['GET'])
def fileNON_download(filename):
    if request.method == 'GET':
        file_path = 'NO DML/' + str(filename) #Here can we unify the name of the
        return send_file(file_path, as_attachment=True)

# Enables admin to delete the uploaded files from the system
@app.route('/download_DML/<filename>', methods = ['GET'])
def file_download(filename):
    if request.method == 'GET':
        file_path = 'Daily_Traffic/' + str(filename)
        return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)