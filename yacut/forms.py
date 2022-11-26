from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError

from yacut.models import URL_map


class Unique(object):
    def __init__(self, model, field):
        self.model = model
        self.field = field

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(f'Имя {field.data} уже занято!')


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(0, 16), Optional(),
            Regexp(
                '^[aA-zZ0-9]+$',
                message='Короткая запись должна включать в себя буквы и/или цифры'
            ),
            Unique(URL_map, URL_map.short)])
    submit = SubmitField('Создать')