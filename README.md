# 💸 Monthly Expense Tracker

> A full-stack web application built with Flask and Python that helps you record, categorize, and analyze your daily expenses — with interactive charts and monthly breakdowns.

---

## ✨ Features

- ✅ Add, edit, and delete expenses
- ✅ Categorize expenses (Food, Transport, Shopping, Bills, Health, Entertainment, Education, Other)
- ✅ Filter by month and category
- ✅ Monthly total and per-category breakdown with progress bars
- ✅ Summary page with bar chart (monthly trend) and doughnut chart (by category)
- ✅ SQLite database — no setup required
- ✅ Clean dark UI with responsive design

---

## 🖥️ Screenshots

| Dashboard | Summary |
|---|---|
| Add expenses, filter by month/category, see breakdown | Monthly bar chart + category doughnut chart |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core backend language |
| Flask | Web framework — routing, templates, form handling |
| SQLite3 | Lightweight database for storing expenses |
| Jinja2 | HTML templating engine (built into Flask) |
| Chart.js | Interactive charts on summary page |
| HTML/CSS | Frontend UI |

---

## 📁 Project Structure

```
expense-tracker/
│
├── app.py                  # Main Flask application
├── expenses.db             # SQLite database (auto-created on first run)
├── requirements.txt        # Python dependencies
├── README.md
│
└── templates/
    ├── index.html          # Dashboard — expense list + add form
    ├── edit.html           # Edit expense page
    └── summary.html        # Charts and overall summary
```

---

## ⚙️ How It Works

### Database Schema
```sql
CREATE TABLE expenses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    amount      REAL    NOT NULL,
    category    TEXT    NOT NULL,
    date        TEXT    NOT NULL,
    note        TEXT
);
```

### Flask Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Dashboard — list expenses with filters |
| `/add` | POST | Add new expense |
| `/edit/<id>` | GET/POST | Edit existing expense |
| `/delete/<id>` | GET | Delete expense |
| `/summary` | GET | Charts and all-time summary |

### Python Concepts Used
- **SQLite3** — database connection, CRUD operations
- **Flask routing** — `@app.route()` decorators
- **Jinja2 templating** — dynamic HTML with Python variables
- **`request.form`** — reading HTML form data
- **`redirect` + `url_for`** — navigation after form submit
- **`datetime`** — default date handling
- **Lambda functions** — used for data transformations
- **SQL queries** — GROUP BY, SUM, strftime for date filtering

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/shakyadita/expense-tracker.git

# 2. Navigate into the project folder
cd expense-tracker

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python app.py
```

Then open your browser and go to:
```
http://127.0.0.1:5000
```

> The SQLite database (`expenses.db`) is created automatically on first run.

---

## 📊 Pages

### 1. Dashboard (`/`)
- Shows all expenses for selected month
- Filter by month and category
- Add new expense via form
- Edit or delete any expense
- Category-wise spending breakdown with progress bars

### 2. Summary (`/summary`)
- All-time total spending
- Monthly spending bar chart
- Category distribution doughnut chart
- Built with Chart.js

---

## 🧠 Concepts Demonstrated

| Concept | Where Used |
|---|---|
| Flask Routing | All pages — `@app.route` |
| SQLite CRUD | Add, edit, delete, read expenses |
| Jinja2 Templating | Dynamic HTML rendering |
| Form Handling | `request.form` for all inputs |
| SQL Aggregation | `GROUP BY`, `SUM`, monthly filters |
| Data Visualization | Chart.js bar and doughnut charts |
| Redirect/URL_for | Post-submit navigation |
| Date Handling | Python `datetime`, SQL `strftime` |

---

## 🔮 Future Improvements

- [ ] Add user login/authentication
- [ ] Export expenses to CSV or PDF
- [ ] Set monthly budget limits with alerts
- [ ] Add recurring expense feature
- [ ] Deploy to cloud (Heroku / Render)
- [ ] Add REST API endpoints

---

## 👩‍💻 Author

**Shakyadita Sonawane**

📧 shakyaditaofficial@gmail.com

🎓 B.E. Computer Engineering (AI/ML Honours) — GCOEARA, 2023

---

## 📃 License

This project is open source and available under the [MIT License](LICENSE).

---

> *"Track every rupee — because small leaks sink big ships."*
