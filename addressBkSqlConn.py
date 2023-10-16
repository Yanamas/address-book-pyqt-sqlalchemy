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
    

engine = create_engine("sqlite:///AddressBook.db", echo=True) # creates file, work with the file
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
