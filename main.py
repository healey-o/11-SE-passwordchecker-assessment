import gooeypie as gp

#Create app
app = gp.GooeyPieApp('Password Checker')
app.width = 400
app.height = 500

#Create grid
app.set_grid(5,2)


#Create widgets
password_labelcontainer = gp.Container(app)
password_labelcontainer.set_grid(1,2)

password_label = gp.Label(app,"Enter Password:")
password_input = gp.Secret(app)

#Add widgets to grid
app.add(password_labelcontainer,1,1)

password_labelcontainer.add(password_label,1,1,align="center")
password_labelcontainer.add(password_input,1,2,fill=True)


app.run()