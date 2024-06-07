from pyhibp import pwnedpasswords as pw
import pyhibp
import sqlite3
import math


class PasswordChecker:
    def __init__(self,password):
        self._password = "password"

        #Total score
        self._score = 0

        #List of possible scores for password
        self.RATINGS = ["Very Weak","Weak","Strong","Very Strong"]

        #The current password rating
        self._current_rating = ""

        #Individual scores for character types
        self._length_score = 0
        self._character_score = 0
        self._rarity_score = 0
        self._pwned_score = 0

        #Counter for types of charcters
        self._specialCount = 0
        self._numberCount = 0
        self._upperCount = 0
        self._lowerCount = 0

        #Initialise connection to database at intit to decrease processing time later
        self._passwordsConnection = sqlite3.connect("common_passwords.db")
        self._cursor = self._passwordsConnection.cursor()

        #Initialise pyhibp
        pyhibp.set_user_agent(ua="Pass-O-Meter/A simple password secuirty analysing program.")

        #Check if pyhibp can be accessed
        try:
            self._timesPwned = pw.is_password_breached(password=self._password)
            self._pyhibpAvailiable = True 
        except:
            self._timesPwned = None
            self._pyhibpAvailiable = False
        

        
        
    

    #Methods - 'score' functions return an integer between 0-100
    def score_length(self): #Scores based on password length

        #Scores based on length using an exponential function
        self._length_score = min(math.ceil((2**len(self._password))/40)+10*len(self._password),100)

    def score_characters(self): #Scores based on special characters/number used
        self._numberCount = 0
        self._upperCount = 0
        self._lowerCount = 0
        self._specialCount = 0
        
        for char in self._password:
            if char.isnumeric():
                self._numberCount += 1
            elif char.isupper():
                self._upperCount += 1
            elif char.islower():
                self._lowerCount += 1
            elif not char.isalnum():#If it is neither a number or letter, it is a special character
                self._specialCount += 1
        
        #Max score achieved by 2 of each type (numbers, uppercase, lowercase, special characters)
        #Second character of each type is worth less
        self._character_score = min(25, self._numberCount * 20) + min(25, self._specialCount * 20) + min(25, self._upperCount * 30) + min(25, self._lowerCount * 30)

    def score_rarity(self): #Scores on the commoness of the password
        #Access database and check for password
        self._cursor.execute(
            "SELECT ROWID, COUNT(1) FROM passwords WHERE value = ?",
            (self._password,)
        )

        #Store its row in the database (or None if not in database)
        passwordRow = self._cursor.fetchone()[0]

        #Check if the password was in a row
        if passwordRow != None:
            #Return a lower value the more common the password
            self._rarity_score = min(round(passwordRow/5),99)#Gives a score between 0 and 99
        else:
            #Not a common password
            self._rarity_score = 100



    def score_pwned(self): #Scores based on if the password is breached
        #Ensure the current network allows API calls
        if self._pyhibpAvailiable:

            #Gets the number of times breached
            self._timesPwned = pw.is_password_breached(password=self._password)

            self._pwned_score = max((100 - self._timesPwned / 5),0)
        else:
            self._pwned_score = 100
    
    def contains_password(self):
        if "password" in self._password.lower():
            return True
        else:
            return False

    #Combines all scores using weightings
    def combine_scores(self,lengthWeight,characterWeight,rarityWeight):
        if self.contains_password():
            self._score = 0
        else:
            totalWeight = lengthWeight + characterWeight + rarityWeight
            weightedLength = ((self._length_score/totalWeight)*lengthWeight)
            weightedCharacters = ((self._character_score/totalWeight)*characterWeight)
            weightedRarity = ((self._rarity_score/totalWeight)*rarityWeight)

        
        #The total score is the sum of the weighted scores
        #The score is out of 100, but if the password is breached, the score is calculated as if the return value of self.score_pwned() is the max score.
            self._score = int((weightedLength + weightedCharacters + weightedRarity) * (self._pwned_score/100))

    #Give a rating based on score
    def rate_password(self):
        #The size of each rating 'bracket'
        ratingSize = 100//len(self.RATINGS)

        #Repeats until the score is lower than the current rating bracket
        completed = False
        for ratingBracket in range(1,len(self.RATINGS)+1):
            if self._score <= ratingSize * ratingBracket and not completed:
                self._current_rating = self.RATINGS[ratingBracket-1]
                completed = True
            

    #Generates feedback based on score
    def generate_feedback(self):
        feedback = ""

        if self.contains_password():
            feedback += "Don't put 'password' in your password. That's just lazy."
        elif self._score == 100:
            feedback += "Your password has achieved the maximum score. You have a very secure password!"
        else:
            feedback += f"Your password is {self._current_rating.lower()}."
            
            #Stores score of each type of 'problem' (not including _pwned_score)
            problems = [self._length_score, self._character_score, self._rarity_score]
            
            #Report on the haveibeenpwned status
            if self.get_times_pwned():
                feedback += (f"\n\nWARNING: Your password has been breached {self.get_times_pwned()} times!")
            elif self.get_times_pwned() == None:
                feedback += (f"\n\nThe Have I Been Pwned API cannot be accessed. To determine whether your password has been breached, please try again later.")
            else:
                feedback += (f"\n\nYour password has not been breached.")
            
            #Check if any other issues are present

            #Length
            if problems[0] < 50:
                feedback += "\n\nYour password is very short. It could be strengthened greatly by making it longer."
            elif problems[0] < 100:
                feedback += "\n\nYour password is moderately long, but would be stronger if it was slightly longer."
            
            #Character variety
            if problems[1] < 100:

                if problems[1] < 50:
                    feedback += "\n\nYou do not have a very large variety of characters in your password. "
                else:
                    feedback += "\n\nYou could strengthen your password by adding a few more different characters. "

                #Get all types of characters and their corresponding names
                characterTypes = {"special character":self._specialCount,"number":self._numberCount,"uppercase letter":self._upperCount,"lowercase letter":self._lowerCount}
                
                

                #Check each type of character

                unusedTypes = []#Stores types of character that are not used

                singleUseTypes = []#Stores types of character that are only used once

                for characterType in characterTypes:
                    if characterTypes[characterType] <= 0:
                        unusedTypes.append(characterType)

                    elif characterTypes[characterType] == 1:
                        singleUseTypes.append(characterType)
                
                if len(unusedTypes) > 0:

                    if len(unusedTypes) > 1:
                        #Add grammar between characters
                        unusedString = "s, ".join(unusedTypes[:len(unusedTypes)-1:]) + "s or " + unusedTypes[len(unusedTypes)-1]
                    else:
                        unusedString = unusedTypes[0]
                    
                    feedback += f"You have not used any {unusedString}s. "

                if len(singleUseTypes) > 0:

                    if len(singleUseTypes) > 1:
                        #Add grammar between characters
                        singleUsedString = ", ".join(singleUseTypes[:len(singleUseTypes)-1:]) + " and " + singleUseTypes[len(singleUseTypes)-1]
                    else:
                        singleUsedString = singleUseTypes[0]
                    
                    feedback += f"You have only used one {singleUsedString}. "

            #Rarity
            if problems[2] < 100:
                feedback += f"\n\nYour password is very commonly used. Try to create a more unique password."
                    
            

        return feedback



    #Getter methods
    def get_times_pwned(self):
        return self._timesPwned
    
    def get_score(self):
        return self._score
    
    def get_length_score(self):
        return self._length_score
    
    def get_character_score(self):
        return self._character_score
    
    def get_rarity_score(self):
        return self._rarity_score
    
    def get_pwned_score(self):
        return self._pwned_score

    def get_rating(self):
        return self._current_rating

    #Setter methods
    def update_password(self,new_password):
        self._password = new_password