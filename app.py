from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import base64
import io
import os

app = Flask(__name__)

# Set up Gemini AI API key (Replace with your valid API key)
GEMINI_API_KEY ="AIzaSyA8eDMHdzzGSm_sKM8My7II8dpU8Z-FDkw"
genai.configure(api_key=GEMINI_API_KEY)


# Function to encode image for Gemini AI
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files or request.files['image'].filename == '':
        return jsonify({'error': 'No image uploaded'}), 400

    word_count = request.form.get('word_count', type=int)
    if not word_count or word_count <= 0:
        return jsonify({'error': 'Invalid word count'}), 400

    image = request.files['image']
    img = Image.open(image)
    img_encoded = encode_image(img)

    try:
        # Use "gemini-1.5-flash" if "gemini-1.5-pro" exceeds quota
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([
            f"Generate a content of about {word_count} words based on this image.",
            {"mime_type": "image/jpeg", "data": img_encoded}
        ])

        generated_content = response.text if response.text else "No content generated."
        return jsonify({'generated_content': generated_content})

    except Exception as e:
        return jsonify({'error': f"Error generating content: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)