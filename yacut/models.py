from datetime import datetime
import random
import string

from yacut import db


def get_unique_short_id():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(6))
    return password


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(), unique=True, default=get_unique_short_id)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            short_link=self.short,
            url=self.original,
        )

    def from_dict(self, data):
        for field in ['url', 'custom_id']:
            if field in data:
                if field == 'url':
                    name = 'original'
                else:
                    name = 'short'
                setattr(self, name, data[field])
