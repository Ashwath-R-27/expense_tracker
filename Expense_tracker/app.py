from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime
from datetime import date, timedelta
from flask_mail import Mail, Message
import bcrypt

app = Flask(__name__)

def send_email():
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'ashwathr27100@gmail.com'
    app.config['MAIL_PASSWORD'] = 'uzpg hgap bcfh hwki'  # NOT your Gmail password
    app.config['MAIL_DEFAULT_SENDER'] = 'ashwathr27100@gmail.com'

    mail = Mail(app)
    return mail

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ashwath@2008",
        database="expenses"
    )

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/entry")
def entrypg():
    today = date.today()
    least = today - timedelta(days=3)
    return render_template("entry.html",least=least,present=today)

@app.route("/submit_expenses", methods=["POST"])
def submit_expenses():
    db = get_db()
    cursor = db.cursor()

    items = request.form.getlist("item[]")
    shops = request.form.getlist("shop[]")
    categories = request.form.getlist("type[]")
    amounts = request.form.getlist("amount[]")
    modes = request.form.getlist("mode[]")
    dates = request.form.getlist("date[]")

    for item, shop, category, amount, mode, date_val in zip(items, shops, categories, amounts, modes, dates):
        cursor.execute("""
            INSERT INTO rough
            (item, shop, category, amount, mode, date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            item.upper(),
            shop.upper(),
            category.upper(),
            amount,
            mode.upper(),
            date_val
        ))

    db.commit()
    cursor.close()
    db.close()

    return "Expenses saved successfully!"

if __name__ == '__main__':
    app.run(debug=True)