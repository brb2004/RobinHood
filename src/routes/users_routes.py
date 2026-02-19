from flask import Flask
from src.forms.user_form import UserForm
from src.repos.users_repos import UsersRepos
from src.repos.sessions_repos import SessionsRepos
from flask import request
import json
import wtforms_json

class UsersRoutes:
    def __init__(self, app):

        @app.route('/todoappuser', methods=['POST'])
        def create_todoappuser():
            form = UserForm.from_json(request.get_json())
            if not form.validate():
                return json.dumps(form.errors), 422

            user = UsersRepos.create({
                "email": form.email.data,
                "password": form.password.data
            })

            session = SessionsRepos.create({
                "id": user["id"],
            })

            return session, 200