import os
import sqlite3
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(os.path.dirname(__file__), 'New_Age_Library.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development
db = SQLAlchemy(app)



   #CREATE TABLE BOOK (
   # ISBN INT PRIMARY KEY,
    #TITLE VARCHAR,
    #GENRE VARCHAR,
    #AGE_DEMOGRAPHIC VARCHAR
#);

def rows_as_dicts(cursor):
    """convert tuple result to dict with cursor"""
    col_names = [i[0] for i in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor]

 
class Book(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    genre = db.Column(db.String(100))
    age_demographic= db.Column(db.String(50))
    def __repr__(self):
        return self.title
    
class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True, nullable = False)
    authorFirstName = db.Column(db.String(100), nullable=False)
    authorLastName = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.Integer, db.ForeignKey(Book.isbn), nullable=False)
    def __repr__(self):
        return f"{self.authorFirstName}, {self.authorLastName}, {self.isbn}"

def create_tables():
    with app.app_context():           
        db.create_all()
        # Create tables for Address, User, and other models if they're not already created
        db.session.commit()


"""def get_db_connection():
    conn = sqlite3.connect('NewLIB.db')
    conn.row_factory = sqlite3.Row
    return conn"""

""" @app1.route('/', methods=['POST', 'GET'])
def index():
    conn = get_db_connection()
    myQuery = conn.execute('SELECT * FROM Book').fetchall()
    conn.close
    return render_template('index.html', myQuery=myQuery) """

@app.route("/", methods=["GET", "POST"])
def index():
    session = db.session()
    q = session.query(
         Book, Author,
    ).filter(
         Author.isbn == Book.isbn,    
    ).all()

   #singleQuery = Author.query.join(Book, Author.isbn==Book.isbn)
    print ('IT IS WORKING ')
    print (q);
    books = Book.query.all()
    
   
    return render_template("index.html", books=books)

if __name__ == "__main__":
    with app.app_context():         # <--- without these two lines,         
        db.create_all()             # <--- we get the OperationalError in the title
        app.run(debug=True)