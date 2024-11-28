from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt
from models.user import User
from database import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:admin123@127.0.0.1:3306/flask-crud"

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)

            return jsonify({"message": "Login realizado com sucesso"})

    return jsonify({"message": "Credenciais invalidas"}), 400


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()

    return jsonify({"message": "Logout realizado com sucesso"})


@app.route("/user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role="user")
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "user_id": user.id,
            "message": "Usuario cadastrado com sucesso"
        })

    return jsonify({"message": "Dados invalidos"}), 400


@app.route("/user/<int:user_id>", methods=["GET"])
@login_required
def read_user(user_id):
    user = User.query.get(user_id)

    if user:
        return jsonify({"username": user.username})

    return jsonify({"message": "Usuario nao encontrado"}), 404


@app.route("/user/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)

    if user_id != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operacao nao permitida"}), 403

    if user and data.get("password"):
        user.password = bcrypt.hashpw(str.encode(data.get("password")), bcrypt.gensalt())
        db.session.commit()

        return jsonify({
            "user_id": user.id,
            "message": f"Usuario foi atualizado com sucesso"
        })

    return jsonify({"message": "Usuario nao encontrado"}), 404


@app.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if current_user.role != "admin":
        return jsonify({"message": "Operacao nao permitida"}), 403

    if user_id == current_user.id:
        return jsonify({"message": "Delecao nao permitida"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "Usuario deletado com sucesso"})

    return jsonify({"message": "Usuario nao encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
