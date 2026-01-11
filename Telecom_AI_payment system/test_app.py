from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import pandas as pd
from datetime import datetime, date
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from chatbot_logic import chatbot_reply

app = Flask(__name__)
app.secret_key = "super-secret-key"

login_manager = LoginManager(app)
login_manager.login_view = "login"

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class User(UserMixin):
    def __init__(self, id, full_name, email):
        self.id = id
        self.full_name = full_name
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT id, full_name, email FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return User(*row) if row else None

def find_column(df, keywords):
    for col in df.columns:
        for k in keywords:
            if k.lower() in col.lower():
                return col
    return None

def is_valid_billing_period(provider, start, end):
    if not provider or not start or not end:
        return False

    if start >= end:
        return False

    y = start.year

    quarterly = [
        (date(y, 1, 1), date(y, 3, 31)),
        (date(y, 4, 1), date(y, 6, 30)),
        (date(y, 7, 1), date(y, 9, 30)),
        (date(y, 10, 1), date(y, 12, 31))
    ]

    half_year = [
        (date(y, 1, 1), date(y, 6, 30)),
        (date(y, 7, 1), date(y, 12, 31))
    ]

    if provider in ["PGCIL", "JIO"]:
        return (start, end) in quarterly

    if provider == "BSNL":
        return (start, end) in half_year

    # ❌ Explicitly block AIRTEL or others
    return False




payment_df = pd.read_excel(
    r"C:\Users\Taran Shetty\OneDrive\Attachments\Desktop\Telecom_AI_payment system\static\data\Payment ALL Updated.xlsx"
)
payment_df.columns = payment_df.columns.str.strip().str.lower()
payment_df = payment_df.fillna(0)

bandwidth_df = pd.read_excel(
    r"C:\Users\Taran Shetty\OneDrive\Attachments\Desktop\Telecom_AI_payment system\static\data\Payment ALL Updated (2).xlsx",
    sheet_name=1
)
bandwidth_df.columns = bandwidth_df.columns.str.strip().str.lower()
bandwidth_df = bandwidth_df.fillna(0)

date_col = find_column(payment_df, ["date", "bill", "invoice"])
payment_df[date_col] = pd.to_datetime(payment_df[date_col], errors="coerce")
min_date = payment_df[date_col].min().date().isoformat()

vendors = ["pgcil", "jio", "bsnl"]
amounts = {v: payment_df[f"{v} pending amount"].sum() for v in vendors}
times = {
    "pgcil": payment_df["pgcil number of quarters pending"].sum(),
    "jio": payment_df["jio number of quarters"].sum(),
    "bsnl": payment_df["bsnl number of half years"].sum(),
}

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO users VALUES (NULL,?,?,?)",
                (
                    request.form["full_name"],
                    request.form["email"],
                    generate_password_hash(request.form["password"])
                )
            )
            conn.commit()
            conn.close()
            flash("Registration successful. Please login.")
            return redirect(url_for("login"))
        except:
            flash("Email already exists")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        row = c.fetchone()
        conn.close()

        if row and check_password_hash(row[3], password):
            login_user(User(row[0], row[1], row[2]))
            return redirect(url_for("dashboard"))

        flash("Invalid login credentials")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    total = sum(amounts.values())
    percentages = [(amounts[v] / total) * 100 if total else 0 for v in vendors]
    quarters = [times[v] for v in vendors]
    return render_template("dashboard.html",
        amounts=percentages,
        quarters=quarters,
        is_home=True
    )

@app.route("/info")
@login_required
def info():
    return render_template(
        "info.html",
        columns=payment_df.columns.tolist(),
        table_data=payment_df.to_dict(orient="records"),
        is_home=False
    )

@app.route("/analysis")
@login_required
def analysis():
    total = sum(amounts.values())
    percentages = [(amounts[v] / total) * 100 if total else 0 for v in vendors]
    quarters = [times[v] for v in vendors]
    return render_template(
        "analysis.html",
        amounts=percentages,
        quarters=quarters,
        is_home=False
    )

