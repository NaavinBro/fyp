from flask import Flask, request, redirect, url_for, render_template
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AITDS', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return 'No file part'

    file = request.files['pdf_file']

    if file.filename == '':
        return 'No selected file'

    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Process the PDF and extract text
        extracted_text = extract_text_from_pdf(filepath)
        
        return f'<h2>Extracted Text:</h2><p>{extracted_text}</p>'

    return 'Invalid file format. Please upload a PDF.'

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)
