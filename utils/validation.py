import re

class Validation:
    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @staticmethod
    def is_valid_password(password):
        if len(password) < 8:
            return False
    
        if not any(char.isdigit() for char in password):
            return False
        if re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", password) is None:
            return False
        return True
