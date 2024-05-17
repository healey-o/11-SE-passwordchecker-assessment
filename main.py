import gooeypie as gp
from passwordchecker import PasswordChecker

#Create app
app = gp.GooeyPieApp('Password Checker')
app.width = 400
app.height = 300

#Create grid
app.set_grid(4,2)

#Define functions
def on_text_change(event):
    passometer.update_password(passwordInput.text)
    scoreDisplay.value = passometer.combine_scores(30,30,30) #Weights to be adjusted
    feedbackText.text = f"""
    Length score: {passometer.score_length()}
    Character Score: {passometer.score_characters()}
    Rarity Score: {passometer.score_rarity()}
    """

#Create widgets
#Title
title = gp.StyleLabel(app,"Pass-O-Meter")
title.font_name = "Comic Sans MS"
title.font_size = 20

#Password input
passwordLabel = gp.Label(app,"Enter Password:")
passwordInput = gp.Secret(app)
#Score
scoreDisplay = gp.Progressbar(app,'determinate')
feedbackText = gp.Label(app, "")

#Add widgets to grid
app.add(title,1,1,align="center",column_span=2)
app.add(passwordLabel,2,1,align="center")
app.add(passwordInput,2,2,fill=True)
app.add(scoreDisplay,3,1,fill=True,column_span=2)
app.add(feedbackText,4,1,fill=True,column_span=2)

#Event listeners
passwordInput.add_event_listener('change', on_text_change)

#Instatiate PasswordChecker class
passometer = PasswordChecker(passwordInput.text)

app.run()