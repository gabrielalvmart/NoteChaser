import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
from app import app
from app.models.track import Track
from app.models.track_singleton import TrackSingleton

UPLOAD_FOLDER = 'app/files'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/selectTrack', methods=['GET'])
def select_track():
    track_filename = request.args.get('track')
    if track_filename:
        track = Track(name=track_filename, audio_path=os.path.join(app.config['UPLOAD_FOLDER'], track_filename))
        TrackSingleton().set_track(track)
        return jsonify({'track': track_filename})
    return jsonify({'error': 'No track selected'})
