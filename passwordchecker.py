import pyhibp
import sqlite3

class PasswordChecker:
    def __init__(self,password):
        self._password = "password"
        self.score = None

        #Initialise connection to database at intit to decrease processing time later
        self.passwordsConnection = sqlite3.connect("common_passwords.db")
        self.cursor = self.passwordsConnection.cursor()
        
    

    #Methods - 'score' functions return an integer between 0-100
    def score_length(self): #Scores based on password length

        #Strongest password length is >= 
        return min(len(self._password)*7,100)

    def score_characters(self): #Scores based on special characters/number used
        specialChars = 0
        numbers = 0
        capitals = 0
        for char in self._password:
            if char.isnumeric():
                numbers += 1
            elif char.isupper():
                capitals += 1
            elif not char.isalnum():#If it is neither a number or letter, it is a special character
                specialChars += 1
        
        #Max score achieved by 2 of each type (numbers, capitals, special characters)
        #Second character of each type is worth less
        return min(33, numbers * 20) + min(34,specialChars * 20) + min(33,capitals * 30)

    def score_rarity(self): #Scores on the commoness of the password
        #Access database and check for password
        self.cursor.execute(
            "SELECT ROWID, COUNT(1) FROM passwords WHERE value = ?",
            (self._password,)
        )

        #Store its row in the database (or None if not in database)
        passwordRow = self.cursor.fetchone()[0]

        #Check if the password was in a row
        if passwordRow != None:
            #Return a lower value the more common the password
            return min(round(passwordRow/5),99)#Gives a score between 0 and 99
        else:
            #Not a common password
            return 100



    def score_pwned(self): #Scores based on if the password is breached
        return 100

    def combine_scores(self,lengthWeight,characterWeight,rarityWeight):
        if self.score_pwned() <= 0: #pwned is either 0 or 100, and if breached score is automatically 0
            return 0
        
        else:
            totalWeight = lengthWeight + characterWeight + rarityWeight
            weightedLength = ((self.score_length()/totalWeight)*lengthWeight)
            weightedCharacters = ((self.score_characters()/totalWeight)*characterWeight)
            weightedRarity = ((self.score_rarity()/totalWeight)*rarityWeight)

            

            return weightedLength + weightedCharacters + weightedRarity


    #Setter method
    def update_password(self,new_password):
        self._password = new_password