from app import app
import json
from flask import render_template, request, jsonify
import hashlib
from datetime import datetime, timedelta
from PIL import Image
import base64
from io import BytesIO
import math
import pytz

date = (datetime.now(pytz.timezone('America/Sao_Paulo')) - timedelta(days=0)).strftime('%d/%m/%Y')


@app.route('/correct-answer', methods=['GET'])
def correct_answer():
    countries = listar_paises('all')
    correct_code = item_aleatorio()[0]
    correct_answer = [x['clean_name'] for x in countries if x['code'] == correct_code][0]

    img = Image.open(f'flags/{correct_code}.png')
    img64 = generate_base64(img)

    time_next = ((datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                 - datetime.now(pytz.timezone('America/Sao_Paulo')))

    time_remaining = {
        'hours': time_next.seconds // 3600,
        'minutes': (time_next.seconds % 3600) // 60,
        'seconds': time_next.seconds % 60
    }
    return jsonify(answer=correct_answer, flag=img64, time_remaining=time_remaining)


@app.route('/', methods=['GET'])
@app.route('/<int:random_day>', methods=['GET'])
def index(random_day=0):
    desafio = listar_paises()
    img = Image.new("RGB", (640, 480), color='#1e1e1e')

    image = generate_base64(img)

    return render_template('index.html', img_str=image, countries=desafio, date=date)


@app.route('/guess', methods=['POST'])
def desafio():
    guess = request.form['country']
    current_flag = request.form['current_flag'].replace('data:image/png;base64, ', '')
    country_code = get_country_info(guess)

    if not country_code:
        return jsonify(error='Invalid country'), 404

    comparar = compare_country(country_code, current_flag)

    return jsonify(result=comparar), 200


@app.route('/initial_flag/<countries>', methods=['GET'])
def initial_flag(countries):
    countries_list = countries.split(',')

    img = Image.new("RGB", (640, 480), color='#1e1e1e')
    for country in countries_list:
        img = generate_flag(country, img)

    return jsonify(flag=generate_base64(img)), 200


def compare_country(guess, flag):
    correct = item_aleatorio()
    correct_image = Image.open(f'flags/{correct[0]}.png').load()
    guess_image = Image.open(f'flags/{guess["code"]}.png').load()

    image = Image.open(BytesIO(base64.b64decode(flag)))
    contador = 0

    for i in range(640):
        for j in range(480):
            if distance(guess_image[i, j], correct_image[i, j]) < 75:
                image.putpixel((i, j), correct_image[i, j])
                contador += 1

    correct_percent = contador * 100 / (640 * 480)
    my_flag = generate_base64(image)
    guess64 = generate_base64(Image.open(f'flags/{guess["code"]}.png'))

    return {
        'country': guess['clean_name'],
        'correct_percent': float(f'{correct_percent:.2f}'),
        'flag_base_64': my_flag,
        'guess64': guess64,
        'date': correct[1],
        'correct': guess['code'] == correct[0]
    }


def get_country_info(country_name):
    countries = listar_paises('all')

    country_info = None
    for country in countries:
        if country['clean_name'].lower() == country_name.lower():
            country_info = country
            break

    return country_info


def item_aleatorio():
    countries = listar_paises('all')
    index = int(hashlib.sha256(str(date).encode('utf-8')).hexdigest(), 16) % len(countries)

    return countries[index]['code'], date


def listar_paises(goal='clean_name'):
    with open('countries.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)

    if goal == 'clean_name':
        return [country['clean_name'] for country in countries]
    else:
        return countries


def generate_base64(img):
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def distance(color1, color2):
    if len(color1) == 3:
        r1, g1, b1 = color1
    else:
        r1, g1, b1, _ = color1

    if len(color2) == 3:
        r2, g2, b2 = color2
    else:
        r2, g2, b2, _ = color2

    return math.sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)


def generate_flag(guess, current):
    correct = item_aleatorio()
    guess_code = get_country_info(guess)
    if not guess_code:
        return current

    correct_image = Image.open(f'flags/{correct[0]}.png').load()
    guess_image = Image.open(f'flags/{guess_code["code"]}.png').load()

    for i in range(640):
        for j in range(480):
            if distance(guess_image[i, j], correct_image[i, j]) < 75:
                current.putpixel((i, j), correct_image[i, j])

    return current
