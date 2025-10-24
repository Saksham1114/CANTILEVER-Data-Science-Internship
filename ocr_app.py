import os
import base64
import io
from flask import Flask, request, render_template_string
from PIL import Image
import pytesseract

# --- Tesseract Configuration ---
# If tesseract is not in your system's PATH, you might need to set this.
# On Windows, it might be:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# On Linux/macOS, it's usually found automatically if installed via apt or brew.

app = Flask(__name__)

# --- HTML Template ---
# We are embedding the HTML directly in the Python file for simplicity.
# It uses Tailwind CSS for styling.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tesseract OCR</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .result-box {
            white-space: pre-wrap; /* Preserves newlines and spaces */
            word-break: break-word; /* Breaks long words */
        }
    </style>
</head>
<body class="bg-gray-100 font-sans antialiased">
    <div class="container mx-auto max-w-4xl px-4 py-12">
        <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">
            Image to Text Converter (OCR)
        </h1>

        <!-- Upload Form -->
        <div class="bg-white p-8 rounded-lg shadow-xl mb-10">
            <form method="POST" action="/" enctype="multipart/form-data">
                <label for="image" class="block text-lg font-medium text-gray-700 mb-2">
                    Upload an image:
                </label>
                <input
                    type="file"
                    name="image"
                    id="image"
                    accept="image/png, image/jpeg, image/jpg, image/bmp, image/tiff"
                    required
                    class="block w-full text-sm text-gray-500
                           file:mr-4 file:py-2 file:px-4
                           file:rounded-full file:border-0
                           file:text-sm file:font-semibold
                           file:bg-blue-50 file:text-blue-700
                           hover:file:bg-blue-100"
                />
                <button
                    type="submit"
                    class="mt-6 w-full bg-blue-600 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:bg-blue-700 transition duration-200"
                >
                    Extract Text
                </button>
            </form>
        </div>

        <!-- Error Message -->
        {% if error %}
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative mb-6" role="alert">
                <strong class="font-bold">Error:</strong>
                <span class="block sm:inline">{{ error }}</span>
            </div>
        {% endif %}

        <!-- Results Section -->
        {% if extracted_text is not none %}
            <div class="bg-white rounded-lg shadow-xl overflow-hidden">
                <h2 class="text-2xl font-semibold text-gray-700 p-6 border-b border-gray-200">
                    Results
                </h2>
                <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Uploaded Image Preview -->
                    <div>
                        <h3 class="text-xl font-medium text-gray-800 mb-4">Uploaded Image:</h3>
                        <img src="{{ image_data }}" alt="Uploaded Image" class="rounded-lg shadow-md border border-gray-200">
                    </div>
                    
                    <!-- Extracted Text -->
                    <div>
                        <h3 class="text-xl font-medium text-gray-800 mb-4">Extracted Text:</h3>
                        <div class="result-box bg-gray-50 p-4 border border-gray-200 rounded-lg h-96 overflow-y-auto">
                            {{ extracted_text }}
                        </div>
                    </div>
                </div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    """Main route that handles image upload and OCR."""
    extracted_text = None
    error = None
    image_data = None
    
    if request.method == "POST":
        # Check if an image was uploaded
        if 'image' not in request.files or request.files['image'].filename == '':
            error = "No image file selected. Please upload an image."
            return render_template_string(HTML_TEMPLATE, error=error)
        
        image_file = request.files['image']
        
        try:
            # --- 1. Prepare Image for Preview ---
            # Read image file into bytes, then encode to base64
            image_bytes = image_file.read()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            image_data = f"data:{image_file.mimetype};base64,{base64_image}"
            
            # --- 2. Process Image for OCR ---
            # Create a PIL Image object from the bytes
            # We use io.BytesIO to treat the bytes as a file
            image_object = Image.open(io.BytesIO(image_bytes))
            
            # --- 3. Run Tesseract OCR ---
            extracted_text = pytesseract.image_to_string(image_object)
            
            if not extracted_text.strip():
                extracted_text = "[No text found in the image]"
        
        except pytesseract.TesseractNotFoundError:
            # This is a critical error to catch!
            error = ("Tesseract OCR Error: The 'tesseract' executable was not found. "
                     "Please make sure Tesseract is installed and in your system's PATH. "
                     "See console for setup instructions.")
            print("\n--- TESSERACT NOT FOUND ---")
            print("Please install the Tesseract OCR engine on your system.")
            print("Windows: https://github.com/UB-Mannheim/tesseract/wiki")
            print("macOS: brew install tesseract")
            print("Linux: sudo apt install tesseract-ocr\n")
            
        except Exception as e:
            error = f"An error occurred during processing: {str(e)}"
            
    # Render the page
    return render_template_string(
        HTML_TEMPLATE,
        extracted_text=extracted_text,
        error=error,
        image_data=image_data
    )

if __name__ == "__main__":
    app.run(debug=True)
