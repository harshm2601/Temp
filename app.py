from flask import Flask, request, jsonify, render_template, send_from_directory, Response
from flask_cors import CORS
from functools import wraps
import base64

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# In-memory storage for horses
horses = []

USERNAME = 'root'
PASSWORD = 'root'

def check_auth(auth_header):
    if not auth_header or not auth_header.startswith('Basic '):
        return False
    try:
        encoded = auth_header.split(' ', 1)[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        username, password = decoded.split(':', 1)
        return username == USERNAME and password == PASSWORD
    except Exception:
        return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not check_auth(auth):
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials',
                401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')

@app.route('/api/horses', methods=['GET'])
@requires_auth
def get_horses():
    return jsonify(horses)

@app.route('/api/horses', methods=['POST'])
@requires_auth
def add_horse():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    if not name or not description:
        return jsonify({'error': 'Name and description required'}), 400
    # Prevent duplicate names
    if any(h['name'] == name for h in horses):
        return jsonify({'error': 'Horse already exists'}), 400
    horses.append({'name': name, 'description': description})
    return jsonify({'success': True})

@app.route('/api/horses/<name>', methods=['DELETE'])
@requires_auth
def delete_horse(name):
    global horses
    horses = [h for h in horses if h['name'] != name]
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True) 