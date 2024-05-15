class PasswordChecker:
    def __init__(self,password):
        self._password = password
        self.score = None
    

    #Methods - 'score' functions return an integer between 0-100
    def score_length(self): #Scores based on password length
        return min(len(self._password)*7,100)

    def score_characters(self): #Scores based on special characters/number used
        specialChars = 0
        numbers = 0
        for char in self._password:
            if char.isnumeric():
                numbers += 1
            elif not char.isalnum():
                specialChars += 1
        
        #Max score achieved by 2 numbers and 2 special characters
        return min(50, numbers * 35) + min(50,specialChars * 35)

    def score_rarity(self): #Scores on the commoness of the password
        pass

    def score_pwned(self): #Scores based on if the password is breached
        pass

    #Setter method
    def update_password(self,new_password):
        self._password = new_password