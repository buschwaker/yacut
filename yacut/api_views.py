from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from . import app, localhost
from .error_handlers import InvalidAPIUsage
from .exceptions import FieldError, ShortUrlGenerateError
from .models import URL_map


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_opinion(short_id):
    url = URL_map.get_url_by_param(short=short_id)
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.to_dict()['url']}), 200


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    try:
        URL_map.validate(data)
        url = URL_map.deserialize_create(data)
    except (FieldError, SQLAlchemyError, ShortUrlGenerateError) as error:
        raise InvalidAPIUsage(str(error))
    dict_to_return = url.to_dict()
    dict_to_return['short_link'] = localhost + dict_to_return['short_link']
    return jsonify(dict_to_return), 201
