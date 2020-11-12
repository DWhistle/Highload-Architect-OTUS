from flask import Blueprint, render_template, redirect, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from private.db.repo.friends_repo import FriendsRepo
from private.db.repo.user_repo import UserRepo
from private.model.friends import UserFriend
from flask_wtf import Form
from wtforms import StringField, BooleanField, FieldList, IntegerField
from wtforms.validators import DataRequired, Length

profiles = Blueprint('profile', __name__,
                     template_folder='template')

class ProfileSearchForm(Form):
    surname = StringField('', validators=[DataRequired()])
    name = StringField('', validators=[DataRequired()])

@profiles.route('/profile')
@jwt_required
def get_current_profile():
    identity = get_jwt_identity()
    if identity is None:
        return redirect('/login')
    user_info = UserRepo.get_user_by_id(identity)
    if user_info is None:
        return redirect('/login')
    friends = FriendsRepo.get_user_friends_list(identity)
    all_users = UserRepo.get_all()
    for user in all_users:
        if user.id != identity and user.id not in friends.keys():
            friends.update({user.id: UserFriend(user.id, user.username, 0, 0)})

    return render_template('profile_page.html', user=user_info, friends=friends.values())


@profiles.route('/profile/search', methods=['GET'])
def get_profile_by_name_surname():
    return render_template('profile_search.html', form = ProfileSearchForm(meta={'csrf': False}))


@profiles.route('/profile/search', methods=['POST'])
def search():
    profile_search = ProfileSearchForm(request.form, meta={'csrf': False})
    if profile_search.is_submitted():
        profiles = UserRepo.search_profile(profile_search.name.data, profile_search.surname.data)
        return render_template('profile_search.html', profiles = profiles, form = profile_search)
    else:
        return get_profile_by_name_surname()