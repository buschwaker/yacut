from flask import jsonify, request

from . import app, localhost
from .error_handlers import InvalidAPIUsage
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
    URL_map.validate(data)
    url = URL_map()
    url.from_dict(data)
    url = URL_map.create(url)
    dict_to_return = url.to_dict()
    dict_to_return['short_link'] = localhost + dict_to_return['short_link']
    return jsonify(dict_to_return), 201
