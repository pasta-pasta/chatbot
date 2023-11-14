# ОСНОВНОЙ МОДУЛЬ ПРИЛОЖЕНИЯ
# Здесь происходит взаимодействие с flask, прием запросов
# Все полученные данные переводятся в формат .json и передаются в модуль handler
import json
import sys

import flask
import requests
from flask import Response
sys.path.append('../defence')
import main
# Стартовый блок
app = flask.Flask(__name__)


# Запросы на корневой адрес (GET, OPTIONS)
@app.route('/', methods=['GET', 'OPTIONS'])
def get_request():
    return 'Alive!'


# Запросы на корневой адрес (POST)
@app.route('/', methods=['POST'])
def post_request():
    data = flask.request.get_json()# Распаковываем пейлоад
    print(data)
    main.handle(data)
    return 'ok'

