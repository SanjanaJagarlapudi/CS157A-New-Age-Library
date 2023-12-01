import os
import sqlite3
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 
import datetime

app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'

#Make a new db for our app, and call it New Age Library
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///New_Age_Library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development

db = SQLAlchemy(app)

   #CREATE TABLE BOOK (
   # ISBN INT PRIMARY KEY,
    #TITLE VARCHAR,
    #GENRE VARCHAR,
    #AGE_DEMOGRAPHIC VARCHAR
    #Publish_date
#);
 
class Book(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    age_demographic= db.Column(db.String(100))
    #publish_date = db.Column(db.DateTime)
    def __repr__(self):
        return self.title

#Update the search columns with the new address modifications 
class Patron(db.Model):
    patron_id = db.Column(db.Integer, primary_key=True)
    patronFirstName = db.Column(db.String(100), nullable=False)
    patronLastName = db.Column(db.String(100), nullable=False)
    patronEmail = db.Column(db.String(100), nullable=False)
    patronCity = db.Column(db.String(100), nullable=False)
    patronStreet = db.Column(db.String(100), nullable=False)
    patronState = db.Column(db.String(100), nullable=False)
    patronCountry = db.Column(db.String(100), nullable=False)
    patronZipcode = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"{self.patronFirstName}, {self.patronLastName}"

class Librarian(db.Model):
    librarian_id = db.Column(db.Integer, primary_key=True)
    librarianFirstName = db.Column(db.String(100), nullable=False)
    librarianLastName = db.Column(db.String(100), nullable=False)
    librarianEmail = db.Column(db.String(100), nullable=False)
    librarianCity = db.Column(db.String(100), nullable=False)
    librarianStreet = db.Column(db.String(100), nullable=False)
    librarianState = db.Column(db.String(100), nullable=False)
    librarianCountry = db.Column(db.String(100), nullable=False)
    librarianZipcode = db.Column(db.Integer, nullable=False)
    #You can change this to return something else later on
    def __repr__(self):
        return f"{self.librarianFirstName}, {self.librarianLastName}"
    
class TransactionHistory(db.Model):
    transactionId = db.Column(db.Integer, primary_key=True)
    checkoutDate = db.Column(db.DateTime, nullable = False)
    dueDate = db.Column(db.DateTime)
    librarianId = db.Column(db.Integer, db.ForeignKey(Librarian.librarian_id), nullable=False)
    patronId = db.Column(db.Integer, db.ForeignKey(Patron.patron_id), nullable=False)
    txn_isbn = db.Column(db.Integer, db.ForeignKey(Book.isbn), nullable=False)

    
   # patron = db.relationship('Patron', backref=db.backref('TransactionHistory', lazy=True))
   # isbn = db.relationship('Book', backref=db.backref('TransactionHistory', lazy=True))

    #change later based on the requirements of the ui
    def __repr__(self):
        return f"{self.transactionId}, {self.txn_isbn}, {self.checkoutDate}, {self.dueDate}"

class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True, nullable = False)
    authorFirstName = db.Column(db.String(100), nullable=False)
    authorLastName = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.Integer, db.ForeignKey(Book.isbn), nullable=False)
    def __repr__(self):
        return f"{self.authorFirstName}, {self.authorLastName}, {self.isbn}"


def load_all_db_results():
    librarians = Librarian.query.all()
    books = Book.query.all()
    patrons = Patron.query.all()    
    authors = Author.query.all()
    transactions = TransactionHistory.query.all()
    
    return [books, authors, patrons, librarians, transactions]

#Home page (DEFAULT PAGE)
@app.route("/", methods=["GET", "POST"])
def new_age_library():
    allObj = load_all_db_results();    
    return render_template("new_age_library.html", allObj=allObj)

@app.route("/patronView", methods=["GET", "POST"])
def displayPatronView():    
    librarians = Librarian.query.all()
    books = Book.query.all()
    patrons = Patron.query.all()    
    authors = Author.query.all()
    transactions = TransactionHistory.query.all()     
   
    return render_template("patern_view_results.html", ibrarians=librarians, books=books, patrons=patrons, authors=authors, transactions=transactions) 


@app.route("/librarianView", methods=["GET", "POST"])
def displayLibrarianView():
    clickVaule = request.form.get("librarian_view")
    librarian_views = Librarian.query.all()
    return render_template("librarian_view_results.html", librarian_views=librarian_views )


@app.route("/adminView", methods=["GET", "POST"])
def displayAdminView():    
    librarians = Librarian.query.all()
    books = Book.query.all()
    patrons = Patron.query.all()    
    authors = Author.query.all()
    transactions = TransactionHistory.query.all()
    return render_template("admin_view_results.html", librarians=librarians, books=books, patrons=patrons, authors=authors, transactions=transactions )


@app.route("/searchTables", methods=["GET", "POST"])
def search():
    table_name = request.form.get("table_to_query")
    search_field = request.form.get("search_field")
    search_field_value = request.form.get("search_field_value")
     

    print(search_field)
    print(search_field_value)

    if table_name == 'Book':
        mystr = "hello"
        
        if search_field == 'isbn':
            books = Book.query.filter_by(isbn=int(search_field_value))
            return render_template("search_results.html" , books=books)
        if search_field == 'title':
            books = Book.query.filter_by(title=search_field_value)
            print(books)
            return render_template("search_results.html" , books=books)
        if search_field == 'genre':
            books = Book.query.filter_by(genre=search_field_value)
            print(books)
            return render_template("search_results.html" , books=books)
        if search_field == 'agedemo':
            books = Book.query.filter_by(age_demographic=search_field_value)
            print(books)
            return render_template("search_results.html" , books=books)
            
        books = Book.query.filter_by(isbn=int(search_field_value))
        return render_template("search_results.html" , books=books)
        print (books)

    return render_template("search_results.html" , books=books)

