from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server
import pathlib
import json
import math


def on_reload():
    with open('description.json', 'r', encoding="utf-8") as my_file:
        parsed_books = json.load(my_file)

    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')

    pages_folder = 'pages'
    pathlib.Path(pages_folder).mkdir(parents=True, exist_ok=True)

    amount_books_per_page = 20
    amount_pages = math.ceil(len(parsed_books) / amount_books_per_page)
    for number, books_per_page in enumerate(
            list(chunked(parsed_books, amount_books_per_page)), 1):
        rendered_page = template.render(
            books_per_page=list(chunked(books_per_page, 2)),
            amount_pages=amount_pages,
            current_page=number,
        )
        with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
