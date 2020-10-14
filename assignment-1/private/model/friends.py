class UserFriend:
    def __init__(self, friend_user_id, friend_username, is_approved, has_friend_approved):
        self.user_id = friend_user_id
        self.username = friend_username
        self.is_approved = is_approved
        self.has_friend_approved = has_friend_approved
