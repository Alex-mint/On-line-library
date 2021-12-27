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

    per_page_books = 20
    pages_amount = []
    pages = math.ceil(len(parsed_books) / per_page_books)
    for page in range(1, pages + 1):
        pages_amount.append(page)
    for number, parsed_books in enumerate(list(chunked(parsed_books, per_page_books)), 1):
        rendered_page = template.render(
            parsed_books=list(chunked(parsed_books, 2)),
            pages_amount=pages_amount,
            current_page=number,
        )
        pathlib.Path(pages_folder).mkdir(parents=True, exist_ok=True)
        with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')


