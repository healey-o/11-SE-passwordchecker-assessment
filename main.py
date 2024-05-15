import gooeypie as gp
from passwordchecker import PasswordChecker

#Create app
app = gp.GooeyPieApp('Password Checker')
app.width = 400
app.height = 200

#Create grid
app.set_grid(3,2)

#Define functions
def on_text_change(event):
    feedbackText.text = f"Your password is {str(len(passwordInput.text))} characters long."
    securityScorer.update_password(passwordInput.text)
    scoreDisplay.value = securityScorer.score_length()

#Create widgets
passwordLabel = gp.Label(app,"Enter Password:")
passwordInput = gp.Secret(app)
scoreDisplay = gp.Progressbar(app,'determinate')
feedbackText = gp.Label(app, "")

#Add widgets to grid
app.add(passwordLabel,1,1,align="center")
app.add(passwordInput,1,2,fill=True)
app.add(scoreDisplay,2,1,fill=True,column_span=2)
app.add(feedbackText,3,1,fill=True,column_span=2)

passwordInput.add_event_listener('change', on_text_change)

securityScorer = PasswordChecker(passwordInput)

app.run()