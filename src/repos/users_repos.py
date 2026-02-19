from config_vars import connection
import pymysql

class UsersRepos:

    @staticmethod
    def create(user):
        con = connection()
        try:
            with con.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (email, password) VALUES (%s, %s)",
                    (user["email"], user["password"])
                )
                con.commit()

                return {
                    "id": cur.lastrowid,
                    "email": user["email"],
                    "password": user["password"]
                }

        finally:
            con.close()


    @staticmethod
    def get(user_id):
        con = connection()
        try:
            with con.cursor() as cur:
                cur.execute(
                    "SELECT * FROM users WHERE id = %s",
                    (user_id,)
                )
                result = cur.fetchone()

                return result if result else None

        finally:
            con.close()