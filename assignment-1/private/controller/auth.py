from flask import Blueprint, render_template, redirect, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FieldList, IntegerField
from wtforms.validators import DataRequired, Length
from private.model.user import Profile, Identity
import private.auth as auth_module
from flask_jwt_extended import create_access_token
from private.db.repo.user_repo import UserRepo

auth = Blueprint('auth', __name__,
                 template_folder='template')


class RegistrationRequest(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    gender = StringField('gender', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    interests = FieldList(StringField('interests'), min_entries=1, validators=[DataRequired()])
    password = StringField('password', validators=[Length(min=6, max=20)])


class LoginRequest(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationRequest(meta={'csrf': False})
    if form.is_submitted():
        if not form.validate():
            return 'error'
        else:
            interests = list(form.interests.data)
            salt = auth_module.generate_salt()
            user_identity = Identity(0, form.username.data, auth_module.encode_password(form.password.data, salt), salt)
            user_profile = Profile(0, form.name.data, form.surname.data, int(form.gender.data), form.city.data, 0,
                                   [interest for interest in interests if interest])
            UserRepo.create_user(user_identity, user_profile)
        return redirect('/login')
    else:

        return render_template('registration.html')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginRequest(meta={'csrf': False})
    if form.is_submitted():
        if not form.validate():
            return 'error'
        else:
            user = auth_module.authenticate(form.username.data, form.password.data)
            if not user:
                return render_template('login_failure.html')
            resp = make_response(render_template('login_success.html'))
            resp.set_cookie('JwtToken', create_access_token(user.user_id))
            return resp
    return render_template('login.html')


@auth.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie('JwtToken', '', expires=0)
    return resp
