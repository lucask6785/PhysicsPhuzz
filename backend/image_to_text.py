from flask import Flask, request, jsonify
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# OCR API URL and API Key
OCR_API_URL = 'https://api.ocr.space/parse/image'  # Replace with the actual OCR API URL
OCR_API_KEY = 'K89188050688957'  # Insert your OCR API key here

# File extension validation
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload-image', methods=['POST'])
def upload_image():
    # Check if 'image' exists in the request files
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['image']
    
    # Check if the file is empty
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    # Validate file type
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the uploaded file
        file.save(filepath)

        # Send the image to the OCR API
        with open(filepath, 'rb') as image_file:
            files = {'file': (filename, image_file, 'image/jpeg')}  # Adjust MIME type if necessary
            headers = {'Authorization': f'Bearer {OCR_API_KEY}'}
            response = requests.post(OCR_API_URL, files=files, headers=headers)

        # Handle OCR response
        if response.status_code == 200:
            data = response.json()
            extracted_text = data.get('ParsedResults', [{}])[0].get('ParsedText', '').strip()

            # Print the extracted text
            print(f"Extracted Text:\n{extracted_text}")
            
            return jsonify({'success': True, 'text': extracted_text})
        else:
            return jsonify({'success': False, 'message': 'OCR API failed', 'error': response.text})

    return jsonify({'success': False, 'message': 'Invalid file type'})

# Run the Flask app
if __name__ == '__main__':
    # Add the path to your image file directly
    image_file_path = "C:\\Users\\jaron\\OneDrive\\Desktop\\Website\\SwampHacksX\\backend\\assets"  # Path to your image file
    
    # Send image as a POST request to the upload-image route
    with open(image_file_path, 'rb') as f:
        files = {'image': f}
        response = requests.post('http://127.0.0.1:5000/upload-image', files=files)  # Change URL if needed
    
    # Print response from the API (extracted text)
    print(response.json())

    # Start the Flask app in debug mode
    app.run(debug=True)
