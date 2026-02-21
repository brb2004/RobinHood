from  config.config_vars import connection
import pymysql

class SessionsRepos:

    @staticmethod
    def create(session):
        con = connection()
        try:
            with con.cursor() as cur:
                cur.execute(
                    "INSERT INTO sessions (user_id) VALUES (%s)",
                    (session["user_id"],)
                )
                con.commit()

                return {
                    "id": cur.lastrowid,
                    "user_id": session["user_id"]
                }

        finally:
            con.close()


    @staticmethod
    def get(session_id):
        con = connection()
        try:
            with con.cursor() as cur:
                cur.execute(
                    "SELECT * FROM sessions WHERE id = %s",
                    (session_id,)
                )
                result = cur.fetchone()

                return result if result else None

        finally:
            con.close()
