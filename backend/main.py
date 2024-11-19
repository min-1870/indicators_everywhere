from flask import Flask, request, jsonify
from flask_cors import CORS  
from analyze import analyze_stock

app = Flask(__name__)

CORS(app)  # Enable CORS for all routes

@app.route('/api/data', methods=['GET'])
def get_data():
    user_input = request.args.get('input', '')
    # Process the input and send a response
    try:
        result = analyze_stock(user_input)
        return jsonify(result), 200
    
    except Exception as e:
        # Handle any exceptions that occur
        result = {'error': str(e)}
        return jsonify(result), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)