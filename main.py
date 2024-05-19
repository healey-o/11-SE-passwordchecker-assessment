import gooeypie as gp
from passwordchecker import PasswordChecker

#Create app
app = gp.GooeyPieApp('Password Checker')
app.width = 400
app.height = 300
app.resizable_horizontal = False
app.resizable_vertical = False

#Create grid
app.set_grid(5,2)

#Define functions
def on_text_change(event):
    if passwordInput.text != "":
        passometer.update_password(passwordInput.text)
        scoreDisplay.value = passometer.combine_scores(1,1,1) #Weights to be adjusted
        feedbackText.text = f"""Length score: {passometer.score_length()}
Character Score: {passometer.score_characters()}
Rarity Score: {passometer.score_rarity()}"""
        
    else:
        #Do not check score of empty string
        scoreDisplay.value = 0
        feedbackText.text = f"""Length score:
Character Score:
Rarity Score:"""


#Create widgets
#Title
title = gp.StyleLabel(app,"Pass-O-Meter")
title.font_name = "Comic Sans MS"
title.font_size = 20

#Password input
passwordLabel = gp.Label(app,"Enter Password:")
passwordInput = gp.Secret(app)

#Score and feedback
scoreDisplay = gp.Progressbar(app,'determinate')
feedbackText = gp.Label(app, "")

#Add text to feedback
feedbackText.text = f"""Length score:
Character Score:
Rarity Score:"""

#Add help/about buttons
btnContainer = gp.Container(app)
btnContainer.set_grid(1,2)

helpBtn = gp.Button(btnContainer,"Help",None)
aboutBtn = gp.Button(btnContainer,"About",None)

#Add widgets to grid
app.add(title,1,1,align="center",column_span=2)
app.add(passwordLabel,2,1,align="center")
app.add(passwordInput,2,2,fill=True)
app.add(scoreDisplay,3,1,fill=True,column_span=2)
app.add(feedbackText,4,1,fill=True,column_span=2)
app.add(btnContainer,5,2,fill=True)

btnContainer.add(helpBtn,1,1,fill=True)
btnContainer.add(aboutBtn,1,2,fill=True)

#Event listeners
passwordInput.add_event_listener('change', on_text_change)



#Instatiate PasswordChecker class
passometer = PasswordChecker(passwordInput.text)

app.run()