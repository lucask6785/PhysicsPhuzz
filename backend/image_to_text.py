from PIL import Image
import pytesseract

# Path to the image file
image_path = ""
# Open the image
image = Image.open(image_path)

# Extract text using Tesseract
extracted_text = pytesseract.image_to_string(image)

print("Extracted Text:")
print(extracted_text)