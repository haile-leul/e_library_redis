from typing import Mapping
from backend import *


while(1):
    print('Welcome to e-lib manager!')
    print('You are in publisher mode.')
    print('Please add a book to the library')
    print('Enter ISBN:')
    b_isbn = input()
    print('Enter book title:')
    b_title = input()
    print('Enter book author:')
    b_author = input()
    print('Enter book genre:')
    b_genre = input()
    print('Enter book language:')
    b_lang = input()
    print('Enter the number of copies to be added:')
    b_copies = input()
    print('Keywords:')
    b_keywords = input()

    book_desc = {
        'isbn': b_isbn,
        'title': b_title,
        'author': b_author,
        'genre': b_genre,
        'language': b_lang,
        'no_of_copies': b_copies,
        'keywords': b_keywords
    }

    print(b_isbn, b_title, b_author, b_genre, b_lang, b_copies)
    add_book(book_desc)
