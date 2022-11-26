import re

from flask import jsonify, request

from . import app, db, localhost
from .error_handlers import InvalidAPIUsage
from .models import URL_map


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_opinion(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.to_dict()['url']}), 200


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
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
            not re.match(r'^[aA-zZ0-9]+$', short_url)
    )
    ):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if (
            short_url and
            URL_map.query.filter_by(short=short_url).first() is not None
    ):
        raise InvalidAPIUsage(f'Имя "{short_url}" уже занято.')
    url = URL_map()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    dict_to_return = url.to_dict()
    dict_to_return['short_link'] = localhost + dict_to_return['short_link']
    return jsonify(dict_to_return), 201
