from flask import Flask, redirect
from yaml import safe_load
from private.controller import profiles, auth, friends
from flask_jwt_extended import JWTManager

app = Flask(__name__,
            static_folder='/static',
            template_folder='./template')

with open('config.yml') as config:
    config_obj = safe_load(config)
with app.app_context() as ctx:
    app.config.update(config_obj)
    ctx.push()

app.register_blueprint(profiles.profiles)
app.register_blueprint(auth.auth)
app.register_blueprint(friends.friends)

jwt = JWTManager(app)


@jwt.expired_token_loader
def redirect_to_login(arg):
    return redirect('/login')


@jwt.invalid_token_loader
def redirect_login(arg):
    return redirect('/login')


@jwt.needs_fresh_token_loader
def redirect_login(arg):
    return redirect('/login')


@jwt.unauthorized_loader
def redirect_login(arg):
    return redirect('/login')


@app.route('/')
def hello():
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
