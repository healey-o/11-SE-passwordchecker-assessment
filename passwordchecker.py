class PasswordChecker:
    def __init__(self,password):
        self.password = password
        self.score = None
    
    def score_length(self):
        return min(len(self.password)*10,100)

    def score_characters(self):
        pass

    def score_rarity(self):
        pass

    def score_security(self):
        pass