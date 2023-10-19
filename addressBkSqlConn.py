from sqlalchemy import create_engine, ForeignKey, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    email = Column("email", String)
    phone = Column("phone", String)

    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f"({self.id}) {self.username} {self.first_name} {self.email} ({self.date_joined} {self.is_active})"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    cat_name = Column("cat_name", String, unique=True)

    def __init__(self, cat_name):
        self.cat_name = cat_name

    def __repr__(self):
        return f"({self.id} {self.cat_name})"

class ContactCategory(Base):
    __tablename__ = 'contact_categories'
    
    id = Column(Integer, primary_key=True)
    
    # Foreign Keys
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __init__(self, contact_id, category_id):
        self.contact_id = contact_id
        self.category_id = category_id

    def __repr__(self):
        return f"({self.contact_id} {self.category_id})"
    

'''
# implement later
class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    
    # Foreign Key
    contact_id = Column(Integer, ForeignKey('contacts.id'))
'''

engine = create_engine("sqlite:///AddressBook.db", echo=True) # creates file, work with the file
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Add categories to db

c1 = Category("Family")
c2 = Category("Work")
c3 = Category("School")
c4 = Category("Gym")


categories = [c1, c2, c3, c4]

for c in categories:
    existing_category = session.query(Category).filter_by(cat_name=c.cat_name).first()
    if existing_category:
        print(f"Category '{c.cat_name}' already exists.")
    else:
        session.add(c)
        

session.commit()