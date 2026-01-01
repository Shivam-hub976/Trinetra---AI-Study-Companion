from ocr_utils import extract_text_from_image, extract_text_from_pdf_images
from flask import Flask, request, jsonify, send_from_directory
import PyPDF2
import docx  
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from summarizer import summarize_text
from study_planner import generate_study_plan


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')


def extract_uploaded_text(file_storage):
    filename = file_storage.filename.lower()
    if filename.endswith('.pdf'):
        # Try text extraction first
        try:
            pdf_reader = PyPDF2.PdfReader(file_storage)
            text = ''
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            if text.strip():
                return text
        except Exception:
            pass
        # If no text, try OCR
        file_storage.seek(0)
        ocr_text = extract_text_from_pdf_images(file_storage)
        return ocr_text
    elif filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        return extract_text_from_image(file_storage)
    elif filename.endswith('.docx'):
        try:
            doc = docx.Document(file_storage)
            text = '\n'.join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            return ''
    else:
        try:
            return file_storage.read().decode('utf-8', errors='replace')
        except Exception as e:
            return ''

@app.route('/summarize', methods=['POST'])
def summarize():
    print('Received /summarize request')
    if 'file' not in request.files:
        print('[ERROR] No file uploaded')
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    safe_filename = ''.join([c if ord(c) < 128 else '?' for c in file.filename])
    print(f'[DEBUG] File received: {safe_filename}')
    text = extract_uploaded_text(file)
    print(f'[DEBUG] Extracted text length: {len(text)}')
    try:
        safe_debug = ''.join([c if ord(c) < 128 else '?' for c in text[:100]])
        print('[DEBUG] Extracted text (first 100 chars):', safe_debug)
    except Exception as e:
        safe_err = ''.join([c if ord(c) < 128 else '?' for c in str(e)])
        print('[DEBUG] Could not print extracted text:', safe_err)
    if not text.strip():
        print('[ERROR] Uploaded file is empty or could not be read.')
        return jsonify({'error': 'Uploaded file is empty or could not be read.'}), 400
    try:
        print('[DEBUG] Starting summarization...')
        summary = summarize_text(text)
        print('[DEBUG] Summary generated.')
        # Ensure summary is formatted with bullet points and new lines
        if isinstance(summary, list):
            formatted_summary = '\n'.join([f"• {point}" for point in summary])
        elif isinstance(summary, str):
            lines = [line.strip() for line in summary.split('\n') if line.strip()]
            formatted_summary = '\n'.join([line if line.startswith('•') else f"• {line}" for line in lines])
        else:
            formatted_summary = str(summary)
        return jsonify({'summary': formatted_summary})
    except Exception as e:
        safe_err = ''.join([c if ord(c) < 128 else '?' for c in str(e)])
        print('[ERROR] Summarization failed:', safe_err)
        return jsonify({'error': f'Summarization failed: {safe_err}'}), 500

@app.route('/plan', methods=['POST'])
def plan():
    print('Received /plan request')
    data = request.get_json()
    if not data or 'hours' not in data or 'topics' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    hours = data['hours']
    topics = data['topics']
    try:
        plan_result = generate_study_plan(topics, hours)
        return jsonify({'plan': plan_result})
    except Exception as e:
        safe_err = ''.join([c if ord(c) < 128 else '?' for c in str(e)])
        print('[ERROR] Planning failed:', safe_err)
        return jsonify({'error': f'Planning failed: {safe_err}'}), 500

# Serve frontend static files
@app.route('/frontend/<path:filename>')
def frontend_static(filename):
    return send_from_directory('frontend', filename)

# Serve main frontend page
@app.route('/app')
def serve_index():
    return send_from_directory('frontend', 'index.html')

# Endpoint for generating study plan

if __name__ == '__main__':
    app.run(debug=True)