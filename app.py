from flask import Flask, request, jsonify, send_file, render_template_string
import os
import subprocess
import logging
import shutil
from datetime import datetime
import json
import zipfile
from pdf2image import convert_from_path

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='pdf_password_removal.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define directories (relative paths for Render compatibility)
INPUT_DIR = os.path.join(os.path.dirname(__file__), "downloads")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "stripped")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
TEMP_PNG_DIR = os.path.join(os.path.dirname(__file__), "temp_png")

# Ensure directories exist
for dir_path in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR, TEMP_PNG_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def remove_pdf_password(input_path, output_path, passwords):
    for password in passwords:
        try:
            result = subprocess.run(
                ["qpdf", "--password=" + password, "--decrypt", input_path, output_path],
                capture_output=True, text=True, check=True
            )
            logging.info(f"Successfully processed: {input_path} with password: {password}")
            return {"success": True, "used_password": password}
        except subprocess.CalledProcessError as e:
            logging.warning(f"Password failed for {input_path}: {password} - {e.stderr}")
            continue
        except Exception as e:
            logging.error(f"Error processing {input_path}: {str(e)}")
            return {"success": False, "error": str(e)}
    return {"success": False, "error": "All passwords failed"}

@app.route('/')
def index():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'index.html')) as f:
            return render_template_string(f.read())
    except FileNotFoundError:
        logging.error("index.html not found")
        return "Error: index.html not found", 500

@app.route('/process', methods=['POST'])
def process_pdfs():
    files = request.files.getlist('files')
    passwords = request.form.getlist('passwords')
    password_list = json.loads(request.form.get('passwordList', '[]'))
    results = []

    # Clear temp directory
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR)

    for i, (file, primary_password) in enumerate(zip(files, passwords)):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        temp_input = os.path.join(TEMP_DIR, f"temp_{timestamp}_{file.filename}")
        output_filename = f"unprotected_{file.filename}"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        file.save(temp_input)
        # Try primary password first, then password list
        passwords_to_try = [primary_password] if primary_password else []
        passwords_to_try.extend(password_list)
        result = remove_pdf_password(temp_input, output_path, passwords_to_try)
        result["filename"] = file.filename
        result["output"] = output_filename
        results.append(result)

    # Clean up temp directory
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR)

    return jsonify({"results": results})

@app.route('/view/<filename>')
def view_file(filename):
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        logging.info(f"Attempting to view file: {file_path}")
        if not os.path.exists(file_path):
            logging.error(f"File does not exist: {file_path}")
            return "Error: File not found", 404
        return send_file(file_path, mimetype='application/pdf', as_attachment=False)
    except Exception as e:
        logging.error(f"Error viewing file {filename}: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        logging.error(f"File not found for download: {filename}")
        return "Error: File not found", 404

@app.route('/png/<filename>')
def convert_to_png(filename):
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        logging.info(f"Converting to PNG: {file_path}")
        if not os.path.exists(file_path):
            logging.error(f"File does not exist: {file_path}")
            return "Error: File not found", 404
        # Convert PDF to PNG
        output_dir = TEMP_PNG_DIR
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_base = os.path.join(output_dir, f"{filename}_page")
        # Convert all pages to PNG
        images = convert_from_path(file_path, dpi=100, output_folder=output_dir, output_file=filename, fmt='png')
        # Collect generated PNGs
        png_files = [f for f in os.listdir(output_dir) if f.startswith(filename) and f.endswith('.png')]
        if not png_files:
            logging.error(f"No PNGs generated for {filename}")
            return "Error: No PNGs generated", 500
        if len(png_files) == 1:
            # Single page: return the PNG
            return send_file(os.path.join(output_dir, png_files[0]), mimetype='image/png', as_attachment=True)
        else:
            # Multiple pages: create a ZIP
            zip_path = os.path.join(output_dir, f"{filename}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for png in png_files:
                    zipf.write(os.path.join(output_dir, png), png)
            return send_file(zip_path, mimetype='application/zip', as_attachment=True)
    except Exception as e:
        logging.error(f"Error converting {filename} to PNG: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    try:
        print("Starting Flask app...")
        port = int(os.getenv('PORT', 8000))  # Use 8000 for Docker
        app.run(debug=False, host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Failed to start Flask app: {str(e)}")
        logging.error(f"Failed to start Flask app: {str(e)}")