from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Set your OCR.space API key here
OCR_API_KEY = "K89188050688957"

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    image_base64 = data.get('image', None)

    if not image_base64:
        return jsonify({"error": "No image provided"}), 400

    # Remove the "data:image/png;base64," prefix if present
    if ',' in image_base64:
        image_base64 = image_base64.split(',')[1]

    # Send the image to OCR.space API
    response = requests.post(
        'https://api.ocr.space/parse/image',
        files={
            'base64image': image_base64,
        },
        data={
            'apikey': OCR_API_KEY,
        },
    )

    # Process the OCR response
    if response.status_code == 200:
        ocr_data = response.json()
        extracted_text = ocr_data.get("ParsedResults", [{}])[0].get("ParsedText", "")
        return jsonify({"text": extracted_text})
    else:
        return jsonify({"error": "Failed to process the image"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)