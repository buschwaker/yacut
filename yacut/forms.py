from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError

from . import SHORT_URL_SIZE_MAX, SHORT_URL_SIZE_MIN, short_url_regex
from yacut.models import URL_map


class Unique(object):
    def __init__(self, model, field, *args, **kwargs):
        self.model = model
        self.field = field
        self.args = args
        self.kwargs = kwargs

    def __call__(self, form, field):
        self.param = str(self.field).split('.')[1]
        check = self.model.get_url_by_param(**{self.param: field.data})
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
            Length(SHORT_URL_SIZE_MIN, SHORT_URL_SIZE_MAX), Optional(),
            Regexp(
                short_url_regex,
                message='Короткая запись должна включать в себя буквы и/или цифры'
            ),
            Unique(URL_map, URL_map.short)])
    submit = SubmitField('Создать')
