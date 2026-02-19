from flask import Flask, request, jsonify
from flask_cors import CORS
from config_vars import connection
import bcrypt

app = Flask(__name__)
CORS(app, origins=["http://localhost:5174"])

@app.route("/")
def index():
    return jsonify({"status": "Stock API running"})

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    hashed_password = bcrypt.hashpw(
        data["password"].encode(),
        bcrypt.gensalt()
    ).decode()

    con = connection()

    try:
        with con.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (email, password)
                VALUES (%s, %s)
                """,
                (data["email"], hashed_password)
            )
            con.commit()

            return jsonify({
                "id": cur.lastrowid,
                "email": data["email"]
            }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        con.close()

@app.route("/sessions", methods=["POST"])
def login():
    data = request.json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing credentials"}), 400

    con = connection()

    try:
        with con.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE email = %s",
                (data["email"],)
            )
            user = cur.fetchone()

            if not user:
                return jsonify({"error": "Invalid credentials"}), 401

            if not bcrypt.checkpw(
                data["password"].encode(),
                user["password"].encode()
            ):
                return jsonify({"error": "Invalid credentials"}), 401

            return jsonify({
                "message": "Login successful",
                "user_id": user["id"]
            }), 200

    finally:
        con.close()


if __name__ == "__main__":
    app.run(debug=True)