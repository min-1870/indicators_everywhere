from flask import Flask, request, jsonify
from flask_cors import CORS  
from analyze import analyze_stock

app = Flask(__name__)

CORS(app)

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
    app.run(debug=True, port=5000)