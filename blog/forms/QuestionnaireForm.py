from wtforms.validators import ValidationError
from wtforms import Form, TextField, PasswordField, validators
from wtforms.fields.core import SelectField

class QuestionnaireForm(Form):
        response = TextField([validators.Length(min=2, max=20,message='پاسخ باید حداقل ۲ کاراکتر و حداکثر ۲۰ کاراکتر باشد.')])

