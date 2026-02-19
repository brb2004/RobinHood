from flask import request, jsonify
from config_vars import connection
import pymysql


def initSessions(app):

    @app.route('/sessions', methods=['POST'])
    def create_session():
        data = request.json()

        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Missing email or password"}), 400

        con = connection()

        try:
            with con.cursor() as cur:

                # Find user
                cur.execute(
                    "SELECT * FROM users WHERE email = %s AND password = %s",
                    (data["email"], data["password"])
                )
                user = cur.fetchone()

                if not user:
                    return jsonify({"error": "Invalid email or password"}), 401

                # Create session
                cur.execute(
                    "INSERT INTO sessions (user_id) VALUES (%s)",
                    (user["id"],)
                )
                con.commit()

                return jsonify({
                    "session_id": cur.lastrowid,
                    "user_id": user["id"]
                }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            con.close()
