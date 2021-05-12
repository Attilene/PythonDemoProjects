import json


class User:
    def __init__(self, login=None, hash_password=None, salt=None, date_registration=None):
        self.login = login
        self.hash_password = hash_password
        self.salt = salt
        self.date_registration = date_registration

    def toJSON(self):
        data = {
            "login": self.login,
            "hash_password": self.hash_password,
            "salt": self.salt,
            "date_registration": self.date_registration
        }
        return json.dumps(data, ensure_ascii=False)

    def get_tuple(self):
        return self.login, self.hash_password, self.salt, self.date_registration