from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json


def on_reload():
    with open('description.json', 'r', encoding="utf-8") as my_file:
        parsed_books_json = my_file.read()

    parsed_books = json.loads(parsed_books_json)
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    rendered_page = template.render( books=parsed_books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')


