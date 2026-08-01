from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import SubmitField, TextAreaField
from wtforms.fields import URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from .constants import CUSTOM_ID_MAX_LENGTH, REGEX


class LinkForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = TextAreaField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=CUSTOM_ID_MAX_LENGTH),
            Regexp(
                REGEX,
                message='Недопустимый формат короткой ссылки.'
            )
        ]
    )
    submit = SubmitField('Создать')


class FilesForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[FileRequired()]
    )
    submit = SubmitField('Загрузить')
