from wtforms.validators import ValidationError
from wtforms import Form, TextField, PasswordField, validators
from wtforms.fields.core import SelectField
from blog.models.db_config import *
from passlib.hash import bcrypt

def existUsername(form, field):
    if User(username=field.data).getUser():
        raise ValidationError('کاربری با این نام کاربری وجود دارد.')

# def varifyPassword(form, field):
#     if not bcrypt.verify(field, User.getPassword(form.username.data)):
#         raise ValidationError('نام کاربری یا رمز ورود صحیح نیست.')



# class LoginForm(Form):
#     username = TextField('نام کاربری', [validators.required(message='نام کاربری را وارد نمایید.')])
#     password = PasswordField('رمز ورود', [validators.required(message='رمز عبور را وارد نمایید.'), varifyPassword])


class RegistrationForm(Form):
    firstname = TextField('نام', [validators.Length(min=3, max=25, message='نام باید حداقل ۳ کاراکتر و حداکثر ۲۵ کاراکتر باشد.')])
    lastname = TextField('نام خانوادگی', [validators.Length(min=3, max=25, message='نام خانوادگی باید حداقل ۳ کاراکتر و حداکثر ۲۵ کاراکتر باشد.')])
    username = TextField('نام کاربری', [existUsername, validators.Length(min=3, max=25, message='نام کاربری باید حداقل ۳ کاراکتر و حداکثر ۲۵ کاراکتر باشد.')])
    email = TextField('ایمیل', [validators.Email(message='ایمیل معتبر نیست.')])
    password = PasswordField('رمز ورود', [validators.Required(message='وارد کردن پسورد الزامی است.')])
    confirm = PasswordField('تکرار رمز عبور' , [validators.EqualTo('password', message='تکرار رمز عبور صحیح نیست.')])


class ResponseForm(Form):
        response = TextField([validators.Length(min=2, max=20,message='پاسخ باید حداقل ۲ کاراکتر و حداکثر ۲۰ کاراکتر باشد.')])

