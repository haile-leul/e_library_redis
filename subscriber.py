from backend import *

pubsub = subscriber()

while(1):
    print('Select one of the following:')
    print('''
    1. Subscribe to a channel
    2. Get messages
    3. Borrow a book
    4. Return a book
    5. See book details
    ''')
    
    selection = input()
    available_inputs = list(range(1,6))

    if int(selection) not in available_inputs:
        print('Your choice does not match an item in the list. Please try again')
        continue

    if selection in [str(i) for i in range(3,6)]:
        print('Please enter book ISBN:')
        b_isbn = input()
        try:
            int(b_isbn)
        except:
            print('Enter an integer for ISBN')
            continue
    elif selection == '1':
        print('Channel name: ')
        channel = input()
    
    if selection == '1': subscribe(pubsub, channel)
    elif selection == '2': get_messages(pubsub)
    elif selection == '3': borrow(b_isbn)
    elif selection == '4': return_book(b_isbn)
    elif selection == '5': book_details(b_isbn)
    else: print('Action failed')