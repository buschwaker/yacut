from datetime import datetime
import random
import re


from yacut import (
    db, GET_SHORT_ID_TRIALS, SHORT_URL_SYMBOLS,
    SHORT_URL_SIZE_GENERATE, SHORT_URL_SIZE_MAX, short_url_regex
)
from yacut.exceptions import FieldError, ShortUrlGenerateError


def get_unique_short_id():
    for _ in range(GET_SHORT_ID_TRIALS):
        short_id = ''.join(
            random.sample(SHORT_URL_SYMBOLS, SHORT_URL_SIZE_GENERATE)
        )
        if URL_map.get_url_by_param(short=short_id) is None:
            return short_id
    raise ShortUrlGenerateError('Не удалось создать короткую ссылку!')


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(), unique=True, default=get_unique_short_id)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_url_by_param(**kwargs):
        url = URL_map.query.filter_by(**kwargs).first()
        return url

    @staticmethod
    def validate(data):
        if data is None:
            raise FieldError('Отсутствует тело запроса')
        if not data.get('url'):
            raise FieldError('\"url\" является обязательным полем!')
        short_url = data.get('custom_id')
        if short_url == '':
            short_url = None
            del data['custom_id']
        if (short_url and (
                not len(short_url) <= SHORT_URL_SIZE_MAX or
                not re.match(short_url_regex, short_url)
        )
        ):
            raise FieldError('Указано недопустимое имя для короткой ссылки')
        if (
                short_url and
                URL_map.get_url_by_param(short=short_url) is not None
        ):
            raise FieldError(f'Имя "{short_url}" уже занято.')

    @staticmethod
    def create(**kwargs):
        url = URL_map(**kwargs)
        db.session.add(url)
        db.session.commit()
        return url

    @staticmethod
    def deserialize_create(data):
        url = URL_map()
        url.from_dict(data)
        db.session.add(url)
        db.session.commit()
        return url

    def to_dict(self):
        return dict(
            short_link=self.short,
            url=self.original,
        )

    def from_dict(self, data):
        self.original = data.get('url')
        self.short = data.get('custom_id')
