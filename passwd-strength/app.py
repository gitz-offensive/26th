from flask import Flask, request, jsonify, render_template
import random
import string

app = Flask(__name__)

# Function to check password strength
def is_password_secure(password):
    # Check if password meets requirements
    if len(password) < 10:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in string.punctuation for char in password):
        return False
    return True

# Function to generate a secure password
def generate_secure_password():
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation

    # Ensure at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars),
    ]

    # Fill the rest of the password with random characters
    for _ in range(6):  # Total length is 10
        password.append(random.choice(lowercase + uppercase + digits + special_chars))

    # Shuffle the password to avoid predictable patterns
    random.shuffle(password)
    return ''.join(password)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to check password and generate a secure one if needed
@app.route('/check-password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get('password')

    if not password:
        return jsonify({'error': 'Password is required'}), 400

    # Check if the password is secure
    if is_password_secure(password):
        return jsonify({'status': 'success', 'message': 'Password is secure'})
    else:
        # Generate a secure password
        secure_password = generate_secure_password()
        return jsonify({
            'status': 'failure',
            'message': 'Password does not meet requirements',
            'secure_password': secure_password,
        })

if __name__ == '__main__':
    app.run(debug=True)
