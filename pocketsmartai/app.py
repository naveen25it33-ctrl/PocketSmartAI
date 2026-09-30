import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from services.gemini_utils import generate_recommendations

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "pocketsmart-dev-secret")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/login")
def login_page():
    return render_template("login.html")

@app.get("/register")
def register_page():
    return render_template("register.html")

@app.post("/login")
def login():
    data = request.get_json(silent=True) or request.form
    email = data.get("email", "").strip()
    password = data.get("password", "")
    if not email or not password:
        return jsonify({"ok": False, "message": "Email and password are required."}), 400
    session["user"] = {"email": email}
    return jsonify({"ok": True, "message": "Login successful.", "redirect": "/"})

@app.post("/register")
def register():
    data = request.get_json(silent=True) or request.form
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    if not name or not email or not password:
        return jsonify({"ok": False, "message": "Name, email and password are required."}), 400
    session["user"] = {"name": name, "email": email}
    return jsonify({"ok": True, "message": "Registration successful.", "redirect": "/"})

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.get("/session-info")
def session_info():
    return jsonify({"logged_in": "user" in session, "user": session.get("user")})

@app.post("/generate-home")
def generate_home():
    data = request.get_json(silent=True) or {}
    return _generate("home", data)

@app.post("/generate-party")
def generate_party():
    data = request.get_json(silent=True) or {}
    return _generate("party", data)

@app.post("/generate-jewelry")
def generate_jewelry():
    data = request.form.to_dict()
    image = request.files.get("image")
    image_bytes = image.read() if image else None
    return _generate("jewelry", data, image_bytes)

def _generate(category, data, image_bytes=None):
    try:
        budget = float(data.get("budget", 0))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "message": "Please enter a valid budget."}), 400

    if budget <= 0:
        return jsonify({"ok": False, "message": "Budget must be greater than zero."}), 400

    result = generate_recommendations(category, data, budget, image_bytes)
    session["last_recommendation"] = result
    return jsonify({"ok": True, "category": category, "result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
