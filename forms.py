from wtforms import Form, TextField

class NameForm(Form):
    name = TextField("Enter your name")