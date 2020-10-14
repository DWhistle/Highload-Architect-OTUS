from flask import Blueprint, render_template, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity

from private.db.repo.friends_repo import FriendsRepo
from private.db.repo.user_repo import UserRepo

friends = Blueprint('friend', __name__,
                    template_folder='template',
                    url_prefix='/friend')


@friends.route('/add/<user_id>', methods=['PUT'])
@jwt_required
def add_friend(user_id: int):
    identity = get_jwt_identity()
    if identity is None:
        return redirect('/login')
    if identity == user_id:
        return {'success': False,
                'error': 'Нельзя подружиться самому с собой!'}
    user = UserRepo.get_user_by_id(identity)
    if user is None:
        return redirect('/login')
    FriendsRepo.add_friend(identity, user_id)
    return {'success': True}
