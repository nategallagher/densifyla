from app import app, db
from flask import render_template


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500


@app.errorhandler(401)
def unauthorized_error(error):
    return render_template("errors/401.html"), 401
