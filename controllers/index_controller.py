from flask import Flask, render_template, redirect, url_for, flash, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL(app)


def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    return render_template('index.html', users=data, title="Users")
