from flask import Blueprint, render_template
from db import get_db
from flask import send_file
from openpyxl import Workbook
import io

statement_bp = Blueprint('statement', __name__)

def get_statement_data():
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

    from collections import defaultdict

    category_totals = defaultdict(float)
    payment_totals = defaultdict(float)

    for row in result:
        amount = float(row[5])

        category = simplify_category(row[3])
        category_totals[category] += amount

        mode = row[4].strip().upper()
        payment_totals[mode] += amount

    con.close()

    return {
        "result": result,
        "total": tot[0],
        "labels": list(category_totals.keys()),
        "values": list(category_totals.values()),
        "pay_labels": list(payment_totals.keys()),
        "pay_values": list(payment_totals.values())
    }

@statement_bp.route("/dashboard/statement")
def statement():
    data = get_statement_data()

    return render_template(
        "statement.html",
        **data
    )

@statement_bp.route("/export/excel")
def export_excel():
    con = get_db()
    cursor = con.cursor()

    cursor.execute("""
        SELECT date, item, shop, category, mode, amount 
        FROM rough ORDER BY date;
    """)
    data = cursor.fetchall()
    con.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"

    # Header
    headers = ["Date", "Item", "Shop", "Category", "Mode", "Amount"]
    ws.append(headers)

    # Data
    for row in data:
        ws.append(row)

    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return send_file(
        file_stream,
        as_attachment=True,
        download_name="expenses.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@statement_bp.route("/pdf")
def pdf():
    data = get_statement_data()

    return render_template(
        "pdf_format.html",
        records=data["result"],   # rename if needed
        total=data["total"],
        labels=data["labels"],
        values=data["values"],
        pay_labels=data["pay_labels"],
        pay_values=data["pay_values"]
    )