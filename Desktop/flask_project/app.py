from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mysqldb import MySQL
from flask_cors import CORS  # Import CORS
import uuid
from waitress import serve

app = Flask(__name__)

# Configure CORS to allow specific origins
cors = CORS(app, resources={
    r"/validate-key": {"origins": [
        "https://sitebyjirointro.myshopify.com",
        "https://admin.shopify.com"
    ]}
})

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",  # Use in-memory storage
    default_limits=["200 per day", "50 per hour"]
)

# Configuring MySQL connection
app.config['MYSQL_HOST'] = 'zy4wtsaw3sjejnud.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'ajrs53ejhmu768yw'
app.config['MYSQL_PASSWORD'] = 'p39gv878dtjstn3c'
app.config['MYSQL_DB'] = 'c85mf4temuzagd4z'

# Initialize MySQL
mysql = MySQL(app)

def generate_licence_key():
    """Generate a unique licence key."""
    return str(uuid.uuid4())

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
        cur = mysql.connection.cursor()
        add_licence = ("INSERT INTO licences (licence_key, customer_email, url) "
                       "VALUES (%s, %s, %s)")
        data_licence = (new_key, customer_email, url)
        cur.execute(add_licence, data_licence)
        mysql.connection.commit()
        cur.close()

        return jsonify({'licence_key': new_key, 'email': customer_email, 'url': url}), 201

    except Exception as err:
        app.logger.error(f'Database Error: {err}')
        return jsonify({'error': f'Database Error: {err}'}), 500

# Retrieve licence keys
@app.route('/licences', methods=['GET'])
@limiter.limit("5 per minute")
def get_licences():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT licence_key, customer_email, url FROM licences")
        results = cur.fetchall()
        cur.close()

        licences = [{'licence_key': row[0], 'email': row[1], 'url': row[2]} for row in results]
        return jsonify(licences), 200

    except Exception as err:
        app.logger.error(f'Database Error: {err}')
        return jsonify({'error': f'Database Error: {err}'}), 500

# Validate a licence key
@app.route('/validate-key', methods=['POST'])
@limiter.limit("5 per minute")
def validate_key():
    request_data = request.get_json()
    licence_key = request_data.get('licence_key')
    email = request_data.get('email')
    url = request_data.get('url')

    if not licence_key or not email or not url:
        return jsonify({'error': 'Licence key, email, and URL are required!'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM licences WHERE licence_key = %s AND customer_email = %s AND url = %s",
                    (licence_key, email, url))
        result = cur.fetchone()
        cur.close()

        if result:
            return jsonify({"valid": True}), 200
        else:
            return jsonify({"valid": False}), 200

    except Exception as err:
        app.logger.error(f'Error validating key: {err}')
        return jsonify({"error": f"Internal server error: {err}"}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    print("Starting server on port 8000...")
    serve(app, host='0.0.0.0', port=8000)