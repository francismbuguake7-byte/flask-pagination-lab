#!/usr/bin/env python3

from flask import request
from flask_restful import Resource

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=5, type=int)

        if page is None or page < 1:
            page = 1
        if per_page is None or per_page < 1:
            per_page = 5

        paginated_books = Book.query.paginate(page=page, per_page=per_page, error_out=False)

        response = {
            "page": paginated_books.page,
            "per_page": paginated_books.per_page,
            "total": paginated_books.total,
            "total_pages": paginated_books.pages,
            "items": [BookSchema().dump(book) for book in paginated_books.items],
        }
        return response, 200


api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)