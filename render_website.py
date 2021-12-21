from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json



def main():
    with open('description.json', 'r', encoding="utf-8") as my_file:
        parsed_books_json = my_file.read()

    parsed_books = json.loads(parsed_books_json)

    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')

    rendered_page = template.render(

        books=parsed_books
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()