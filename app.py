import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import time

# Import our image generation functions
from image_creator import generate_text_to_image, generate_text_and_image_to_image

# --- Flask App Setup ---

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['GENERATED_FOLDER'] = 'static/generated'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Ensure the upload and generated directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# --- Helper Functions ---

def get_api_key():
    """Gets the Google API key from the environment."""
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set.")
    return api_key

# --- Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def handle_generate():
    """Handles the image generation request from the frontend."""
    try:
        api_key = get_api_key()

        mode = request.form.get('mode')
        prompt = request.form.get('prompt')

        if not prompt:
            return jsonify({'error': 'Prompt is required.'}), 400

        timestamp = int(time.time())

        if mode == 'text-to-image':
            output_filename = f"txt2img_{timestamp}.png"
            output_path = os.path.join(app.config['GENERATED_FOLDER'], output_filename)

            generated_path = generate_text_to_image(api_key, prompt, output_path)

            if not generated_path:
                return jsonify({'error': 'Image generation failed on the backend.'}), 500

            return jsonify({
                'imageUrl': f'/{generated_path}',
                'finalPrompt': prompt
            })

        elif mode == 'text-and-image-to-image':
            if 'image' not in request.files:
                return jsonify({'error': 'Image file is required for this mode.'}), 400

            image_file = request.files['image']
            if image_file.filename == '':
                return jsonify({'error': 'No selected file.'}), 400

            # Securely save the uploaded file
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(upload_path)

            output_filename = f"img2img_{timestamp}_{filename}"
            output_path = os.path.join(app.config['GENERATED_FOLDER'], output_filename)

            generated_path, final_prompt = generate_text_and_image_to_image(
                api_key=api_key,
                image_path=upload_path,
                prompt=prompt,
                output_path=output_path
            )

            if not generated_path:
                return jsonify({'error': 'Image generation failed on the backend.'}), 500

            return jsonify({
                'imageUrl': f'/{generated_path}',
                'finalPrompt': final_prompt
            })

        else:
            return jsonify({'error': 'Invalid generation mode specified.'}), 400

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An unexpected server error occurred.'}), 500

# This route is needed to serve the generated images from the 'static' folder
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
