from flask import Flask, request, jsonify
from flask_cors import CORS  
from constants import TICKERS_RECOMMEND_NUMBER
from analyze import analyze_stock
from recommend import recommend_tickers

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/analyze', methods=['GET'])
def get_analyze():
    user_input = request.args.get('input', '')
    
    try:
        result = analyze_stock(user_input)
        return jsonify(result), 200
    
    except ValueError as ve:        
        return jsonify({'error': str(ve)}), 400

    except Exception as _:
        return jsonify({'error': 'Unhandled Exception' }), 400
    
@app.route('/api/recommend', methods=['GET'])
def get_recommend():
    
    try:
        result = recommend_tickers(TICKERS_RECOMMEND_NUMBER)
        return jsonify(result), 200

    except Exception as _:
        return jsonify({'error': 'Unhandled Exception' }), 400

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
    )