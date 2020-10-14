from private import db
from private.model.friends import UserFriend


class FriendsRepo:
    @staticmethod
    def get_user_friends_list(user_id: int):
        with db.get_db() as connection:
            with connection.cursor() as cursor:
                user_friends = (""" SELECT  ufi.user_id as user_id,
                                        ufi.friend_user_id as friend_user_id,
                                        u.login as friend_username,
                                        ufi.is_approved as is_approved,
                                        COALESCE(ufi2.is_approved, 0) as has_friend_approved
                                        
                                        FROM user_friend_invites ufi
                                        INNER JOIN user u ON u.id = ufi.friend_user_id
                                        LEFT JOIN user_friend_invites ufi2 on 
                                        ufi2.friend_user_id = ufi.user_id and 
                                        ufi2.user_id = ufi.friend_user_id
                                        WHERE ufi.user_id = %(user_id)s
                            """)
                cursor.execute(user_friends, {'user_id': user_id})
                friends = cursor.fetchall()
                friends_response = {}
                for user_id, friend_user_id, friend_username, is_approved, has_friend_approved in friends:
                    friends_response.update({friend_user_id: UserFriend(friend_user_id, friend_username, is_approved, has_friend_approved)})
                return friends_response

    @staticmethod
    def add_friend(user_id: int, user_to_friend_id: int):
        with db.get_db() as connection:
            with connection.cursor(buffered=True) as cursor:
                friend_upsert = "friend_add"
                users_data = (user_id, user_to_friend_id)
                cursor.callproc(friend_upsert, users_data)
                connection.commit()
