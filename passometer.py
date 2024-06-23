import gooeypie as gp
import custom_widgets as cw
from passwordchecker import PasswordChecker
from tkinter import ttk
import random
import platform

pyperclipInstalled = True

try:
    import pyperclip
except ImportError:
    pyperclipInstalled = False


#Prevent explosions on a Mac - some gooeypie features behave... differently
if platform.system() == "Darwin":
    everythingIsBreaking = True
else:
    everythingIsBreaking = False



#Create app
app = gp.GooeyPieApp('Password Checker')

#Fit everything in window based on OS- Mac has larger default text size
if everythingIsBreaking:
    app.width = 600
else:
    app.width = 500


app.height = 500
app.resizable_horizontal = False
app.resizable_vertical = False
app.set_icon("logo_32.png")


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
def OnPasswordSubmit(event):
    if passwordInput.text != "":
        #Update password checker, then display results
        passometer.update_password(passwordInput.text)

        #Calculates all scores
        passometer.score_length()
        passometer.score_characters()
        passometer.score_rarity()
        passometer.score_pwned()
        #Calculate final score
        passometer.combine_scores(4,3,1)

        passometer.rate_password()

        scoreDisplay.value = passometer.get_score()

        feedbackText.text = passometer.generate_feedback()

        if pyperclipInstalled:
            if passometer.get_score() >= 80:
                passwordCopyBtn.text = "Copy Password"
                passwordCopyBtn.disabled = False
            else:
                passwordCopyBtn.text = "Password Too Weak to Copy"
                passwordCopyBtn.disabled = True
            
        
    else:
        #Do not check score of empty string
        scoreDisplay.value = 0
        feedbackText.text = "Please enter a password to recieve feedback."

        if pyperclipInstalled:
            passwordCopyBtn.text = "Enter Password to Copy"
            passwordCopyBtn.disabled = True

#Toggle password masking
def TogglePasswordMask(event):
    passwordInput.toggle()
    if passwordVisibiltyBtn.text == "Show":
        passwordVisibiltyBtn.text = "Hide"
    else:
        passwordVisibiltyBtn.text = "Show"


      
#Open subwindows
def OpenHelp(event):
    helpWindow.show_on_top()

def OpenAbout(event):
    aboutWindow.show_on_top()

def CloseHelp(event):
    helpWindow.hide()

def CloseAbout(event):
    aboutWindow.hide()



#Fancy Animation over title
def HoverTitle(event):
    colours = ['red','orange','green','blue','purple']
    title.color = random.choice(colours)
    title.font_style = 'italic'
    title.font_weight = 'bold'

def StopHover(event):

    if everythingIsBreaking: #Gooeypie's 'default' colour does not work on Mac
        title.color = 'black'
    else:
        title.color = 'default'
    
    title.font_style = 'normal'
    title.font_weight = 'normal'


#Copy password to clipboard - only runs if pyperclip installed
def CopyPassword(event):
    pyperclip.copy(passometer.get_password())

#Create subwindows
#Help
helpWindow = gp.Window(app, '❓ Help')
helpWindow.width = 400
helpWindow.height = 300
helpWindow.set_grid(3, 1)
helpWindow.set_row_weights(0,1,0)

#About
aboutWindow = gp.Window(app, 'ℹ️ About')
aboutWindow.width = 400
aboutWindow.height = 300
aboutWindow.set_grid(6, 1)
aboutWindow.set_row_weights(0,1,0,0,0,0)

#Create widgets
#Title
title = gp.StyleLabel(app,"Pass-O-Meter")
title.font_name = "Georgia"
title.font_size = 20

title.add_event_listener("mouse_over",HoverTitle)
title.add_event_listener("mouse_out",StopHover)

#Password input area
passwordContainer = gp.Container(app)
passwordContainer.set_grid(1,3)
passwordContainer.set_column_weights(0,1,0)

passwordLabel = gp.Label(passwordContainer,"Enter Password:")
passwordInput = gp.Secret(passwordContainer)
passwordVisibiltyBtn = gp.Button(passwordContainer,"Show",TogglePasswordMask)#Toggles password masking

passwordSubmit = gp.Button(app,"Scan Password",OnPasswordSubmit)

#Score and feedback
scoreDisplay = cw.ColourProgressbar(app,'determinate')
feedbackText = gp.StyleLabel(app, "")

#Add text to feedback
feedbackText.text = "Please enter a password to recieve feedback."

#Set font size to (try to) keep compatability between Mac and Windows
feedbackText.font_size = 10

#Windows and Mac's text wrap appears to work differently - The window in Mac does not automatically adjust to fit text
if everythingIsBreaking:
    feedbackText.width = 50
else:
    feedbackText.width = 70

feedbackText.wrap = True

#Copy password
if pyperclipInstalled:
    passwordCopyBtn = gp.Button(app,"Enter Password to Copy", CopyPassword)
else:
    passwordCopyBtn = gp.Button(app,"Install pyperclip to Copy", CopyPassword)
passwordCopyBtn.disabled = True

#Add help/about buttons
btnContainer = gp.Container(app)
btnContainer.set_grid(1,2)

helpBtn = gp.Button(btnContainer,"❓ Help",OpenHelp)
aboutBtn = gp.Button(btnContainer,"ℹ️ About",OpenAbout)

#Subwindow widgets
#Help
helpTitle = gp.StyleLabel(helpWindow,"Help")
helpTitle.font_size = 20
helpTitle.font_name = "Georgia"

helpText = gp.StyleLabel(helpWindow, """Pass-O-Meter can score your password's security and give feedback based on the results.
Simply enter your password into the prompted textbox, and press [Scan Password] when ready.
The app will score your password and give feedback on how to improve it if necessary, and allow you to copy the password once a high enough score has been reached.""")
helpText.font_size = 10

if everythingIsBreaking:
    helpText.width = 50
else:
    helpText.width = 70


helpText.width = 78
helpText.wrap = True

helpClose = gp.Button(helpWindow, "Close",CloseHelp)

#About
aboutTitle = gp.StyleLabel(aboutWindow,"About")
aboutTitle.font_size = 20
aboutTitle.font_name = "Georgia"

aboutText = gp.StyleLabel(aboutWindow, "Pass-O-Meter was developed by Oliver Healey and it has been released under a MIT License. It was created for a Year 11 Software Engineering assessment task, using Python. The app was constructed using the gooeypie GUI library, as well as a pyhibp, a python library that allows access to the Have I Been Pwned? library. The pyperclip library can ooptionally be used to allow easy copying of strong passwords.\nLinks:")
aboutText.font_size = 10

if everythingIsBreaking:
    aboutText.width = 50
else:
    aboutText.width = 70

aboutText.wrap = True

gooeypieLink = gp.Hyperlink(aboutWindow, "GooeyPie","https://www.gooeypie.dev/about")
pyhibpLink = gp.Hyperlink(aboutWindow, "pyHIBP (pyHave I Been Pwned)", "https://pypi.org/project/pyhibp/")
pyperclipLink = gp.Hyperlink(aboutWindow, "pyperclip", "https://pypi.org/project/pyperclip/")

aboutClose = gp.Button(aboutWindow, "Close",CloseAbout)

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
aboutWindow.add(gooeypieLink,3,1)
aboutWindow.add(pyhibpLink,4,1)
aboutWindow.add(pyperclipLink,5,1)
aboutWindow.add(aboutClose,6,1,valign="bottom",align="center") 


app.run()