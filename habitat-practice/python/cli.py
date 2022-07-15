from crud import Session
from models import Book
from sqlalchemy import and_, or_

import json
from datetime import date, datetime

s = Session()

books = s.query(Book).limit(100).all()
book_arr = []
book_dict = {}
    
count = 0

for count, u in enumerate(books):

    book_dict['id'] = u.__dict__['id']
    book_dict['title'] = u.__dict__['title']
    book_dict['title_url'] = u.__dict__['title_url']
    book_dict['author'] = u.__dict__['author']
    book_dict['published'] = u.__dict__['published'].isoformat()
    book_dict['price'] = u.__dict__['price']
    book_dict['pages'] = u.__dict__['pages']  
    book_json = json.loads(json.dumps(book_dict))
  
    if book_json in book_arr:
        print('no dupes')
    else:
        book_arr.append(book_json) 
    
    count = count + 1 


for book in books:
    # price = input(f"Price for '{book.title}': $")
    book.price= 1
    # book.price = price
    # s.add(book)

# s.commit()

#--------------------------------------------------------------
## a few helpful methods to query and filter database
#--------------------------------------------------------------

# ### get first book in the table
# print(f'first book: {s.query(Book).first().title}')

# ### two methods of filtering table values
# r = s.query(Book).filter_by(title='Deep Learning').first()
# print("filter_by:", r)
# r = s.query(Book).filter(Book.title=='Deep Learning').first()
# print("filter:", r)

# ### ignore case
# r = s.query(Book).filter(Book.title.ilike('deep learning')).first()  
# print("ignore case:", r)

# ### filter to between two dates
# start_date = datetime(2009, 1, 1)
# end_date = datetime(2012, 1, 1)
# r = s.query(Book).filter(Book.published.between(start_date, end_date)).all()
# print("filter between two dates:", r)

# ### multiple filters at a time ( -- and -- )
# r = s.query(Book).filter(
#     and_(
#        Book.pages > 750,
#        Book.published > datetime(2016, 1, 1)
#     )
# ).all()
# print("multiple filters --and--:", r)

# ### multiple filters at a time ( -- or -- )
# r = s.query(Book).filter(
#     or_(
#         Book.published < datetime(1700, 1, 1),
#         Book.published > datetime(2017, 1, 1)
#     )
# ).all()
# print("multiple filters --or--:", r)

# ### order by
# r = s.query(Book).order_by(Book.pages.desc()).all()
# ##print("order by:", r)

# ### limit
# r = s.query(Book).limit(2).all()
# print("limit: ", r)

# ### complex query
# r = s.query(Book).filter(
#     and_(
#         or_(
#             Book.pages < 500,
#             Book.pages > 750
#         ),
#         Book.published.between(datetime(2016, 1, 1), datetime(2017, 1, 1))
#     )
# )\
# .order_by(Book.pages.desc())\
# .limit(1)\
# .first() 
# print("complex query: ", r)
##
#--------------------------------------------------------------

s.expunge_all()
s.close()