class PasswordChecker:
    def __init__(self,password):
        self._password = password
        self.score = None
    
    def score_length(self):
        return min(len(self._password)*10,100)

    def score_characters(self):
        pass

    def score_rarity(self):
        pass

    def score_pwned(self):
        pass

    def update_password(self,new_password):
        self._password = new_password