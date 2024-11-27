from flask import Flask, request, jsonify
from flask_cors import CORS  
from analyze import analyze_stock
from helper_functions import upload_index, upload_favicon

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
upload_index('index.html')
upload_favicon('favicon.ico')

@app.route('/api/data', methods=['GET'])
def get_data():
    user_input = request.args.get('input', '')
    
    try:
        result = analyze_stock(user_input)
        return jsonify(result), 200
    
    except ValueError as ve:        
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        return jsonify({'error': 'Unhandled Exception' }), 400

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=5000)