'''@app.route("/", methods=["GET", "POST"])
def index():
    books = Book.query.all()
    print(books)
   
    return render_template("index.html", books=books)'''

#TO ADD NEW BOOKS
@app.route("/addBook", methods=["GET", "POST"])
def update_book_table():
    title = request.form.get("title")
    genre = request.form.get("genre")
    age_demographic = request.form.get("demographics")   

    new_book = Book(title=title, genre=genre, age_demographic=age_demographic)
    db.session.add(new_book)
    db.session.commit()

    return redirect("/")

@app.route("/deleteBook", methods=["POST"])
def delete():
    isbn = request.form.get("book_isbn")
    # Retrieve the book from the database using the book_id
    book = Book.query.get(isbn)
    if book:
        # If the book exists, delete it from the database
        db.session.delete(book)
        db.session.commit()
    return redirect("/")

@app.route("/updateBook", methods=["POST"])
def updateBook():
    book.isbn = request.form.get("book.isbn")
    new_title = request.form.get("new_title")  
    new_genre = request.form.get("new_genre")
    new_demographics = request.form.get("new_demographics")
    
    book = Book.query.get(book.isbn)
    if book:
        book.title = new_title
        book.genre = new_genre
        book.age_demographic = new_demographics    

        db.session.commit()

    return redirect("/")

#TO ADD NEW Authors
@app.route("/addAuthor", methods=["GET", "POST"])
def addAuthor():
    fname = request.form.get("author_firstname")
    lname = request.form.get("author_lastname")    
    isbn = request.form.get("book_isbn")   

    new_author = Author(authorFirstName=fname, authorLastName=lname, isbn=isbn)
    db.session.add(new_author)
    db.session.commit()

    librarians = Librarian.query.all()
    books = Book.query.all()
    patrons = Patron.query.all()    
    authors = Author.query.all()
    transactions = TransactionHistory.query.all()
  
    return render_template("admin_view_results.html", librarians=librarians, books=books, patrons=patrons, authors=authors, transactions=transactions )

##Sanjana's Code starts from here: 
#Patron Functionalities

@app.route("/addPatron", methods=["GET", "POST"])
def addPatron():
    fname = request.form.get("patron_firstname")
    lname = request.form.get("patron_lastname")    
    email = request.form.get("patron_email")  
    city = request.form.get("patron_city")  
    state = request.form.get("patron_state")  
    street = request.form.get("patron_street")   
    country = request.form.get("patron_country")
    zipcode = request.form.get("patron_zipcode")

    new_patron = Patron(patronFirstName=fname, patronLastName=lname, patronEmail=email, patronCity=city, patronStreet=street, patronState = state, patronCountry = country, patronZipcode = zipcode )
    db.session.add(new_patron)
    db.session.commit()

    #Confused on what to do with the code below:
    #Why have we not included transaction below
    librarians = Librarian.query.all()
    books = Book.query.all()
    patrons = Patron.query.all()    
    authors = Author.query.all()
    transactions = TransactionHistory.query.all()
    return render_template("admin_view_results.html", librarians=librarians, books=books, patrons=patrons, authors=authors, transactions = transactions )
 
#Librarian Functionalities

@app.route("/addLibrarian", methods=["GET", "POST"])
def addLibrarian():
    fname = request.form.get("librarian_firstname")
    lname = request.form.get("librarian_lastname")    
    email = request.form.get("librarian_email")  
    city = request.form.get("librarian_city")  
    state = request.form.get("librarian_state")  
    street = request.form.get("librarian_street")   
    country = request.form.get("librarian_country")
    zipcode = request.form.get("librarian_zipcode")

    new_librarian = Librarian(librarianFirstName=fname, librarianLastName=lname, librarianEmail=email, librarianCity=city, librarianStreet=street, librarianState = state, librarianCountry = country, librarianZipcode = zipcode )
    db.session.add(new_librarian)
    db.session.commit()

    #Confused on what to do with the code below:
    #Why have we not included transaction below
    librarians = Librarian.query.all()
    books = Book.query.all()
    patrons = Patron.query.all()    
    authors = Author.query.all()
    transactions = TransactionHistory.query.all()
    return render_template("admin_view_results.html", librarians=librarians, books=books, patrons=patrons, authors=authors, transactions = transactions )
 
 #Transaction Functionalities
@app.route("/addTransaction", methods=["GET", "POST"])
def addTransaction():
    checkout = convert(request.form.get("transaction_checkoutDate")) 
    due = convert(request.form.get("transaction_dueDate")) 
    libid = request.form.get("t_librarian_id")  
    patid = request.form.get("t_patron_id")  
    isbn = request.form.get("t_book_isbn")  

    new_transaction = TransactionHistory(checkoutDate=checkout, dueDate=due, librarianId=libid, patronId=patid, txn_isbn=isbn)
    db.session.add(new_transaction)
    db.session.commit()

    #Confused on what to do with the code below:
    #Why have we not included transaction below
    librarians = Librarian.query.all()
    books = Book.query.all()
    patrons = Patron.query.all()    
    authors = Author.query.all()
    transactions = TransactionHistory.query.all()
  #  admin_views5 = Address.query.all()
    return render_template("admin_view_results.html", librarians=librarians, books=books, patrons=patrons, authors=authors, transactions = transactions )
 
def create_tables():
    with app.app_context():
        db.create_all()
        # Create tables for Address, User, and other models if they're not already created
        db.session.commit()
def convert(date_time):
    format =  '%b %d %Y'
    datetime_str = datetime.datetime.strptime(date_time, format) 
    return datetime_str
if __name__ == "__main__":
    create_tables()  # Create tables before running the app
    app.run(debug=True)