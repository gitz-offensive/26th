from flask import Flask, request, jsonify, render_template
import hashlib
import os

app = Flask(__name__)

# Function to calculate file hash
def calculate_file_hash(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to verify file integrity
@app.route('/verify', methods=['POST'])
def verify_file():
    if 'file' not in request.files or 'expected_hash' not in request.form or 'algorithm' not in request.form:
        return jsonify({'error': 'File, expected hash, or algorithm missing'}), 400

    file = request.files['file']
    expected_hash = request.form['expected_hash']
    algorithm = request.form['algorithm']

    # Validate the selected algorithm
    if algorithm not in ['md5', 'sha1', 'sha256']:
        return jsonify({'error': 'Invalid algorithm selected'}), 400

    # Save the uploaded file temporarily
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Calculate the file hash
    file_hash = calculate_file_hash(file_path, algorithm)

    # Clean up the uploaded file
    os.remove(file_path)

    # Compare the hashes
    if file_hash == expected_hash:
        return jsonify({'status': 'success', 'message': 'File integrity verified', 'algorithm': algorithm})
    else:
        return jsonify({'status': 'failure', 'message': 'File integrity check failed', 'algorithm': algorithm})

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
