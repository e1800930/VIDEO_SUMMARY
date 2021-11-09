# views --contains all of the view for website routing
from flask.templating import render_template_string
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import pafy
from werkzeug.utils import secure_filename
from app._init_ import app, ALLOWED_EXTENSIONS, APP_ROOT,UPLOAD_FOLDER
import vid_sum.evaluate as summarise_module


##ALLOWED_FILE - uppercase and lower case letter
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    	return render_template("public/upload.html")

@app.route('/uploads',  methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
		
		# check if the post request has the file part
	    if 'file' not in request.files:
		    flash('No file part')
		    return redirect(request.url)
	    file = request.files['file']
	    if file.filename == '':
		    flash('No image selected for uploading')
		    return redirect(request.url)
	    else:
		    filename = secure_filename(file.filename)
		    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		    summarise_module.main( UPLOAD_FOLDER + filename ,  )
		    flash('Video successfully uploaded and displayed below .Upload_video filename: ' + filename)
		    return render_template('public/upload.html', filename=filename)


			

#'display -video ' route
@app.route('/uploads/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
	
