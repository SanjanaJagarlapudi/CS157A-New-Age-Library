import os
import sqlite3
import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 



app = Flask(__name__)

def convert(date_time):
    format =  '%b %d %Y %H:%M:%S %p'
    datetime_str = datetime.datetime.strptime(date_time, format) 
    return datetime_str

class Adam():
        name:"adam john"

class Dean():
        name:"adam john"

def returnLists():
       names = ["hema", "malini"]
       books = ["thinking", "excellent"]
       return [names, books]

if __name__ == "__main__":
        date_time = 'nov 30 2023 08:30:00'
        print(convert(date_time))
      

        app.run(debug=True)  


''' print('hello')
        list1 = [Adam, Dean]
        for i in list1:
            print (i == Adam) 
        a = returnLists();
        
        print (a.get("names"));'''      