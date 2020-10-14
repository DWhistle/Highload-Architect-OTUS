class Profile:
    def __init__(self, profile_id, name, surname, gender, city, user_id, interests: list):
        self.id = profile_id
        self.name = name
        self.surname = surname
        self.gender = gender
        self.city = city
        self.user_id = user_id
        self.interests = interests


class Identity:
    def __init__(self, user_id, username, user_pass, password_salt):
        self.user_id = user_id
        self.username = username
        self.user_pass = user_pass
        self.password_salt = password_salt


class User:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
