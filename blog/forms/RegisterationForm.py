from wtforms.validators import ValidationError, NumberRange
from wtforms import Form, TextField, PasswordField, IntegerField, validators
from blog.models.db_config import *

def existUsername(form, field):
    if User(username=field.data).getUser():
        raise ValidationError('کاربری با این نام کاربری وجود دارد.')

class RegistrationForm(Form):
    firstname = TextField('نام', [validators.Length(min=3, max=25, message='نام باید حداقل ۳ کاراکتر و حداکثر ۲۵ کاراکتر باشد.')])
    # lastname = TextField('نام خانوادگی', [validators.Length(min=3, max=25, message='نام خانوادگی باید حداقل ۳ کاراکتر و حداکثر ۲۵ کاراکتر باشد.')])
    birthyear = IntegerField(
        'سال تولد',
        validators=[NumberRange(
            min=1300,
            max=1395,
            message='سال تولد باید عددی بین ۱۳۰۰ و ۱۳۹۵ باشد.'
        )]
    )
    username = TextField('نام کاربری', [existUsername, validators.Length(min=3, max=25, message='نام کاربری باید حداقل ۳ کاراکتر و حداکثر ۲۵ کاراکتر باشد.')])
    email = TextField('ایمیل', [validators.Email(message='ایمیل معتبر نیست.')])
    password = PasswordField('رمز ورود', [validators.Required(message='وارد کردن پسورد الزامی است.')])
    confirm = PasswordField('تکرار رمز عبور' , [validators.EqualTo('password', message='تکرار رمز عبور صحیح نیست.')])


