from flask import Flask, render_template, request,redirect,url_for, jsonify
from datetime import date, timedelta
from statement import statement_bp
from mailing import mailing_bp
from db import get_db

app = Flask(__name__)

app.register_blueprint(statement_bp)
app.register_blueprint(mailing_bp)

@app.route("/")
def first():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

def get_total(cursor, table_name):
    cursor.execute(f"SELECT COALESCE(SUM(amount), 0) FROM {table_name}")
    result = cursor.fetchone()
    return float(result[0] or 0)

@app.route("/dashboard")
def dashboard():

    con = get_db()
    cursor = con.cursor()

    total_expense = get_total(cursor, "rough")
    total_income = get_total(cursor, "income")

    con.close()

    return render_template(
        "dashboard.html",
        total_expense=total_expense,
        total_income=total_income,
        balance=total_income - total_expense
    )

@app.route("/dashboard/expenseentry")
def entrypg():
    today = date.today()
    least = today - timedelta(days=3)
    return render_template("entry.html",least=least,present=today)

@app.route("/dashboard/expenseentry/submitted")
def submitted():
    return render_template('entry.html',status='success')

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

    return redirect(url_for("submitted"))

if __name__ == '__main__':
    app.run(debug=True)