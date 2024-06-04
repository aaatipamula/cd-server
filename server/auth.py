import os
import hmac
from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, redirect, render_template, current_app, request, session, url_for, jsonify

auth = Blueprint("auth", __name__, url_prefix="/auth")

USERNAME = os.environ.get('FLASK_AUTH_USERNAME', 'test')
PASSWORD = os.environ.get('FLASK_AUTH_PASSWORD', '123')

err_codes = {
    "10": "Invalid login"
}

def check_auth(username, password):
    return hmac.compare_digest(username, USERNAME) and hmac.compare_digest(password, PASSWORD)

def requires_auth(is_api=False):
    """Decorator to prompt for login or return JSON for API endpoints."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'logged_in' not in session:
                if is_api:
                    return jsonify({"error": "Unauthorized"}), 401
                return redirect(url_for('auth.login'))
            now = datetime.now()
            last_activity = session.get('last_activity', now)
            if now - last_activity > current_app.permanent_session_lifetime:
                if is_api:
                    return jsonify({"error": "Session expired"}), 401
                return redirect(url_for('auth.logout'))
            session['last_activity'] = now
            return f(*args, **kwargs)
        return decorated
    return decorator

@auth.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True
    current_app.permanent_session_lifetime = timedelta(minutes=5)  # Reset session lifetime on each request

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if check_auth(username, password):
            session['logged_in'] = True
            session['last_activity'] = datetime.now()
            return redirect(url_for('admin.get_admin'))
        else:
            return redirect(f"{url_for('auth.login')}?err_code={10}")

    code = request.args.get("err_code", "")
    return render_template("login.html", error=err_codes.get(code))

@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

