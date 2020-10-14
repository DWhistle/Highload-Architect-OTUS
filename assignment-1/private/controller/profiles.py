from flask import Blueprint, render_template, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity

from private.db.repo.friends_repo import FriendsRepo
from private.db.repo.user_repo import UserRepo
from private.model.friends import UserFriend

profiles = Blueprint('profile', __name__,
                     template_folder='template')


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
