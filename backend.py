import redis
from collections import defaultdict
import pprint

HOST = 'localhost'
PORT = 6379
DATABASE = 0

r = redis.Redis(host=HOST, port=PORT, db=DATABASE)


# publisher functions
def add_book(book_desc):
    book_id = book_desc['isbn']
    # bookid = r.incr("next_book_id")
    name = 'book:' + book_id

    # if book with ISBN already exists do this
    if(r.hvals(name)):
        print("Book already exists.")
        print("1. Just increase the number of copies")
        print("2. Replace book entry")
        print("3. Cancel action")
        action = input()
        if action == "1":
            previous_copies = int(r.hget(name, "no_of_copies"))
            new_copies = previous_copies + int(book_desc['no_of_copies'])
            r.hset(name, key="no_of_copies", value=new_copies)
        elif action == "2":
            r.hset(name=name, mapping=book_desc)
        else:
            print('Action Canceled')
            return
    # if book doesnt exist add new entry
    else:
        r.hset(name=name, mapping=book_desc)
    r.expire(name, 600)

    # publish to channels
    kwlist = [x.strip() for x in book_desc['keywords'].split(',')]
    for kw in kwlist:
        r.publish(kw.lower(), 'ISBN: ' + book_desc['isbn'] + ' - ' + book_desc['title'])
    print('Book Added Successfully')

def borrow(b_isbn):
    name = 'book:' + b_isbn
    print(name)
    book = r.hgetall(name)
    if not book:
        print("This book does not exist in our library's database.")
        return
    if int(book['no_of_copies'.encode('utf-8')]) > 0:
        r.hincrby(name, 'no_of_copies'.encode('utf-8'), -1)
        print('You have borrowed ' + '"' + str(book['title'.encode('utf-8')].decode('utf-8')) + '"')
    else:
        print('This book is not available')

def return_book(b_isbn):
    name = 'book:' + b_isbn
    book = r.hgetall(name)

    if not book:
        print('Book does not exist in the library')
        return
    r.hincrby(name, 'no_of_copies'.encode('utf-8'), 1)
    print('You have returned '+ '"' + str(book['title'.encode('utf-8')].decode('utf-8')) + '"')

# subscriber functions
def subscriber():
    pubsub = r.pubsub()
    return pubsub

def subscribe(pubsub, channel):
    pubsub.subscribe(channel)
    print('Subscribed to ', channel)

# get new messages for the subscribed keyword
def get_messages(pubsub):
    try:
        messages = defaultdict(list)
        while True:
            message = pubsub.get_message()
            if not message: break
            # print(message)
            if message['type'] == 'message':
                channel = message['channel'].decode('utf-8')
                messages[channel].append(message['data'].decode('utf-8'))
        for channel in messages.keys():
            print("You have new messages!\n")
            print("New books for keyword " + channel)
            for book in messages[channel]:
                print(book)
    except:
        print('You have not subscribed to any channels yet.\nPlease subscribe to a channel first.')

def book_details(b_isbn):
    name = 'book:' + b_isbn

    book = r.hgetall(name)
    book = {key.decode('utf-8'):value.decode('utf-8') for key,value in book.items()}

    pprint.pprint(book)
