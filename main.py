from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime 
import pandas
import pprint
from collections import defaultdict

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


excel_data_df = pandas.read_excel(
    'wine3.xls',
    sheet_name='Лист1',
    usecols=['Категория','Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
).fillna('')
drinks = excel_data_df.to_dict(orient='records')
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
