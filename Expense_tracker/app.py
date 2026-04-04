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

from collections import defaultdict

@app.route("/dashboard/statement")
def statement():
    con = get_db()
    cursor = con.cursor()

    cursor.execute("""
        SELECT DATE_FORMAT(date, '%d/%m/%Y'),
               item, shop, category, mode, amount 
        FROM rough ORDER BY date;
    """)
    result = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM rough")
    tot = cursor.fetchone()

    # ✅ Category grouping (IMPORTANT: your DB stores UPPERCASE)
    CATEGORY_MAP = {
        "Food & Dining": ["GROCERIES", "SNACKS", "TEA / COFFEE", "MEAT(CHICKEN/MUTTON/FISH)", "HOTEL"],
        "Transport": ["PETROL / FUEL", "TRANSPORT", "TAXI / AUTO", "BUS / TRAIN"],
        "Bills & Utilities": ["MOBILE RECHARGE", "INTERNET BILL", "ELECTRICITY BILL", "WATER BILL", "RENT"],
        "Shopping": ["ONLINE SHOPPING", "CLOTHING", "ELECTRONICS"],
        "Health & Personal": ["MEDICAL / PHARMACY", "HOSPITAL", "PERSONAL CARE", "GYM / FITNESS"],
        "Others": ["ATM WITHDRAWAL", "INTERNET BANKING", "EDUCATION", "STATIONERY",
                   "ENTERTAINMENT", "MOVIE", "SUBSCRIPTION", "TRAVEL", "GIFT", "MAINTENANCE", "OTHER"]
    }

    def simplify_category(cat):
        cat = cat.strip().upper()
        for key, values in CATEGORY_MAP.items():
            if cat in values:
                return key
        return "Others"

    # ✅ Calculate totals
    category_totals = defaultdict(float)

    for row in result:
        category = simplify_category(row[3])
        amount = float(row[5])
        category_totals[category] += amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    con.close()

    return render_template(
        "statement.html",
        result=result,
        total=tot[0],
        labels=labels,
        values=values
    )

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