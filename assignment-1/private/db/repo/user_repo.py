from private import db


# noinspection SqlResolve
from private.model.user import Profile, Identity, User


class UserRepo:

    @staticmethod
    def get_user_by_id(user_id: int):
        with db.get_db() as connection:
            with connection.cursor() as cursor:
                user_info_query = ("""
                    select u.id as user_id,
                            u.login,
                            u.password,
                            p.city,
                            p.first_name,
                            p.gender,
                            p.surname,
                            p.id as profile_id
                        from user u
                        INNER JOIN profile p on u.id = p.user_id
                        WHERE u.id = %s
                """)
                profile_interests = ("""
                    SELECT pi.name from profile_interests pi
                        WHERE pi.profile_id = %s
                """)
                cursor.execute(user_info_query, (user_id,))
                row = cursor.fetchone()
                if row is None:
                    return None
                user_id, login, password, city, first_name, gender, surname, profile_id = row
                cursor.execute(profile_interests, (profile_id,))
                if cursor.rowcount > 0:
                    user_interests = []
                else:
                    user_interests = cursor.fetchall()
                profile = Profile(profile_id, first_name, surname, gender, city, user_id, [str(u[0]) for u in user_interests])
                return profile

    @staticmethod
    def get_all():
        with db.get_db() as connection:
            with connection.cursor(buffered=True) as cursor:
                user_info = ("""
                                select u.id as user_id,
                                        u.login
                                        from user u
                            """)
                cursor.execute(user_info)
                users = cursor.fetchall()
                user_result = []
                for user_id, login in users:
                    user_result.append(User(user_id, login))
                return user_result

    @staticmethod
    def get_user_creds_by_username(username):
        with db.get_db() as connection:
            with connection.cursor(buffered=True) as cursor:
                user_creds = ("""
                            select u.id as user_id,
                                    u.login,
                                    u.password,
                                    u.password_salt
                                    from user u
                                    WHERE u.login = %s
                                    """)
                cursor.execute(user_creds, (username,))
                user = cursor.fetchone()
                if user is None:
                    return None
                user_id, user_name, user_password, password_salt = user
                identity = Identity(user_id, username, user_password, password_salt)
                return identity

    @staticmethod
    def create_user(identity: Identity, profile: Profile):
        with db.get_db() as connection:
            with connection.cursor() as cursor:
                insert_user_query = ("""
                    INSERT INTO user(login, password, password_salt)
                    VALUES (%(login)s, %(password)s, %(password_salt)s)
                """)
                insert_profile_query = ("""
                    INSERT INTO profile(first_name, surname, gender, city, user_id)
                    VALUES (%(first_name)s, %(surname)s, %(gender)s, %(city)s, %(user_id)s)
                              """)
                insert_interests_query = """
                    INSERT INTO profile_interests(profile_id, name)
                    VALUES (%s, %s)
                """
                user_data = {
                    'login': identity.username,
                    'password': identity.user_pass,
                    'password_salt': identity.password_salt
                }
                cursor.execute(insert_user_query, user_data)
                user_id = cursor.lastrowid
                profile_data = {
                    'first_name': profile.name,
                    'surname': profile.surname,
                    'gender': profile.gender,
                    'city': profile.city,
                    'user_id': user_id
                }
                cursor.execute(insert_profile_query, profile_data)
                profile_id = cursor.lastrowid
                interests_data = [(profile_id, interest) for interest in profile.interests]
                cursor.executemany(insert_interests_query, interests_data)
                connection.commit()

    @staticmethod
    def search_profile(name: str, surname: str):
        with db.get_db() as connection:
            with connection.cursor(buffered=True) as cursor:
                user_info = ("""
                        select 
                            p.user_id,
                            p.city,
                            p.first_name,
                            p.gender,
                            p.surname,
                            p.id as profile_id
                        from profile p
                        where 
                        p.first_name like %(name)s and
                        p.surname like %(surname)s
                        order by p.id asc
                            """)
                profile_search_data = {
                    'name': f'{name}%',
                    'surname': f'{surname}%'
                }
                cursor.execute(user_info, profile_search_data)
                profiles_data = cursor.fetchall()
                profiles = []
                for user_id, city, first_name, gender, surname, profile_id in profiles_data:
                    profiles.append(Profile(profile_id, first_name, surname, gender, city, user_id, []))
                return profiles



