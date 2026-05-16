from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import pandas as pd
import sqlite3
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from tensorflow.keras.models import load_model

# =========================
# App Config
# =========================
app = Flask(__name__)
app.secret_key = "epilepsy_secret_key"

# =========================
# Load Model & Scaler
# =========================
model = load_model("cnn_model.h5", compile=False)
scaler = joblib.load("scaler.pkl")

# =========================
# EEG Class Mapping
# =========================
EEG_MAPPING = {
    1: "Seizure Activity",
    2: "Tumor Region EEG (Non-Seizure)",
    3: "Healthy Brain Region EEG (Non-Seizure)",
    4: "Eyes Closed EEG (Non-Seizure)",
    5: "Eyes Open EEG (Non-Seizure)"
}


# =========================
# Database
# =========================
def get_db():
    return sqlite3.connect("users.db")

with get_db() as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            eeg_class INTEGER,
            eeg_label TEXT
        )
    """)

# =========================
# Routes
# =========================
@app.route("/")
def home():
    return render_template("home.html")

# -------------------------
# Register
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            with get_db() as con:
                con.execute(
                    "INSERT INTO users VALUES (NULL, ?, ?)",
                    (request.form["username"], request.form["password"])
                )
            return redirect(url_for("login"))
        except:
            return "⚠ Username already exists"
    return render_template("register.html")

# -------------------------
# Login
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cur = get_db().cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (request.form["username"], request.form["password"])
        )
        if cur.fetchone():
            session["user"] = request.form["username"]
            return redirect(url_for("prediction"))
        return "❌ Invalid credentials"
    return render_template("login.html")


@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None

    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename.endswith(".xlsx"):
            df = pd.read_excel(file)

            # ✅ Remove non-EEG columns
            df = df.drop(columns=["Unnamed", "y"], errors="ignore")

            # ✅ Validate EEG features
            if df.shape[1] != 178:
                return "❌ File must contain exactly 178 EEG features"

            # ✅ Scale & reshape for CNN
            X = scaler.transform(df.values)
            X = X.reshape(X.shape[0], X.shape[1], 1)

            preds = model.predict(X)
            pred_class = int(np.argmax(preds[0]) + 1)
            label = EEG_MAPPING[pred_class]

            with get_db() as con:
                con.execute(
                    "INSERT INTO predictions (username, eeg_class, eeg_label) VALUES (?,?,?)",
                    (session["user"], pred_class, label)
                )

            result = label
            session["last_result"] = label

    return render_template("prediction.html", result=result)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    cur = get_db().cursor()
    cur.execute("""
        SELECT eeg_label, COUNT(*) 
        FROM predictions 
        WHERE username=?
        GROUP BY eeg_label
    """, (session["user"],))
    data = cur.fetchall()

    labels = [row[0] for row in data]
    counts = [row[1] for row in data]

    
    # Graph
    plt.figure(figsize=(9, 5))
    plt.bar(labels, counts)

    plt.title("EEG Prediction Distribution", fontsize=14)
    plt.xlabel("EEG Class", fontsize=12)
    plt.ylabel("Count", fontsize=12)

    # 🔑 Key fix
    plt.xticks(rotation=30, ha="right", fontsize=9)

    plt.tight_layout()

    graph_path = "static/prediction_graph.png"
    plt.savefig(graph_path)
    plt.close()


    return render_template(
        "dashboard.html",
        graph=graph_path,
        result=session.get("last_result")
    )

# -------------------------
# Logout
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# =========================
# Run App
# =========================
if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)
