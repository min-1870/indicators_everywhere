from flask import Flask, request, jsonify
from flask_cors import CORS
from src.app.constants import TICKERS_RECOMMEND_NUMBER
from src.app.analyze_stock import analyze_stock
from src.app.recommend_tickers import recommend_tickers

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/analyze", methods=["GET"])
def get_analyze():
    user_input = request.args.get("input", "")

    try:
        result = analyze_stock(user_input)
        return jsonify(result), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/recommend", methods=["GET"])
def get_recommend():

    try:
        result = recommend_tickers(TICKERS_RECOMMEND_NUMBER)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
    )
