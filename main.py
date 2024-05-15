import gooeypie as gp
from passwordchecker import PasswordChecker

#Create app
app = gp.GooeyPieApp('Password Checker')
app.width = 400
app.height = 200

#Create grid
app.set_grid(4,2)

#Define functions
def on_text_change(event):
    feedbackText.text = f"Your password is {str(len(passwordInput.text))} characters long."
    passometer.update_password(passwordInput.text)
    scoreDisplay.value = passometer.score_length()

#Create widgets
title = gp.StyleLabel(app,"Pass-O-Meter")
title.font_name = "Comic Sans MS"
title.font_size = 20

passwordLabel = gp.Label(app,"Enter Password:")
passwordInput = gp.Secret(app)
scoreDisplay = gp.Progressbar(app,'determinate')
feedbackText = gp.Label(app, "")

#Add widgets to grid
app.add(title,1,1,align="center",column_span=2)
app.add(passwordLabel,2,1,align="center")
app.add(passwordInput,2,2,fill=True)
app.add(scoreDisplay,3,1,fill=True,column_span=2)
app.add(feedbackText,4,1,fill=True,column_span=2)

passwordInput.add_event_listener('change', on_text_change)

passometer = PasswordChecker(passwordInput)

app.run()