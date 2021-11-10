import argparse
import datetime
import os
import pprint
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

parser = argparse.ArgumentParser()
parser.add_argument('-p','--path_to_file', type=str, default=f'{os.getcwd()}/wine.xls')
args = parser.parse_args()
path_to_file = args.path_to_file

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


drinks = pandas.read_excel(
    path_to_file,
    sheet_name='Лист1',
    usecols=['Категория','Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
).fillna('').to_dict(orient='records')
drink_types = sorted({drink['Категория'] for drink in drinks})
sorted_drinks = defaultdict(list)
for drink in drink_types:
    sorted_drinks[drink] = list(filter(lambda x: x['Категория'] == drink, drinks))
pp = pprint.PrettyPrinter()
pp.pprint(sorted_drinks)

rendered_page = template.render(
    years=datetime.datetime.now().year - 1920,
    drinks=sorted_drinks
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
