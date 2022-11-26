from datetime import datetime
import re
import random

from yacut import db, SHORT_URL_SYMBOLS, SHORT_URL_SIZE_GENERATE, short_url_regex
from yacut.error_handlers import InvalidAPIUsage


def get_unique_short_id():
    short_id = False
    url = True
    while url:
        characters = ''.join(random.sample(SHORT_URL_SYMBOLS, len(SHORT_URL_SYMBOLS)))
        short_id = characters[:SHORT_URL_SIZE_GENERATE]
        url = URL_map.get_url_by_param(short=short_id)
    return short_id


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
            raise InvalidAPIUsage('Отсутствует тело запроса')
        if not data.get('url'):
            raise InvalidAPIUsage('\"url\" является обязательным полем!')
        short_url = data.get('custom_id')
        if short_url == '':
            short_url = None
            del data['custom_id']
        if (short_url and (
                not len(short_url) <= 16 or
                not re.match(short_url_regex, short_url)
        )
        ):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if (
                short_url and
                URL_map.get_url_by_param(short=short_url) is not None
        ):
            raise InvalidAPIUsage(f'Имя "{short_url}" уже занято.')

    @staticmethod
    def create(obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def to_dict(self):
        return dict(
            short_link=self.short,
            url=self.original,
        )

    def from_dict(self, data):
        self.original = data.get('url')
        self.short = data.get('custom_id')
