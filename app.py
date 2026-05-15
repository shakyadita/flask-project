from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DATABASE = 'expenses.db'


# ─── Database Setup ───────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            note        TEXT
        )
    ''')
    conn.commit()
    conn.close()


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()

    # Get filter params
    month  = request.args.get('month',  datetime.now().strftime('%Y-%m'))
    cat    = request.args.get('category', 'All')

    # Build query
    if cat == 'All':
        cursor.execute(
            "SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ? ORDER BY date DESC",
            (month,)
        )
    else:
        cursor.execute(
            "SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ? AND category = ? ORDER BY date DESC",
            (month, cat)
        )

    expenses = cursor.fetchall()

    # Total for selected month
    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE strftime('%Y-%m', date) = ?",
        (month,)
    )
    total = cursor.fetchone()[0]

    # Category-wise breakdown for selected month
    cursor.execute(
        "SELECT category, COALESCE(SUM(amount), 0) as cat_total FROM expenses WHERE strftime('%Y-%m', date) = ? GROUP BY category ORDER BY cat_total DESC",
        (month,)
    )
    category_totals = cursor.fetchall()

    # All distinct months for filter dropdown
    cursor.execute(
        "SELECT DISTINCT strftime('%Y-%m', date) as month FROM expenses ORDER BY month DESC"
    )
    months = [row['month'] for row in cursor.fetchall()]
    if month not in months:
        months.insert(0, month)

    conn.close()

    categories = ['Food', 'Transport', 'Shopping', 'Bills', 'Health',
                  'Entertainment', 'Education', 'Other']

    return render_template('index.html',
                           expenses=expenses,
                           total=total,
                           category_totals=category_totals,
                           selected_month=month,
                           selected_cat=cat,
                           months=months,
                           categories=categories)


@app.route('/add', methods=['POST'])
def add_expense():
    title    = request.form.get('title', '').strip()
    amount   = request.form.get('amount', 0)
    category = request.form.get('category', 'Other')
    date     = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    note     = request.form.get('note', '').strip()

    if not title or not amount:
        return redirect(url_for('index'))

    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (title, amount, category, date, note) VALUES (?, ?, ?, ?, ?)",
        (title, float(amount), category, date, note)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for('index'))


@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    conn = get_db()

    if request.method == 'POST':
        title    = request.form.get('title', '').strip()
        amount   = request.form.get('amount', 0)
        category = request.form.get('category', 'Other')
        date     = request.form.get('date')
        note     = request.form.get('note', '').strip()

        conn.execute(
            "UPDATE expenses SET title=?, amount=?, category=?, date=?, note=? WHERE id=?",
            (title, float(amount), category, date, note, expense_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    expense = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()

    categories = ['Food', 'Transport', 'Shopping', 'Bills', 'Health',
                  'Entertainment', 'Education', 'Other']

    return render_template('edit.html', expense=expense, categories=categories)


@app.route('/summary')
def summary():
    conn = get_db()
    cursor = conn.cursor()

    # Monthly totals for chart
    cursor.execute(
        "SELECT strftime('%Y-%m', date) as month, SUM(amount) as total FROM expenses GROUP BY month ORDER BY month"
    )
    monthly_data = cursor.fetchall()

    # All-time category breakdown
    cursor.execute(
        "SELECT category, SUM(amount) as total FROM expenses GROUP BY category ORDER BY total DESC"
    )
    category_data = cursor.fetchall()

    # Grand total
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    grand_total = cursor.fetchone()[0]

    conn.close()

    return render_template('summary.html',
                           monthly_data=monthly_data,
                           category_data=category_data,
                           grand_total=grand_total)


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
