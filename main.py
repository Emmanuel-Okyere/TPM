from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
import os
import mariadb
import sys
import psycopg2
import mysql.connector
import pyodbc
from flask_marshmallow import Marshmallow


app=Flask(__name__)

app.config['SECRET_KEY']="secret"
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:okyere@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True


db=SQLAlchemy(app)
ma=Marshmallow(app)

class Person(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.String(50))

class DataSchema(ma.Schema):
    class Meta:
        fields=("username","email")

db.init_app(app)






@app.route("/" ,methods=["GET","POST"])
def home():
    return render_template("home.html")


@app.route("/all",methods=["GET","POST"])
def processData():
    if request.method == "GET":
        return render_template("home.html")

    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        database=request.form.get("db")

        if database =="postgres":
            user=Person(username=username,email=email,password=password)
            db.session.add(user)
            db.session.commit()
            return render_template("home.html",message="Your Data has been stored in Our PostGreSQL Database Successfully")
            
        elif database=="mysql":
            mydb = mysql.connector.connect(host="localhost",user="root",password="", database="loginsystem")
            mycursor = mydb.cursor()
            sql = "INSERT INTO users (username,email,password) VALUES (%s,%s,%s)"
            val = (username, email,password)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template("home.html",message="Your Data has been stored in Our SQL Database Successfully")


        elif database == "mariadb":
            try:
                conn = mariadb.connect(user="root",password="okyere",host="127.0.0.1",port=3306,database="maria")
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)
            cur = conn.cursor()
            try: 
                cur.execute("INSERT INTO user (username,email,password) VALUES ('{}','{}','{}')".format(username,email,password)) 
            except mariadb.Error as e: 
                print(f"Error: {e}")
            conn.commit() 
            return render_template("home.html",message="Your Data has been stored in Our Mariadb Successfully")
        elif database=="msserver":
            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};""Server=AQUILA-KPASOYA;" "Database=microsoft;""Trusted_Connection=yes;")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO microsoft.dbo.person (username,email,password) VALUES ('{}','{}','{}')".format(username,email,password))
            conn.commit()
            return render_template("home.html",message="Your Data has been stored in Our MsServer Successfully")


        else:
            return render_template("home.html")
            
            
        
@app.route("/get-data/<int:database>")
def retrieveData(database):
    if database == 1:
        dataschema=DataSchema(many=True)
        all_data=Data.query.all()
        data=[]
        for row in dataschema.dump(all_data):
            res=[]
            res.append(row['username'])
            res.append(row['email'])
            data.append(tuple(res))
        
        return render_template("results.html",results=data)
    elif database==2:
        mydb = mysql.connector.connect(host="localhost",user="root",password="", database="loginsystem")
        mycursor = mydb.cursor()
        sql = "SELECT * FROM  users"
        mycursor.execute(sql)
        data=mycursor.fetchall()
        print(data[0])
        return render_template("results.html",results=data)
    elif database == 3:
         conn = mariadb.connect(user="root",password="okyere",host="127.0.0.1",port=3306,database="maria")
         cur = conn.cursor()
         cur.execute("SELECT * FROM  data")
         data = cur.fetchall()
         return render_template("results.html",results=data)

    elif database==4:
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};""Server=HAYATU;" "Database=citizen;""Trusted_Connection=yes;")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM  citizen.dbo.data")
        data=cursor.fetchall()
        return render_template("results.html",results=data)




if __name__=="__main__":
    app.run(debug=True)



