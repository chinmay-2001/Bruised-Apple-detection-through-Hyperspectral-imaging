# Integrating flask with HTML

import sklearn
import glob
import copy
import shutil
import os,shutil
import sys
import subprocess
import torch
from IPython.display import Image
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory
from werkzeug.utils import secure_filename

# Libraries required for Models
from MODELS import *
import numpy as np
import pandas as pd
from PIL import Image
from osgeo import gdal, gdalconst
from osgeo.gdalconst import * 


filename_store=""
# file_wholepath=""
# Initialize

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# upload and save and display file
ALLOWED_EXTENSIONS = set(['bip'])

# file funcitons

# def find_result_file_path(find_path_for_this_file):
    
#     dir=r"C:\Users\Dell\Desktop\flasknew\yolov5\runs\detect"
#     for root, dirs, files in os.walk(dir):
#         for name in files:
#             if name==fc:
#                 filename_store=name
#                 file_wholepath=str(os.path.join(root, name))
#                 return str(os.path.join(root, name))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def YOLO_prediction(filename):
    
    # cleaning detect folder, removing all directories/files/subdirectories
    dir = r"C:\Users\admin\Desktop\flasknew-Copy\yolov5\runs\detect"
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
    
    # uploaded HSI converted to JPG
    hsi_to_image(r"C:\Users\admin\Desktop\flasknew-Copy\static\uploads"+f"\\{filename}")
    
    # now pass the jpg in test_image_path
    jpgFileName=filename_store+".jpg"
        
    detect_py_path=r"C:\Users\admin\Desktop\flasknew-Copy\yolov5\detect.py"
    test_image_path=r"C:\Users\admin\Desktop\flasknew-Copy\static\uploads"+f"\\{jpgFileName}"
    best_pt_path=r"C:\Users\admin\Desktop\flasknew-Copy\yolov5\runs\train\exp\weights\best.pt"
    
    print("*******__________********** : : test_image_path = ",test_image_path)
    
    
    cmd="python "+detect_py_path+" --source "+test_image_path+" --weights "+best_pt_path
    file=open(r"C:\Users\admin\Desktop\flasknew-Copy\run.bat",'w')
    file.write(cmd)
    file.close()
    subprocess.run([r"C:\Users\admin\Desktop\flasknew-Copy\run.bat",""])
    file=open(r"C:\Users\admin\Desktop\flasknew-Copy\run.bat",'w')
    file.truncate()
    file.close()
    return

 
@app.route('/')
def upload_form():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_image():
    global filename_store
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # SAVE selected file by user
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        flash(f'Image {file.filename} successfully uploaded')
        
        # Save name of FILE in use in VARIABLE
        nameSplit=filename.split(".")
        filename_store=nameSplit[0]
        
        # writing to file, in order to use in MODELS.py
        fi=open(r"C:\Users\admin\Desktop\flasknew-Copy\target_file_name_store.txt",'w')
        fi.write(filename_store)
        fi.close()
        
        # Run YOLOv5 on .jpg
        YOLO_prediction(filename_store+".bip")
        
        # Render html page
        return render_template('home.html', filename=filename)
    else:
        flash('Only .bip format is supported!')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route("/getimage")
def get_img():
    
    f=open(r"C:\Users\admin\Desktop\flasknew-Copy\target_file_name_store.txt",'r')
    filename_store=f.read()
    f.close()
    
    # Result Filename is same, but in folder: /runs/detect/exp/name.jpg
    
    print("fileSTORE IS : : : ",filename_store)
    img_filename=filename_store+".jpg"
    modelResultImg=r"C:\Users\admin\Desktop\flasknew-Copy\yolov5\runs\train\exp"+"\\{img_filename}"
    
    # Copy the Image to static folder for easy display in Modal
    src_dir=modelResultImg
    dst_dir = r"C:\Users\admin\Desktop\flasknew-Copy\static"
    for jpgfile in glob.iglob(os.path.join(src_dir, img_filename)):
        shutil.copy(jpgfile, dst_dir)
    
    complete()
    
    return img_filename

# running the app
if __name__=='__main__':
    app.run(debug=True)
