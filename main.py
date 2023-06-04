from flask import Flask, flash, request, redirect, url_for, render_template,send_file
import urllib.request
import os
from werkzeug.utils import secure_filename
import spacy

nlp = spacy.load('en_core_web_sm')
#model_contents = nlp.to_bytes()

app = Flask(__name__)
UPLOAD_FOLDER = 'static/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/summarize', methods=['post'])
def summarize():
    print("Video Summarization started......")
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No video selected for uploading')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "input.mp4"))

        # Perform natural language processing on the video summary
        video_summary = process_video_summary()

        os.system('python demo.py')
        flash('Video successfully uploaded and displayed above')
        return render_template('index1.html', filename="output.mp4", video_summary=video_summary)
        # return render_template('index.html', filename="output.mp4")
  

@app.route('/display/<filename>')
def display_video(filename):
	return redirect(url_for('static', filename='output.mp4'), code=301)


def process_video_summary():
    spacy_path = spacy.__file__
    # Read the contents of the spaCy library file
    with open(spacy_path, 'r', encoding='utf-8') as f:
        spacy_contents = f.read()

    # Write the spaCy library contents to output.txt
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(spacy_contents)
         
    # Read the video summary file
    with open('output.txt', 'r') as f:
        video_summary = f.read()
    # Perform natural language processing on the video summary using spaCy
    doc = nlp(video_summary)
    # Example: Extract named entities from the summary
    named_entities = [ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG']]
    # Return the processed video summary
    return named_entities


if __name__=="__main__":
     app.run(debug=True, port=5000)