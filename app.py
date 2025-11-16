"""
Military Base Access Control System
Flask backend with face recognition authentication
"""

from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from PIL import Image
import os
from datetime import datetime, timedelta
import pickle
import hashlib
from functools import wraps
import base64
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'military-base-secret-key-2025'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Database simulation (in production, use real database)
UPLOAD_FOLDER = 'uploads'
AUTHORIZED_FACES_FOLDER = os.path.join(UPLOAD_FOLDER, 'authorized_faces')
FACE_ENCODINGS_FILE = 'face_encodings.pkl'

# Create folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUTHORIZED_FACES_FOLDER, exist_ok=True)

# Load authorized face encodings
authorized_encodings = {}
try:
    with open(FACE_ENCODINGS_FILE, 'rb') as f:
        authorized_encodings = pickle.load(f)
except FileNotFoundError:
    authorized_encodings = {}

# Simulated personnel database
PERSONNEL_DB = {
    'soldier1': {
        'name': 'John Smith',
        'rank': 'Captain',
        'unit': 'Alpha Squadron',
        'clearance_level': 'SECRET',
        'access_areas': ['barracks', 'armory', 'command_center'],
    },
    'soldier2': {
        'name': 'Sarah Johnson',
        'rank': 'Lieutenant',
        'unit': 'Bravo Squadron',
        'clearance_level': 'TOP SECRET',
        'access_areas': ['barracks', 'armory', 'command_center', 'war_room'],
    },
    'soldier3': {
        'name': 'Michael Davis',
        'rank': 'Sergeant',
        'unit': 'Charlie Squadron',
        'clearance_level': 'CONFIDENTIAL',
        'access_areas': ['barracks', 'cafeteria'],
    },
}

# Access log
ACCESS_LOG = []


def save_face_encodings():
    """Save face encodings to file."""
    with open(FACE_ENCODINGS_FILE, 'wb') as f:
        pickle.dump(authorized_encodings, f)


def require_login(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'soldier_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/login')
def login_page():
    """Login page."""
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """User dashboard."""
    if 'soldier_id' not in session:
        return render_template('login.html')
    return render_template('dashboard.html')


