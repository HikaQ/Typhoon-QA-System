from flask import Flask, jsonify
from routes.knowledge_graph import bp as kg_bp
from routes.user import bp as user_bp
from routes.conversation import bp as chat_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(kg_bp)
app.register_blueprint(user_bp)
app.register_blueprint(chat_bp)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "msg": "typhoon graphrag backend running"
    })

if __name__ == "__main__":
    app.run(debug=True)
