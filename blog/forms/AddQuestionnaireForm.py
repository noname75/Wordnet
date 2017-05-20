from wtforms.validators import ValidationError
from wtforms import Form, TextField, TextAreaField, validators
from blog.models.db_config import *


def existSubejct(form, field):
    if Questionnaire(subject=field.data).getQuestionnaire():
        raise ValidationError('پرسش‌نامه‌ای با این نام وجود دارد.')


class AddQuestionnaireForm(Form):
    subject = TextField('نام', [existSubejct, validators.Length(min=3, max=25,
                                                                message='نام باید حداقل ۳ کاراکتر و حداکثر ۲۵ کاراکتر باشد.')])
    moreInfo = TextAreaField('توضیحات', [validators.Required(message='وارد کردن توضیحات الزامی است.')])
    stimuli = TextAreaField('واژه‌ها', [validators.Required(message='وارد کردن واژه‌ها الزامی است.')])
