import re

from flask import jsonify, request, url_for
from http import HTTPStatus

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id, redirect_view
from .constants import CUSTOM_ID_MAX_LENGTH, REGEX


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > CUSTOM_ID_MAX_LENGTH:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if not re.fullmatch(
            REGEX,
            custom_id
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URLMap.query.filter_by(
            short=custom_id
        ).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        short = custom_id
    else:
        short = get_unique_short_id()
    urlmap = URLMap(original=data['url'], short=short)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(
        {
            'url': urlmap.original,
            'short_link': url_for(
                'redirect_view',
                short=urlmap.short,
                _external=True
            )
        }
    ), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original})
