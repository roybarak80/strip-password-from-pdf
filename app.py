from flask import Flask, request, jsonify, send_file, render_template_string
import os
import subprocess
import logging
import shutil
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='pdf_password_removal.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define directories
INPUT_DIR = "/Users/roybarak/Projects/strip-pass-pdf/downloads"
OUTPUT_DIR = "/Users/roybarak/Projects/strip-pass-pdf/stripped"
TEMP_DIR = "/Users/roybarak/Projects/strip-pass-pdf/temp"

# Ensure directories exist
for dir_path in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def remove_pdf_password(input_path, output_path, password):
    try:
        result = subprocess.run(
            ["qpdf", "--password=" + password, "--decrypt", input_path, output_path],
            capture_output=True, text=True, check=True
        )
        logging.info(f"Successfully processed: {input_path}")
        return {"success": True}
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to process {input_path}: {e.stderr}")
        return {"success": False, "error": e.stderr}
    except Exception as e:
        logging.error(f"Failed to process {input_path}: {str(e)}")
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    with open(os.path.join(os.path.dirname(__file__), 'index.html')) as f:
        return render_template_string(f.read())

@app.route('/process', methods=['POST'])
def process_pdfs():
    files = request.files.getlist('files')
    passwords = request.form.getlist('passwords')
    results = []

    # Clear temp directory
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR)

    for i, (file, password) in enumerate(zip(files, passwords)):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        temp_input = os.path.join(TEMP_DIR, f"temp_{timestamp}_{file.filename}")
        output_filename = f"unprotected_{file.filename}"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        file.save(temp_input)
        result = remove_pdf_password(temp_input, output_path, password)
        result["filename"] = file.filename
        result["output"] = output_filename
        results.append(result)

    # Clean up temp directory
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR)

    return jsonify({"results": results})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)
@app.route('/view/<filename>')
def view_file(filename):
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        return send_file(file_path, mimetype='application/pdf', as_attachment=False)
    except FileNotFoundError:
        logging.error(f"File not found for viewing: {filename}")
        return "Error: File not found", 404

if __name__ == "__main__":
    try:
        print("Starting Flask app...")
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"Failed to start Flask app: {str(e)}")
        logging.error(f"Failed to start Flask app: {str(e)}")