import gooeypie as gp
from passwordchecker import PasswordChecker

#Create app
app = gp.GooeyPieApp('Password Checker')
app.width = 400
app.height = 350
app.resizable_horizontal = False
app.resizable_vertical = False

#Create grid
app.set_grid(6,2)


#Define functions
#Update screen to display score
def on_password_submit(event):
    if passwordInput.text != "":
        #Update password checker, then display results
        passometer.update_password(passwordInput.text)

        scoreDisplay.value = passometer.combine_scores(1,1,1) #Weights to be adjusted

        feedbackText.text = f"""Length score: {passometer.score_length()}
Character Score: {passometer.score_characters()}
Rarity Score: {passometer.score_rarity()}
"""
        
        if passometer.timesPwned:
            feedbackText.text += (f"\nWARNING: Password has been breached {passometer.timesPwned} times!")
        
    else:
        #Do not check score of empty string
        scoreDisplay.value = 0
        feedbackText.text = f"""Length score:
Character Score:
Rarity Score:
"""
        
#Open subwindows
def open_help(event):
    helpWindow.show_on_top()

def open_about(event):
    aboutWindow.show_on_top()

def close_help(event):
    helpWindow.hide()

def close_about(event):
    aboutWindow.hide()

#Create subwindows
#Help
helpWindow = gp.Window(app, 'Help')
helpWindow.width = 400
helpWindow.height = 300
helpWindow.set_grid(3, 1)

#About
aboutWindow = gp.Window(app, 'About')
aboutWindow.width = 400
aboutWindow.height = 300
aboutWindow.set_grid(3, 1)

#Create widgets
#Title
title = gp.StyleLabel(app,"Pass-O-Meter")
title.font_name = "Comic Sans MS"
title.font_size = 20

#Password input
passwordLabel = gp.Label(app,"Enter Password:")
passwordInput = gp.Secret(app)
passwordSubmit = gp.Button(app,"Scan Password",on_password_submit)

#Score and feedback
scoreDisplay = gp.Progressbar(app,'determinate')
feedbackText = gp.Label(app, "")

#Add text to feedback
feedbackText.text = f"""Length score:
Character Score:
Rarity Score:
"""

#Add help/about buttons
btnContainer = gp.Container(app)
btnContainer.set_grid(1,2)

helpBtn = gp.Button(btnContainer,"Help",open_help)
aboutBtn = gp.Button(btnContainer,"About",open_about)

#Subwindow widgets
#Help
helpTitle = gp.StyleLabel(helpWindow,"Help")
helpTitle.font_size = 20
helpTitle.font_name = "Times New Roman"

helpText = gp.Label(helpWindow, "...")

helpClose = gp.Button(helpWindow, "Close",close_help)

#About
aboutTitle = gp.StyleLabel(aboutWindow,"About")
aboutTitle.font_size = 20
aboutTitle.font_name = "Times New Roman"

aboutText = gp.Label(aboutWindow, "...")

aboutClose = gp.Button(aboutWindow, "Close",close_about)

#Add widgets to grid
app.add(title,1,1,align="center",column_span=2)

app.add(passwordLabel,2,1,align="center")
app.add(passwordInput,2,2,fill=True)
app.add(passwordSubmit,3,1,fill=True,column_span=2)

app.add(scoreDisplay,4,1,fill=True,column_span=2)
app.add(feedbackText,5,1,fill=True,column_span=2)
app.add(btnContainer,6,2,fill=True)

btnContainer.add(helpBtn,1,1,fill=True)
btnContainer.add(aboutBtn,1,2,fill=True)

helpWindow.add(helpTitle,1,1,fill=True)
helpWindow.add(helpText,2,1,fill=True,stretch=True)
helpWindow.add(helpClose,3,1,valign="bottom")

aboutWindow.add(aboutTitle,1,1,fill=True)
aboutWindow.add(aboutText,2,1,fill=True,stretch=True)
aboutWindow.add(aboutClose,3,1,valign="bottom")



#Instatiate PasswordChecker class
passometer = PasswordChecker(passwordInput.text)

app.run()