@app.route("/mpls")
@login_required
def mpls():
    return render_template("mpls.html", is_home=False)

@app.route("/mpls/<vendor>")
@login_required
def mpls_vendor(vendor):
    cols = {
        "pgcil": ["location name", "pgcil pending amount", "pgcil number of quarters pending"],
        "jio": ["location name", "jio pending amount", "jio number of quarters"],
        "bsnl": ["location name", "bsnl pending amount", "bsnl number of half years"]
    }
    df = payment_df[cols[vendor]].copy()
    df = df.loc[(df.drop(columns=["location name"]) != 0).any(axis=1)]
    return render_template(
        "mpls_vendor.html",
        vendor=vendor.upper(),
        columns=df.columns.tolist(),
        table_data=df.to_dict(orient="records"),
        is_home=False
    )

@app.route("/new_commission")
@login_required
def new_commission():
    return render_template("new_commission.html", is_home=False)

@app.route("/new_commission/airtel")
@login_required
def airtel_commission():
    df = payment_df[["location name","airtel pending amount","airtel number of days"]]
    df = df.loc[(df != 0).any(axis=1)]
    return render_template(
        "airtel_commission.html",
        columns=df.columns.tolist(),
        table_data=df.to_dict(orient="records"),
        is_home=False
    )

@app.route("/bandwidth")
@login_required
def bandwidth():
    return render_template("bandwidth.html", is_home=False)

@app.route("/bandwidth/<vendor>")
@login_required
def bandwidth_vendor(vendor):
    bw = find_column(bandwidth_df, ["bandwidth"])
    vc = find_column(bandwidth_df, [vendor])
    df = bandwidth_df[[bw, vc]]
    return render_template(
        "bandwidth_vendor.html",
        vendor=vendor.upper(),
        columns=df.columns.tolist(),
        table_data=df.to_dict(orient="records"),
        is_home=False
    )

@app.route("/request-payment", methods=["GET","POST"])
@login_required
def request_payment():
    locations = sorted(payment_df["location name"].astype(str).unique())

    if request.method == "POST":
        provider = request.form.get("provider")
        location = request.form.get("location")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        if not all([provider, location, start_date, end_date]):
            flash("Please fill all fields before submitting", "danger")
            return redirect(url_for("request_payment"))

        s = datetime.strptime(start_date, "%Y-%m-%d").date()
        e = datetime.strptime(end_date, "%Y-%m-%d").date()

        if not is_valid_billing_period(provider, s, e):
            flash(f"Invalid billing period selected for {provider}", "danger")
            return redirect(url_for("request_payment"))
        flash(f"Payment request successful for {provider}", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "request_payment.html",
        locations=locations,
        providers=["PGCIL","JIO","BSNL","AIRTEL"],
        min_date=min_date,
        is_home=False
    )


@app.route("/api/available-providers")
@login_required
def available_providers():
    loc = request.args.get("location","").lower()
    df = payment_df[payment_df["location name"].str.lower()==loc]
    if df.empty:
        return jsonify([])
    available = []
    if (df["pgcil pending amount"]!=0).any(): available.append("PGCIL")
    if (df["jio pending amount"]!=0).any(): available.append("JIO")
    if (df["bsnl pending amount"]!=0).any(): available.append("BSNL")
    if (df["airtel pending amount"]!=0).any(): available.append("AIRTEL")
    return jsonify(available)

@app.route("/chatbot")
@login_required
def chatbot_page():
    return render_template("chatbot.html", is_home=False)


@app.route("/api/chatbot", methods=["POST"])
@login_required
def chatbot_message():
    data = request.get_json()
    user_message = data.get("message", "")

    reply = chatbot_reply(user_message, amounts, times)

    return jsonify({
        "reply": reply
    })


if __name__ == "__main__":
    app.run(debug=True)
