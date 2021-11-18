import argparse
import datetime
import os
import collections
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

STORE_LAUNCH_YEAR = 1920

parser = argparse.ArgumentParser()
parser.add_argument('-p','--path_to_file', type=str, default=f'{os.getcwd()}/wine.xls')
args = parser.parse_args()
path_to_file = args.path_to_file

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


catalog = pandas.read_excel(
    path_to_file,
    sheet_name='Лист1',
    usecols=['Категория','Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
).fillna('').to_dict(orient='records')
drinks_by_categories = collections.defaultdict(list)
for product in catalog:
    drinks_by_categories[product['Категория']].append(product)

rendered_page = template.render(
    years=datetime.datetime.now().year - STORE_LAUNCH_YEAR,
    drinks=drinks_by_categories
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