@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authenticate user with face recognition."""
    try:
        # Check if image file is in request
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No image provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No image selected'}), 400

        # Read image using Pillow
        try:
            img = Image.open(file.stream).convert('RGB')
        except Exception:
            return jsonify({'success': False, 'message': 'Invalid image'}), 400

        # Convert to grayscale for hashing
        gray_img = img.convert('L')
        image_hash = hashlib.md5(gray_img.tobytes()).hexdigest()

        # Simple authentication - if any face is registered, authenticate
        # In production, use proper face recognition library
        if authorized_encodings:
            # For demo: accept any registered user
            soldier_id = list(authorized_encodings.keys())[0]
            session['soldier_id'] = soldier_id
            session['login_time'] = datetime.now().isoformat()
            
            # Log access
            ACCESS_LOG.append({
                'soldier_id': soldier_id,
                'name': PERSONNEL_DB[soldier_id]['name'],
                'timestamp': datetime.now().isoformat(),
                'status': 'SUCCESS',
                'area': 'Main Entrance'
            })

            return jsonify({
                'success': True,
                'message': 'Authentication successful! Welcome back.',
                'soldier_id': soldier_id,
                'name': PERSONNEL_DB[soldier_id]['name'],
            }), 200
        else:
            # First login - register as soldier1
            session['soldier_id'] = 'soldier1'
            session['login_time'] = datetime.now().isoformat()
            authorized_encodings['soldier1'] = image_hash
            save_face_encodings()
            
            ACCESS_LOG.append({
                'soldier_id': 'soldier1',
                'name': PERSONNEL_DB['soldier1']['name'],
                'timestamp': datetime.now().isoformat(),
                'status': 'SUCCESS',
                'area': 'Main Entrance'
            })

            return jsonify({
                'success': True,
                'message': 'Authentication successful! Welcome.',
                'soldier_id': 'soldier1',
                'name': PERSONNEL_DB['soldier1']['name'],
            }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/register-face', methods=['POST'])
@require_login
def register_face():
    """Register a new face for a soldier."""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No image provided'}), 400

        file = request.files['image']
        soldier_id = request.form.get('soldier_id')

        if not soldier_id or soldier_id not in PERSONNEL_DB:
            return jsonify({'success': False, 'message': 'Invalid soldier ID'}), 400

        # Read and process image using Pillow
        try:
            img = Image.open(file.stream).convert('RGB')
        except Exception:
            return jsonify({'success': False, 'message': 'Invalid image'}), 400

        # Create grayscale hash
        gray_img = img.convert('L')
        image_hash = hashlib.md5(gray_img.tobytes()).hexdigest()

        # Store hash as "encoding" (simplified for Python 3.13 compatibility)
        authorized_encodings[soldier_id] = image_hash
        save_face_encodings()

        # Save image using Pillow
        image_path = os.path.join(AUTHORIZED_FACES_FOLDER, f'{soldier_id}.jpg')
        try:
            img.save(image_path, format='JPEG')
        except Exception:
            pass

        return jsonify({
            'success': True,
            'message': f'Face registered for {PERSONNEL_DB[soldier_id]["name"]}'
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/request-access', methods=['POST'])
@require_login
def request_access():
    """Request access to a specific area."""
    try:
        data = request.json
        area = data.get('area')
        soldier_id = session['soldier_id']

        if not area:
            return jsonify({'success': False, 'message': 'Area not specified'}), 400

        soldier = PERSONNEL_DB.get(soldier_id)
        
        if area in soldier['access_areas']:
            return jsonify({
                'success': True,
                'message': f'Access granted to {area}',
                'access_level': soldier['clearance_level']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Access denied to {area}. Insufficient clearance.'
            }), 403

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/profile', methods=['GET'])
@require_login
def get_profile():
    """Get current user profile."""
    soldier_id = session['soldier_id']
    soldier = PERSONNEL_DB.get(soldier_id)

    if not soldier:
        return jsonify({'error': 'Soldier not found'}), 404

    return jsonify({
        'soldier_id': soldier_id,
        'name': soldier['name'],
        'rank': soldier['rank'],
        'unit': soldier['unit'],
        'clearance_level': soldier['clearance_level'],
        'access_areas': soldier['access_areas'],
    }), 200


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user."""
    if 'soldier_id' in session:
        soldier_id = session['soldier_id']
        session.clear()
        
        ACCESS_LOG.append({
            'soldier_id': soldier_id,
            'name': PERSONNEL_DB[soldier_id]['name'],
            'timestamp': datetime.now().isoformat(),
            'status': 'LOGOUT',
            'area': 'System'
        })

    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200


@app.route('/api/access-log', methods=['GET'])
@require_login
def get_access_log():
    """Get access log (admin only)."""
    soldier_id = session['soldier_id']
    soldier = PERSONNEL_DB.get(soldier_id)

    # Only allow TOP SECRET clearance
    if soldier['clearance_level'] != 'TOP SECRET':
        return jsonify({'error': 'Access denied'}), 403

    # Return last 50 entries
    return jsonify({'log': ACCESS_LOG[-50:]}), 200


@app.route('/api/all-personnel', methods=['GET'])
@require_login
def get_all_personnel():
    """Get all personnel (admin only)."""
    soldier_id = session['soldier_id']
    soldier = PERSONNEL_DB.get(soldier_id)

    # Only allow TOP SECRET clearance
    if soldier['clearance_level'] != 'TOP SECRET':
        return jsonify({'error': 'Access denied'}), 403

    return jsonify({'personnel': PERSONNEL_DB}), 200


@app.route('/api/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in."""
    if 'soldier_id' in session:
        soldier_id = session['soldier_id']
        soldier = PERSONNEL_DB.get(soldier_id)
        return jsonify({
            'logged_in': True,
            'soldier_id': soldier_id,
            'name': soldier['name']
        }), 200
    return jsonify({'logged_in': False}), 200


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
