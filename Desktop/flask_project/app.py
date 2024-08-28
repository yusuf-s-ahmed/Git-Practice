from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import mysql.connector
import uuid
from waitress import serve

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",  # Use in-memory storage
    default_limits=["200 per day", "50 per hour"]
)

def generate_licence_key():
    """Generate a unique licence key."""
    return str(uuid.uuid4())

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='Q8P$an97A',
        host='127.0.0.1',
        database='shopify_licence_system'
    )

# Create a new licence key
@app.route('/generate-key', methods=['POST'])
@limiter.limit("5 per minute")
def generate_key():
    data = request.json
    customer_email = data.get('email')
    url = data.get('url')

    if not customer_email or not url:
        return jsonify({'error': 'Email and URL are required!'}), 400

    new_key = generate_licence_key()

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        add_licence = ("INSERT INTO licences (licence_key, customer_email, url) "
                       "VALUES (%s, %s, %s)")
        data_licence = (new_key, customer_email, url)

        cursor.execute(add_licence, data_licence)
        cnx.commit()

        return jsonify({'licence_key': new_key, 'email': customer_email, 'url': url}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database Error: {err}'}), 500

    finally:
        cursor.close()
        cnx.close()

# Retrieve licence keys
@app.route('/licences', methods=['GET'])
@limiter.limit("5 per minute")
def get_licences():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("SELECT licence_key, customer_email, url FROM licences")
        results = cursor.fetchall()

        licences = []
        for row in results:
            licences.append({
                'licence_key': row[0],
                'email': row[1],
                'url': row[2]
            })

        return jsonify(licences), 200

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database Error: {err}'}), 500

    finally:
        cursor.close()
        cnx.close()

# Validate a licence key
@app.route('/validate-key', methods=['POST'])
@limiter.limit("5 per minute")
def validate_key():
    data = request.json
    licence_key = data.get('licence_key')
    email = data.get('email')
    url = data.get('url')

    if not licence_key or not email or not url:
        return jsonify({'error': 'Licence key, email, and URL are required!'}), 400

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        query = ("SELECT licence_key FROM licences WHERE licence_key = %s AND customer_email = %s AND url = %s")
        cursor.execute(query, (licence_key, email, url))
        result = cursor.fetchone()

        if result:
            return jsonify({'valid': True}), 200
        else:
            return jsonify({'valid': False, 'error': 'Invalid licence key, email, or URL!'}), 400

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database Error: {err}'}), 500

    finally:
        cursor.close()
        cnx.close()

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    print("Starting server on port 8000...")
    serve(app, host='0.0.0.0', port=8000)