from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server
import pathlib
import json
import math


def on_reload():
    with open('description.json', 'r', encoding="utf-8") as my_file:
        parsed_books_json = my_file.read()

    parsed_books = json.loads(parsed_books_json)
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    pages_folder = 'pages'

    amount_books_per_page = 20
    pages_nambers = []
    pages = math.ceil(len(parsed_books) / amount_books_per_page)
    for page in range(1, pages + 1):
        pages_nambers.append(page)
    for number, books_per_page in enumerate(list(chunked(parsed_books, amount_books_per_page)), 1):
        rendered_page = template.render(
            books_per_page=list(chunked(books_per_page, 2)),
            pages_nambers=pages_nambers,
            current_page=number,
        )
        pathlib.Path(pages_folder).mkdir(parents=True, exist_ok=True)
        with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)
on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')


