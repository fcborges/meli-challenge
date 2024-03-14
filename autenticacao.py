from flask import Flask, request

app = Flask(__name__)


class Autenticador:

    def __init__(self):
        # Lista de usuarios registrados (este es un ejemplo, en una aplicación real, utilizaría una base de datos)
        self.USERS = [
            {'username': 'admin', 'password': 'admin'},
            {'username': 'challenge', 'password': 'aprove'},
            {'username': 'meli', 'password': 'M3rc4d0L1vr3'}
        ]

    app.config['SECRET_KEY'] = 'chave_secreta'

    def verificar_autenticacao(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return False

        # Verificar se as credenciais estão na lista de usuários cadastrados
        for user in self.USERS:
            if user['username'] == auth.username and user['password'] == auth.password:
                return True

        return False
