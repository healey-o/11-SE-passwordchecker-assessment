from pyhibp import pwnedpasswords as pw
import pyhibp
import sqlite3
import math

class PasswordChecker:
    def __init__(self,password):
        self._password = "password"
        self.score = None

        #Initialise connection to database at intit to decrease processing time later
        self.passwordsConnection = sqlite3.connect("common_passwords.db")
        self.cursor = self.passwordsConnection.cursor()

        #Initialise pyhibp
        pyhibp.set_user_agent(ua="Pass-O-Meter/A simple password secuirty analysing program.")

        #Check if pyhibp can be accessed
        try:
            pw.is_password_breached(password=self._password)
            self.pyhibpAvailiable = True
        except:
            self.pyhibpAvailiable = False

        
        
    

    #Methods - 'score' functions return an integer between 0-100
    def score_length(self): #Scores based on password length

        #Strongest password length is >= 
        return min(math.ceil((2**len(self._password))/40)+5*len(self._password),100)

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
        
        #Ensure the current network allows API calls
        if self.pyhibpAvailiable:
            #Gets the number of times breached
            timesPwned = pw.is_password_breached(password=self._password)

            return max((100 - timesPwned * 3),0)
        else:
            return 100

    def combine_scores(self,lengthWeight,characterWeight,rarityWeight):
        totalWeight = lengthWeight + characterWeight + rarityWeight
        weightedLength = ((self.score_length()/totalWeight)*lengthWeight)
        weightedCharacters = ((self.score_characters()/totalWeight)*characterWeight)
        weightedRarity = ((self.score_rarity()/totalWeight)*rarityWeight)

        
        #The total score is the sum of the weighted scores
        #The score is out of 100, but if the password is breached, the score is calculated as if the return value of self.score_pwned() is the max score.
        return int((weightedLength + weightedCharacters + weightedRarity) * (self.score_pwned()/100))


    #Setter method
    def update_password(self,new_password):
        self._password = new_password