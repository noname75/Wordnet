from wtforms import Form, TextField, validators

class QuestionnaireForm(Form):
    response = TextField('', [
        validators.Length(min=2, max=20, message='پاسخ باید حداقل ۲ کاراکتر و حداکثر ۲۰ کاراکتر باشد.')])

