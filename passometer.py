import gooeypie as gp
import custom_widgets as cw
from passwordchecker import PasswordChecker
from tkinter import ttk


#Create app
app = gp.GooeyPieApp('Password Checker')
app.width = 500
app.height = 425
app.resizable_horizontal = False
app.resizable_vertical = False


#Create grid
app.set_grid(6,2)
app.set_column_weights(3,1)
app.set_row_weights(0,0,0,0,1,0)

#Set tkinter theme
style = ttk.Style()



#Instatiate PasswordChecker class
passometer = PasswordChecker("")


#Define functions
#Update screen to display score
def on_password_submit(event):
    if passwordInput.text != "":
        #Update password checker, then display results
        passometer.update_password(passwordInput.text)

        #Calculates all scores
        passometer.score_length()
        passometer.score_characters()
        passometer.score_rarity()
        passometer.score_pwned()
        #Calculate final score
        passometer.combine_scores(4,5,1)

        passometer.rate_password()

        scoreDisplay.value = passometer.get_score()

        feedbackText.text = passometer.generate_feedback()
        
    else:
        #Do not check score of empty string
        scoreDisplay.value = 0
        feedbackText.text = "Please enter a password to recieve feedback."

#Toggle password masking
def toggle_password_mask(event):
    passwordInput.toggle()
    if passwordVisibiltyBtn.text == "Show":
        passwordVisibiltyBtn.text = "Hide"
    else:
        passwordVisibiltyBtn.text = "Show"


      
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
helpWindow.set_row_weights(0,1,0)

#About
aboutWindow = gp.Window(app, 'About')
aboutWindow.width = 400
aboutWindow.height = 300
aboutWindow.set_grid(3, 1)
aboutWindow.set_row_weights(0,1,0)

#Create widgets
#Title
title = gp.StyleLabel(app,"Pass-O-Meter")
title.font_name = "Comic Sans MS"
title.font_size = 20

#Password input area
passwordContainer = gp.Container(app)
passwordContainer.set_grid(1,3)
passwordContainer.set_column_weights(0,1,0)

passwordLabel = gp.Label(passwordContainer,"Enter Password:")
passwordInput = gp.Secret(passwordContainer)
passwordVisibiltyBtn = gp.Button(passwordContainer,"Show",toggle_password_mask)#Toggles password masking

passwordSubmit = gp.Button(app,"Scan Password",on_password_submit)

#Score and feedback
scoreDisplay = cw.ColourProgressbar(app,'determinate')
feedbackText = gp.Label(app, "")

#Add text to feedback
feedbackText.text = "Please enter a password to recieve feedback."
feedbackText.width = 78
feedbackText.wrap = True

#Copy password
passwordCopyBtn = gp.Button(app,"Copy Password (Coming Soon)",None)
passwordCopyBtn.disabled = True

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

helpText = gp.Label(helpWindow, """Pass-O-Meter can score your password's security and give feedback based on the results.
Simply enter your password into the prompted textbox, and press [Scan Password] when ready.
The app will score your password and give feedback on how to improve it if necessary.""")


helpText.width = 78
helpText.wrap = True

helpClose = gp.Button(helpWindow, "Close",close_help)

#About
aboutTitle = gp.StyleLabel(aboutWindow,"About")
aboutTitle.font_size = 20
aboutTitle.font_name = "Times New Roman"

aboutText = gp.Label(aboutWindow, "Pass-O-Meter was developed by Oliver Healey and it has been released using a MIT License. It was created for a Year 11 Software Engineering assessment task, using Python. The app was constructed using the gooeypie GUI library, as well as a pyhibp, a python library that allows access to the Have I Been Pwned? library.")
aboutText.width = 78
aboutText.wrap = True

aboutClose = gp.Button(aboutWindow, "Close",close_about)

#Add widgets to grid
app.add(title,1,1,align="center",column_span=2)

app.add(passwordContainer,2,1,column_span=2,fill=True)

passwordContainer.add(passwordLabel,1,1,align="center",stretch=True)
passwordContainer.add(passwordInput,1,2,fill=True,stretch=True)
passwordContainer.add(passwordVisibiltyBtn,1,3)


app.add(passwordSubmit,3,1,fill=True,column_span=2,stretch=True)

app.add(scoreDisplay,4,1,fill=True,column_span=2)
app.add(feedbackText,5,1,fill=True,column_span=2)

app.add(passwordCopyBtn,6,1,fill=True)

app.add(btnContainer,6,2,fill=True)

btnContainer.add(helpBtn,1,1,fill=True)
btnContainer.add(aboutBtn,1,2,fill=True)

helpWindow.add(helpTitle,1,1,fill=True)
helpWindow.add(helpText,2,1,fill=True)
helpWindow.add(helpClose,3,1,valign="bottom",align="center")

aboutWindow.add(aboutTitle,1,1,fill=True)
aboutWindow.add(aboutText,2,1,fill=True)
aboutWindow.add(aboutClose,3,1,valign="bottom",align="center")


app.run()